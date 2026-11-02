"""Local durable-event consumers; transport is replaceable and never carries payloads."""

from copy import deepcopy
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from .service import Problem, stamp
from .store import Conflict, iter_partition

MANDATORY = ("score", "audit")
LEASE_SECONDS = 60
MAX_BACKOFF_SECONDS = 300
AUDIT_RETENTION_DAYS = 60


class EventProcessor:
    def __init__(self, identity, audit_sink=None):
        self.identity, self.store, self.audit_sink = identity, identity.store, audit_sink

    @staticmethod
    def score_projection(item):
        if not item or not item.get("reviewCount"):
            return {"reviewCount": 0, "runScore": None}
        value = Decimal(item["ratingSum"]) / Decimal(8 * item["reviewCount"])
        return {
            "reviewCount": item["reviewCount"],
            "runScore": str(value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
        }

    def get_score(self, edition_id):
        return self.score_projection(
            self.store.get(("projections", "EDITION#" + edition_id, "SCORE#current"))
        )

    def acquire_lease(self, consumer, worker_id, fencing_token=None):
        """Acquire or renew one consumer lease with a monotonic fencing token."""
        if consumer not in MANDATORY:
            raise Problem(422, "UNKNOWN_CONSUMER")
        key = ("operations", "WORKER#" + consumer, "FENCE")
        for _ in range(20):
            now = self.identity.clock()
            current = self.store.get(key)
            active = current and now < self._parse(current["leaseExpiresAt"])
            renewing = bool(
                active
                and current["workerId"] == worker_id
                and current["fencingToken"] == fencing_token
            )
            if active and not renewing:
                raise Problem(409, "LEASE_HELD")
            token = (
                current["fencingToken"] if renewing else (current or {}).get("fencingToken", 0) + 1
            )
            updated = {
                "consumer": consumer,
                "workerId": worker_id,
                "fencingToken": token,
                "leaseExpiresAt": stamp(now + timedelta(seconds=LEASE_SECONDS)),
            }
            try:
                self.store.commit({key: current}, {key: updated})
                return {key: value for key, value in updated.items()}
            except Conflict:
                continue
        raise Problem(503, "CONCURRENT_RETRY_REQUIRED")

    def _require_fence(self, consumer, worker_id, fencing_token):
        lease = self.store.get(("operations", "WORKER#" + consumer, "FENCE"))
        now = self.identity.clock()
        if not (
            lease
            and lease["workerId"] == worker_id
            and lease["fencingToken"] == fencing_token
            and now < self._parse(lease["leaseExpiresAt"])
        ):
            raise Problem(409, "STALE_FENCING_TOKEN")

    @staticmethod
    def _parse(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def deliver(
        self,
        owner,
        event_id,
        consumer,
        dispatch_epoch=1,
        *,
        worker_id=None,
        fencing_token=None,
    ):
        if consumer not in MANDATORY:
            raise Problem(422, "UNKNOWN_CONSUMER")
        if worker_id is not None or fencing_token is not None:
            self._require_fence(consumer, worker_id, fencing_token)
        pk = "USER#" + owner
        event_key = ("operations", pk, "EVENT#" + event_id)
        for _ in range(20):
            event = self.store.get(event_key)
            if not event:
                raise Problem(404, "EVENT_NOT_FOUND")
            if event.get("dispatchEpoch") != dispatch_epoch:
                raise Problem(409, "STALE_DISPATCH_EPOCH")
            now = self.identity.clock()
            payload_expiry = event.get("payloadExpiresAt")
            if payload_expiry and now >= self._parse(payload_expiry):
                raise Problem(410, "EVENT_EXPIRED")
            if consumer == "audit" and event.get("auditPayloadExpiredAt"):
                raise Problem(410, "AUDIT_PAYLOAD_EXPIRED")
            delivery_key = ("operations", pk, f"DELIVERY#{event_id}#{consumer}")
            delivery = self.store.get(delivery_key)
            if delivery:
                return {key: value for key, value in delivery.items() if key != "_rev"}
            expected = {event_key: event, delivery_key: None}
            writes = {}
            if consumer == "score":
                self._score(owner, event, expected, writes)
            else:
                self._audit(owner, event, now, expected, writes)
            delivered = {
                "eventId": event_id,
                "consumer": consumer,
                "confirmedAt": stamp(now),
                "dispatchEpoch": dispatch_epoch,
            }
            writes[delivery_key] = delivered
            other = MANDATORY[1] if consumer == MANDATORY[0] else MANDATORY[0]
            other_key = ("operations", pk, f"DELIVERY#{event_id}#{other}")
            expected[other_key] = self.store.get(other_key)
            updated = deepcopy(event)
            if expected[other_key] and not updated.get("allConfirmedAt"):
                updated["allConfirmedAt"] = stamp(now)
                updated["payloadExpiresAt"] = stamp(now + timedelta(days=7))
                work_key = (
                    "operations",
                    updated["workPartition"],
                    updated["workSort"],
                )
                work = self.store.get(work_key)
                expected[work_key] = work
                if work:
                    writes[work_key] = {**work, "state": "completed", "completedAt": stamp(now)}
            writes[event_key] = updated
            try:
                self.store.commit(expected, writes)
                return delivered
            except Conflict:
                continue
        raise Problem(503, "CONCURRENT_RETRY_REQUIRED")

    def reconcile(self, limit=100, worker_id="local-reconciler"):
        processed, failed = 0, 0
        leases = {}
        for consumer in MANDATORY:
            current = self.store.get(("operations", "WORKER#" + consumer, "FENCE"))
            token = (
                current.get("fencingToken")
                if current and current.get("workerId") == worker_id
                else None
            )
            leases[consumer] = self.acquire_lease(consumer, worker_id, token)
        for shard in range(16):
            for _, marker in iter_partition(
                self.store, "operations", f"WORK#event#pending#{shard:02d}"
            ):
                if marker.get("state") != "pending":
                    continue
                if self.identity.clock() < self._parse(marker["nextAttemptAt"]):
                    continue
                try:
                    for consumer in MANDATORY:
                        lease = leases[consumer]
                        self.deliver(
                            marker["owner"],
                            marker["eventId"],
                            consumer,
                            worker_id=worker_id,
                            fencing_token=lease["fencingToken"],
                        )
                    processed += 1
                except Problem:
                    self._record_failure(marker)
                    failed += 1
                if processed + failed >= limit:
                    return {"processed": processed, "failed": failed}
        return {"processed": processed, "failed": failed}

    def _record_failure(self, marker):
        key = ("operations", marker["workPartition"], marker["workSort"])
        current = self.store.get(key)
        if not current or current.get("state") != "pending":
            return
        attempts = current.get("attempts", 0) + 1
        delay = min(2 ** (attempts - 1), MAX_BACKOFF_SECONDS)
        updated = {
            **current,
            "attempts": attempts,
            "nextAttemptAt": stamp(self.identity.clock() + timedelta(seconds=delay)),
        }
        try:
            self.store.commit({key: current}, {key: updated})
        except Conflict:
            pass

    def expire_payloads(self, limit=100):
        """Actively remove expired payloads; TTL remains only a secondary safeguard."""
        removed, audit_expired = 0, 0
        now = self.identity.clock()
        for shard in range(16):
            for _, marker in iter_partition(
                self.store, "operations", f"WORK#event#pending#{shard:02d}"
            ):
                owner, event_id = marker.get("owner"), marker.get("eventId")
                if not owner or not event_id:
                    continue
                event_key = ("operations", "USER#" + owner, "EVENT#" + event_id)
                event = self.store.get(event_key)
                if not event:
                    audit_expiry = marker.get("auditExpiresAt")
                    if audit_expiry and now >= self._parse(audit_expiry):
                        self._discard_audit_locator(marker)
                        removed += 1
                    continue
                completed_expiry = event.get("payloadExpiresAt")
                audit_expiry = self._parse(event["occurredAt"]) + timedelta(
                    days=AUDIT_RETENTION_DAYS
                )
                if completed_expiry and now >= self._parse(completed_expiry):
                    self._discard_event(marker, event, "DELIVERED_PAYLOAD_EXPIRED")
                    removed += 1
                elif now >= audit_expiry and not self._delivery(owner, event_id, "audit"):
                    if not self._delivery(owner, event_id, "score"):
                        self.deliver(owner, event_id, "score")
                    self._discard_event(marker, event, "AUDIT_PAYLOAD_EXPIRED")
                    audit_expired += 1
                if removed + audit_expired >= limit:
                    return {"removed": removed, "auditExpired": audit_expired}
        return {"removed": removed, "auditExpired": audit_expired}

    def _delivery(self, owner, event_id, consumer):
        return self.store.get(("operations", "USER#" + owner, f"DELIVERY#{event_id}#{consumer}"))

    def _discard_event(self, marker, event, reason):
        owner, event_id = marker["owner"], marker["eventId"]
        event_key = ("operations", "USER#" + owner, "EVENT#" + event_id)
        work_key = ("operations", event["workPartition"], event["workSort"])
        keys = [event_key, work_key]
        for consumer in MANDATORY:
            keys.append(("operations", "USER#" + owner, f"DELIVERY#{event_id}#{consumer}"))
        expected = {key: self.store.get(key) for key in keys}
        minimal = {
            "state": "expired",
            "reason": reason,
            "expiredAt": stamp(self.identity.clock()),
        }
        lake = self.store.get(("operations", "USER#" + owner, "LAKE#" + event_id))
        if lake and reason == "DELIVERED_PAYLOAD_EXPIRED":
            minimal.update(
                owner=owner,
                eventId=event_id,
                auditExpiresAt=lake["expiresAt"],
                workPartition=event["workPartition"],
                workSort=event["workSort"],
            )
        writes = {key: None for key in keys}
        writes[work_key] = minimal
        try:
            self.store.commit(expected, writes)
        except Conflict as error:
            raise Problem(503, "CONCURRENT_RETRY_REQUIRED") from error

    def _discard_audit_locator(self, marker):
        work_key = ("operations", marker["workPartition"], marker["workSort"])
        lake_key = (
            "operations",
            "USER#" + marker["owner"],
            "LAKE#" + marker["eventId"],
        )
        expected = {work_key: self.store.get(work_key), lake_key: self.store.get(lake_key)}
        object_key = (expected[lake_key] or {}).get("objectKey")
        if self.audit_sink is not None and object_key:
            self.audit_sink.delete(object_key)
        try:
            self.store.commit(expected, {work_key: None, lake_key: None})
        except Conflict as error:
            raise Problem(503, "CONCURRENT_RETRY_REQUIRED") from error

    def _score(self, owner, event, expected, writes):
        participation_id = event["participationId"]
        pk = "USER#" + owner
        part_key = ("history", pk, "P#" + participation_id + "#PART")
        review_key = ("history", pk, "P#" + participation_id + "#REVIEW")
        account_key = ("identity", pk, "ACCOUNT")
        contribution_key = ("projections", pk, "CONTRIBUTION#" + participation_id)
        for key in (part_key, review_key, account_key, contribution_key):
            expected[key] = self.store.get(key)
        part, review, account, old = (
            expected[k] for k in (part_key, review_key, account_key, contribution_key)
        )
        valid = bool(
            account
            and account.get("state") == "active"
            and part
            and part.get("state") == "completed"
            and review
            and review.get("moderationState") == "valid"
        )
        new = None
        if valid:
            new = {
                "participationId": participation_id,
                "editionId": part["editionId"],
                "effectVersion": review["effectVersion"],
                "ratingSum": sum(review["ratings"].values()),
            }
        editions = {value["editionId"] for value in (old, new) if value}
        for edition_id in editions:
            score_key = ("projections", "EDITION#" + edition_id, "SCORE#current")
            score = self.store.get(score_key)
            expected[score_key] = score
            updated = deepcopy(score) if score else {"ratingSum": 0, "reviewCount": 0}
            if old and old["editionId"] == edition_id:
                updated["ratingSum"] -= old["ratingSum"]
                updated["reviewCount"] -= 1
            if new and new["editionId"] == edition_id:
                updated["ratingSum"] += new["ratingSum"]
                updated["reviewCount"] += 1
            writes[score_key] = updated
        writes[contribution_key] = new

    def _audit(self, owner, event, now, expected, writes):
        pk = "USER#" + owner
        audit_key = ("operations", pk, "AUDIT_SOURCE#" + event["id"])
        audit_source = self.store.get(audit_key)
        expected[audit_key] = audit_source
        review_key = ("history", pk, "P#" + event["participationId"] + "#REVIEW")
        review = self.store.get(review_key)
        expected[review_key] = review
        if not review and not audit_source:
            raise Problem(409, "AUDIT_SOURCE_UNAVAILABLE")
        lake_key = ("operations", pk, "LAKE#" + event["id"])
        lake = self.store.get(lake_key)
        expected[lake_key] = lake
        payload = {
            "eventId": event["id"],
            "participationId": event["participationId"],
            "occurredAt": event["occurredAt"],
            "expiresAt": stamp(
                datetime.fromisoformat(event["occurredAt"].replace("Z", "+00:00"))
                + timedelta(days=60)
            ),
            **(
                {
                    "before": deepcopy(audit_source["before"]),
                    "after": deepcopy(audit_source["after"]),
                }
                if audit_source
                else {
                    "after": {
                        "ratings": deepcopy(review["ratings"]),
                        **({"comment": review["comment"]} if "comment" in review else {}),
                    }
                }
            ),
        }
        record = payload
        if self.audit_sink is not None:
            # Comments stay only in the object; the row is the locator erasure needs to find it.
            record = {
                "eventId": event["id"],
                "occurredAt": event["occurredAt"],
                "expiresAt": payload["expiresAt"],
                "objectKey": self.audit_sink.put(event["id"], event["occurredAt"], payload),
            }
        if lake and {k: v for k, v in lake.items() if k != "_rev"} != record:
            raise Problem(409, "AUDIT_COLLISION")
        writes[lake_key] = record
        if audit_source:
            writes[audit_key] = None
