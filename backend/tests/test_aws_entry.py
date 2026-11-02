import io
import json
import unittest
from unittest.mock import patch

import boto3
from botocore.exceptions import ClientError
from botocore.stub import ANY, Stubber
from runpass import lambda_entry
from runpass.api import create_app
from runpass.aws_adapters import CognitoAccountRemover, S3AuditSink, S3BlobStore
from runpass.identity import JwksProvider
from runpass.service import Problem
from runpass.store import Unavailable

FAKE_CREDENTIALS = {
    "region_name": "sa-east-1",
    "aws_access_key_id": "synthetic",
    "aws_secret_access_key": "synthetic",
}
EVENT_ID, OCCURRED_AT = "event-1", "2026-10-28T15:00:00Z"
AUDIT_KEY = "dev/2026-10-28/event-1.json"


def client(service):
    return boto3.client(service, **FAKE_CREDENTIALS)


def stream_record(pk, sequence="1", **image):
    new_image = {"PK": {"S": pk}, **{k: {"S": v} for k, v in image.items()}}
    return {"dynamodb": {"SequenceNumber": sequence, "NewImage": new_image}}


class S3BlobStoreTests(unittest.TestCase):
    def setUp(self):
        self.client = client("s3")
        self.stub = Stubber(self.client)
        self.stub.activate()
        self.blobs = S3BlobStore(self.client, "photos")
        self.addCleanup(self.stub.assert_no_pending_responses)

    def test_upload_url_is_scoped_to_owner_prefix_and_expires_in_15_minutes(self):
        def build(service, **kwargs):
            return boto3.client(service, **FAKE_CREDENTIALS, **kwargs)

        with patch.object(lambda_entry, "_boto_client", build):
            blobs = S3BlobStore(lambda_entry._s3_client(), "photos")
        issued = blobs.issue("upload-1", "image/jpeg", "owner-1")
        self.assertIn(
            "photos.s3.sa-east-1.amazonaws.com/temporary/owner-1/upload-1", issued["uploadUrl"]
        )
        self.assertIn("X-Amz-Algorithm=AWS4-HMAC-SHA256", issued["uploadUrl"])
        self.assertEqual(issued["uploadMethod"], "PUT")
        self.assertEqual(issued["uploadHeaders"], {"Content-Type": "image/jpeg"})
        self.assertIn("X-Amz-Expires=900", issued["uploadUrl"])

    def test_head_reports_pinned_version_and_missing_object_is_a_conflict(self):
        self.stub.add_response(
            "head_object",
            {"VersionId": "v1", "ContentLength": 10, "ContentType": "image/jpeg"},
            {"Bucket": "photos", "Key": "temporary/owner-1/upload-1"},
        )
        self.assertEqual(
            self.blobs.head("upload-1", "owner-1"),
            {"version": "v1", "size": 10, "contentType": "image/jpeg"},
        )
        self.stub.add_client_error("head_object", "404")
        with self.assertRaises(Problem) as error:
            self.blobs.head("upload-1", "owner-1")
        self.assertEqual(error.exception.code, "OBJECT_NOT_UPLOADED")

    def test_read_requests_the_pinned_version(self):
        from botocore.response import StreamingBody

        self.stub.add_response(
            "get_object",
            {"Body": StreamingBody(io.BytesIO(b"bytes"), 5)},
            {"Bucket": "photos", "Key": "temporary/owner-1/upload-1", "VersionId": "v1"},
        )
        self.assertEqual(self.blobs.read("upload-1", "v1", "owner-1"), b"bytes")

    def test_delete_owner_removes_versions_and_markers_only_under_owner_prefixes(self):
        self.stub.add_response(
            "list_object_versions",
            {
                "Versions": [{"Key": "temporary/owner-1/a", "VersionId": "1"}],
                "DeleteMarkers": [{"Key": "temporary/owner-1/a", "VersionId": "2"}],
            },
            {"Bucket": "photos", "Prefix": "temporary/owner-1/"},
        )
        self.stub.add_response(
            "delete_objects",
            {},
            {
                "Bucket": "photos",
                "Delete": {
                    "Objects": [
                        {"Key": "temporary/owner-1/a", "VersionId": "1"},
                        {"Key": "temporary/owner-1/a", "VersionId": "2"},
                    ],
                    "Quiet": True,
                },
            },
        )
        self.stub.add_response(
            "list_object_versions", {}, {"Bucket": "photos", "Prefix": "derived/owner-1/"}
        )
        self.assertEqual(self.blobs.delete_owner("owner-1"), 2)

    def test_partial_delete_failure_keeps_the_job_retriable(self):
        self.stub.add_response(
            "list_object_versions", {"Versions": [{"Key": "temporary/o/a", "VersionId": "1"}]}
        )
        self.stub.add_response(
            "delete_objects",
            {"Errors": [{"Key": "temporary/o/a", "Code": "InternalError"}]},
        )
        with self.assertRaises(Unavailable):
            self.blobs.delete_owner("o")


class S3AuditSinkTests(unittest.TestCase):
    def setUp(self):
        self.client = client("s3")
        self.stub = Stubber(self.client)
        self.stub.activate()
        self.sink = S3AuditSink(self.client, "audit", "dev")

    def test_key_has_no_personal_data_and_create_is_conditional(self):
        self.stub.add_response(
            "put_object",
            {},
            {
                "Bucket": "audit",
                "Key": AUDIT_KEY,
                "Body": ANY,
                "ContentType": "application/json",
                "Metadata": ANY,
                "IfNoneMatch": "*",
            },
        )
        self.assertEqual(self.sink.put(EVENT_ID, OCCURRED_AT, {"comment": "x"}), AUDIT_KEY)
        self.stub.assert_no_pending_responses()

    def retry_with_stored_digest(self, stored_digest):
        self.stub.add_client_error("put_object", "PreconditionFailed")
        self.stub.add_response("head_object", {"Metadata": {"sha256": stored_digest}})
        return self.sink.put(EVENT_ID, OCCURRED_AT, {"a": 1})

    def test_retry_with_same_content_confirms_and_divergent_content_conflicts(self):
        import hashlib

        digest = hashlib.sha256(b'{"a": 1}').hexdigest()
        self.assertEqual(self.retry_with_stored_digest(digest), AUDIT_KEY)
        with self.assertRaises(Problem) as error:
            self.retry_with_stored_digest("different")
        self.assertEqual(error.exception.code, "AUDIT_COLLISION")


class CognitoRemoverTests(unittest.TestCase):
    def setUp(self):
        self.client = client("cognito-idp")
        self.stub = Stubber(self.client)
        self.stub.activate()
        self.remover = CognitoAccountRemover(self.client, "sa-east-1_pool")

    def test_already_removed_user_is_success_and_other_errors_retry(self):
        self.stub.add_response(
            "admin_delete_user", {}, {"UserPoolId": "sa-east-1_pool", "Username": "owner-1"}
        )
        self.remover.delete_owner("owner-1")
        self.stub.add_client_error("admin_delete_user", "UserNotFoundException")
        self.remover.delete_owner("owner-1")
        self.stub.add_client_error("admin_delete_user", "TooManyRequestsException")
        with self.assertRaises(Unavailable):
            self.remover.delete_owner("owner-1")


class ConsumerTests(unittest.TestCase):
    class Processor:
        def __init__(self, outcome=None):
            self.outcome, self.calls = outcome, []

        def deliver(self, owner, event_id, consumer, epoch):
            self.calls.append((owner, event_id, consumer, epoch))
            if self.outcome:
                raise self.outcome

    @staticmethod
    def batch(body=None):
        body = body or json.dumps({"owner": "o", "eventId": "e", "dispatchEpoch": 3})
        return {"Records": [{"messageId": "m1", "body": body}]}

    def test_delivers_identifiers_and_epoch(self):
        processor = self.Processor()
        self.assertEqual(
            lambda_entry.consume(processor, "score", self.batch()), {"batchItemFailures": []}
        )
        self.assertEqual(processor.calls, [("o", "e", "score", 3)])

    def test_terminal_refusals_are_acknowledged(self):
        for status, code in (
            (404, "EVENT_NOT_FOUND"),
            (409, "STALE_DISPATCH_EPOCH"),
            (410, "EVENT_EXPIRED"),
        ):
            result = lambda_entry.consume(
                self.Processor(Problem(status, code)), "audit", self.batch()
            )
            self.assertEqual(result, {"batchItemFailures": []})

    def test_transient_failures_return_only_that_message(self):
        for failure in (Unavailable(), Problem(503, "CONCURRENT_RETRY_REQUIRED")):
            result = lambda_entry.consume(self.Processor(failure), "audit", self.batch())
            self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "m1"}]})

    def test_malformed_message_is_discarded(self):
        processor = self.Processor()
        self.assertEqual(
            lambda_entry.consume(processor, "score", self.batch("not-json")),
            {"batchItemFailures": []},
        )
        self.assertEqual(processor.calls, [])


class PublisherTests(unittest.TestCase):
    class Store:
        def __init__(self, event):
            self.event = event

        def get(self, key):
            return self.event

    class Sqs:
        def __init__(self, fail=False):
            self.sent, self.fail = [], fail

        def send_message(self, QueueUrl, MessageBody):
            if self.fail:
                raise ClientError({"Error": {"Code": "Throttled", "Message": "x"}}, "SendMessage")
            self.sent.append((QueueUrl, json.loads(MessageBody)))

    MARKER = {"owner": "o", "eventId": "e"}

    def run_publish(self, sqs, event, records):
        return lambda_entry.publish(
            self.Store(event), sqs, ["score-q", "audit-q"], {"Records": records}
        )

    def test_sends_only_identifiers_with_current_epoch_to_each_destination(self):
        sqs = self.Sqs()
        result = self.run_publish(
            sqs,
            {"dispatchEpoch": 2, "ratings": {"a": 5}},
            [stream_record("WORK#event#pending#03", **self.MARKER)],
        )
        self.assertEqual(result, {"batchItemFailures": []})
        body = {"owner": "o", "eventId": "e", "dispatchEpoch": 2}
        self.assertEqual(sqs.sent, [("score-q", body), ("audit-q", body)])

    def test_ignores_other_partitions_and_erased_events(self):
        sqs = self.Sqs()
        self.run_publish(sqs, {"dispatchEpoch": 1}, [stream_record("USER#o")])
        self.run_publish(sqs, None, [stream_record("WORK#event#pending#03", **self.MARKER)])
        self.assertEqual(sqs.sent, [])

    def test_failure_reports_sequence_for_retry(self):
        with self.assertLogs("runpass", "ERROR"):
            result = self.run_publish(
                self.Sqs(fail=True),
                {"dispatchEpoch": 1},
                [stream_record("WORK#event#pending#03", sequence="42", **self.MARKER)],
            )
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "42"}]})


class MaintenanceTests(unittest.TestCase):
    class Tasks:
        def __init__(self, reconcile=None, erase=None):
            self.reconcile_outcome, self.erase_outcome = reconcile, erase
            self.expired = False

        def reconcile(self, worker_id):
            if self.reconcile_outcome:
                raise self.reconcile_outcome
            return {"processed": 0, "failed": 0}

        def expire_payloads(self):
            self.expired = True
            return {"removed": 0, "auditExpired": 0}

        def run_pending(self):
            if self.erase_outcome:
                raise self.erase_outcome
            return {"completed": 0, "pending": 0}

    def test_held_lease_is_not_an_error(self):
        tasks = self.Tasks(reconcile=Problem(409, "LEASE_HELD"))
        summary = lambda_entry.run_maintenance(tasks, tasks, "request-1")
        self.assertEqual(summary["reconcile"], {"skipped": "LEASE_HELD"})

    def test_failure_runs_remaining_tasks_and_then_raises_for_the_alarm(self):
        tasks = self.Tasks(reconcile=Unavailable())
        with self.assertRaises(RuntimeError):
            lambda_entry.run_maintenance(tasks, tasks, "request-1")
        self.assertTrue(tasks.expired)


class ApiHandlerTests(unittest.TestCase):
    def test_http_api_event_reaches_fastapi_and_stays_fail_closed(self):
        from mangum import Mangum

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/me",
            "rawQueryString": "",
            "headers": {"host": "api.example.test"},
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/me",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "192.0.2.1",
                    "userAgent": "test",
                },
                "domainName": "api.example.test",
                "stage": "$default",
            },
            "isBase64Encoded": False,
        }
        handler = Mangum(create_app(), lifespan="off")
        with patch.object(lambda_entry, "_api", return_value=handler):
            response = lambda_entry.api_handler(event, object())
        self.assertEqual(response["statusCode"], 503)
        self.assertEqual(json.loads(response["body"])["code"], "DEPENDENCY_UNAVAILABLE")

    def test_import_does_not_load_secrets_or_clients(self):
        with patch.object(lambda_entry, "_boto_client", side_effect=AssertionError("eager")):
            import importlib

            importlib.reload(lambda_entry)


class JwksProviderTests(unittest.TestCase):
    ISSUER = "https://cognito-idp.sa-east-1.amazonaws.com/sa-east-1_AbC123"

    def test_accepts_only_the_issuer_of_the_configured_region(self):
        JwksProvider(self.ISSUER, "sa-east-1")
        for issuer, region in (
            (self.ISSUER, "us-east-2"),
            ("https://cognito-idp.us-east-2.amazonaws.com/us-east-2_AbC123", "sa-east-1"),
            ("https://cognito-idp.sa-east-1.amazonaws.com/us-east-2_AbC123", "sa-east-1"),
            ("https://evil.example/sa-east-1_AbC123", "sa-east-1"),
            (self.ISSUER + "/extra", "sa-east-1"),
            (self.ISSUER, "sa-east-1|.*"),
        ):
            with self.subTest(issuer=issuer, region=region):
                with self.assertRaises(ValueError):
                    JwksProvider(issuer, region)
