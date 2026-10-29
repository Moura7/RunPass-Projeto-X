import io
import unittest
from datetime import datetime, timedelta, timezone

from PIL import Image
from runpass.identity import Principal
from runpass.service import IdentityService, Problem
from runpass.store import MemoryStore
from runpass.upload import MemoryBlobStore, UploadService

NOW = datetime(2026, 10, 28, 15, tzinfo=timezone.utc)


def jpeg(color="red", size=(40, 20), orientation=None):
    output = io.BytesIO()
    exif = Image.Exif()
    if orientation:
        exif[274] = orientation
    Image.new("RGB", size, color).save(output, "JPEG", exif=exif)
    return output.getvalue()


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.now = NOW
        self.store = MemoryStore()
        self.identity = IdentityService(
            self.store, b"upload-test-hmac-key-at-least-32-bytes", lambda: self.now
        )
        self.blobs = MemoryBlobStore()
        self.service = UploadService(self.identity, self.blobs)
        self.actor = self.admit("owner")

    def admit(self, subject):
        actor = Principal(subject, True)
        self.identity.create_profile(
            actor, "profile-" + subject, {"displayName": subject, "username": subject}
        )
        self.identity.admit(
            actor,
            "admit-" + subject,
            {"birthDate": "1990-01-01", "declaresAdult": True},
        )
        return actor

    def start_and_put(self, data, content_type="image/jpeg", key="start"):
        session = self.service.start(
            self.actor, key, {"contentType": content_type, "sizeBytes": len(data)}
        )
        expires = datetime.fromisoformat(session["expiresAt"].replace("Z", "+00:00"))
        version = self.blobs.put(
            session["uploadId"], self.actor.subject, expires, content_type, data, self.now
        )
        return session, version

    def test_valid_image_is_oriented_and_stripped_before_reference(self):
        source = jpeg(size=(40, 20), orientation=6)
        session, _ = self.start_and_put(source)
        result = self.service.finalize(self.actor, session["uploadId"], "finish")
        self.assertEqual(result["state"], "valid")
        reference = result["imageReference"]
        derived = Image.open(io.BytesIO(self.blobs.derived[reference]["data"]))
        self.assertEqual(derived.size, (20, 40))
        self.assertEqual(len(derived.getexif()), 0)
        self.assertLessEqual(len(self.blobs.derived[reference]["data"]), 1_000_000)
        image_item = self.store.get(("operations", "USER#owner", "IMAGE#" + reference))
        self.assertEqual((image_item["state"], image_item["refs"]), ("valid", 0))

    def test_finalize_pins_version_even_if_url_is_overwritten(self):
        original = jpeg("red")
        session, first_version = self.start_and_put(original)
        process = self.service.process
        self.service.process = lambda owner, upload_id: self.store.get(
            ("operations", "USER#" + owner, "UPLOAD#" + upload_id)
        )
        pending = self.service.finalize(self.actor, session["uploadId"], "finish")
        self.assertEqual(pending["state"], "pending")
        expires = datetime.fromisoformat(session["expiresAt"].replace("Z", "+00:00"))
        replacement = jpeg("blue")
        self.assertEqual(len(replacement), len(original))
        self.blobs.put(session["uploadId"], "owner", expires, "image/jpeg", replacement, self.now)
        self.service.process = process
        result = self.service.process("owner", session["uploadId"])
        self.assertEqual(result["sourceVersion"], first_version)
        derived = Image.open(io.BytesIO(self.blobs.derived[result["imageReference"]]["data"]))
        self.assertGreater(derived.getpixel((0, 0))[0], derived.getpixel((0, 0))[2])

    def test_invalid_bytes_mime_and_declared_size_fail_closed(self):
        invalid = b"not an image"
        session, _ = self.start_and_put(invalid)
        result = self.service.finalize(self.actor, session["uploadId"], "bad")
        self.assertEqual(
            result,
            {"uploadId": session["uploadId"], "state": "failed", "reasonCode": "INVALID_IMAGE"},
        )

        png = io.BytesIO()
        Image.new("RGB", (10, 10)).save(png, "PNG")
        session, _ = self.start_and_put(png.getvalue(), "image/jpeg", "mime")
        result = self.service.finalize(self.actor, session["uploadId"], "mime-finish")
        self.assertEqual(result["reasonCode"], "FORMAT_MISMATCH")

        session = self.service.start(
            self.actor, "wrong-size", {"contentType": "image/jpeg", "sizeBytes": len(jpeg()) + 1}
        )
        expires = datetime.fromisoformat(session["expiresAt"].replace("Z", "+00:00"))
        self.blobs.put(session["uploadId"], "owner", expires, "image/jpeg", jpeg(), self.now)
        with self.assertRaises(Problem) as error:
            self.service.finalize(self.actor, session["uploadId"], "wrong-finish")
        self.assertEqual(error.exception.code, "OBJECT_MISMATCH")

    def test_expiration_timeout_and_owner_authorization(self):
        source = jpeg()
        session, _ = self.start_and_put(source)
        other = self.admit("other")
        original_head = self.blobs.head
        head_calls = []
        self.blobs.head = lambda upload_id: head_calls.append(upload_id) or original_head(upload_id)
        with self.assertRaises(Problem) as error:
            self.service.get(other, session["uploadId"])
        self.assertEqual(error.exception.code, "UPLOAD_NOT_FOUND")
        with self.assertRaises(Problem) as error:
            self.service.finalize(other, session["uploadId"], "foreign-finalize")
        self.assertEqual(error.exception.code, "UPLOAD_NOT_FOUND")
        self.assertEqual(head_calls, [])

        self.now += timedelta(minutes=16)
        with self.assertRaises(Problem) as error:
            self.service.finalize(self.actor, session["uploadId"], "expired")
        self.assertEqual(error.exception.code, "SESSION_EXPIRED")

        self.now = NOW
        session, _ = self.start_and_put(source, key="timeout")
        process = self.service.process
        self.service.process = lambda owner, upload_id: self.store.get(
            ("operations", "USER#" + owner, "UPLOAD#" + upload_id)
        )
        self.service.finalize(self.actor, session["uploadId"], "pin")
        self.service.process = process
        self.now += timedelta(minutes=16)
        result = self.service.process("owner", session["uploadId"])
        self.assertEqual((result["state"], result["reasonCode"]), ("failed", "PROCESSING_TIMEOUT"))

    def test_pixel_limit_fails_without_creating_a_reference(self):
        output = io.BytesIO()
        Image.new("1", (5001, 5000)).save(output, "PNG")
        session, _ = self.start_and_put(output.getvalue(), "image/png", "pixels")
        result = self.service.finalize(self.actor, session["uploadId"], "pixels-finish")
        self.assertEqual(result["state"], "failed")
        self.assertEqual(result["reasonCode"], "PIXEL_LIMIT_EXCEEDED")
        self.assertEqual(self.blobs.derived, {})

    def test_start_is_idempotent_and_rejects_unadmitted(self):
        body = {"contentType": "image/jpeg", "sizeBytes": 10}
        first = self.service.start(self.actor, "same", body)
        self.assertEqual(self.service.start(self.actor, "same", body), first)
        with self.assertRaises(Problem):
            self.service.start(Principal("new", True), "new", body)
