"""Owned participation drafts and atomic completion source records."""

import hashlib
import json
from datetime import date
from uuid import uuid4
from zoneinfo import ZoneInfo

from cryptography.fernet import Fernet, InvalidToken

from .service import Problem, stamp


class ParticipationService:
    def __init__(self, identity, catalog, cursor_key):
        self.identity, self.catalog = identity, catalog
        self.store = identity.store
        self.cipher = Fernet(cursor_key)

    @staticmethod
    def projection(item):
        return {
            key: item[key]
            for key in (
                "id",
                "editionId",
                "distanceId",
                "state",
                "version",
                "timeSeconds",
                "placement",
                "bibNumber",
                "showTime",
                "showPlacement",
                "completedAt",
                "medalImageReference",
                "publishToFeed",
            )
            if key in item
        }

    def _catalog_guard(self, read, edition_id, expected_catalog_version):
        head = read(("catalog", "EDITION#" + edition_id, "HEAD"))
        if (
            not head
            or head.get("publicationState") != "approved"
            or head.get("archived")
            or head.get("version") != expected_catalog_version
        ):
            raise Problem(409, "EDITION_CHANGED")

    def create(self, actor, key, payload):
        observed = self.catalog.require_draftable(
            actor, payload["editionId"], payload["distanceId"]
        )
        pk = "USER#" + actor.subject

        def work(read, write, account, now, replay):
            self._catalog_guard(read, payload["editionId"], observed["version"])
            claim_key = ("history", pk, "EDITION#" + payload["editionId"] + "#CLAIM")
            claim = read(claim_key)
            if replay is not None:
                item = read(("history", pk, "P#" + replay["id"] + "#PART"))
                if not item:
                    raise Problem(404, "PARTICIPATION_NOT_FOUND")
                return self.projection(item), replay
            if claim:
                raise Problem(409, "PARTICIPATION_EXISTS")
            participation_id = str(uuid4())
            part_key = ("history", pk, "P#" + participation_id + "#PART")
            owner_key = ("history", "PARTICIPATION#" + participation_id, "OWNER")
            item = {
                "id": participation_id,
                "owner": actor.subject,
                "editionId": payload["editionId"],
                "distanceId": payload["distanceId"],
                "catalogVersion": observed["version"],
                "state": "draft",
                "version": 1,
                "showTime": True,
                "showPlacement": True,
                "createdAt": stamp(now),
                "updatedAt": stamp(now),
            }
            for field in ("timeSeconds", "placement", "bibNumber"):
                if payload.get(field) is not None:
                    item[field] = payload[field]
            write(part_key, item)
            write(owner_key, {"owner": actor.subject})
            write(claim_key, {"participationId": participation_id, "version": 1})
            receipt = {"id": participation_id}
            return self.projection(item), receipt

        return self.identity.transact(
            actor, "createParticipationDraft", key, payload, work, admitted=True
        )

    def get(self, actor, participation_id):
        def work(read, write, account, now, replay):
            owner = read(("history", "PARTICIPATION#" + participation_id, "OWNER"))
            if not owner or owner.get("owner") != actor.subject:
                raise Problem(404, "PARTICIPATION_NOT_FOUND")
            item = read(("history", "USER#" + actor.subject, "P#" + participation_id + "#PART"))
            if not item or item.get("state") not in {"draft", "completed"}:
                raise Problem(404, "PARTICIPATION_NOT_FOUND")
            return self.projection(item), {}

        return self.identity.transact(actor, "getParticipation", None, {}, work, admitted=True)

    def complete(self, actor, participation_id, key, payload):
        pk = "USER#" + actor.subject

        def work(read, write, account, now, replay):
            part_key = ("history", pk, "P#" + participation_id + "#PART")
            item = read(part_key)
            owner = read(("history", "PARTICIPATION#" + participation_id, "OWNER"))
            if not item or not owner or owner.get("owner") != actor.subject:
                raise Problem(404, "PARTICIPATION_NOT_FOUND")
            if replay is not None:
                if item.get("state") != "completed":
                    raise Problem(503, "PARTICIPATION_INTEGRITY_FAILURE")
                return self.projection(item), replay
            if item.get("state") != "draft":
                raise Problem(409, "PARTICIPATION_NOT_DRAFT")
            if item["version"] != payload["expectedVersion"]:
                raise Problem(409, "VERSION_CONFLICT")
            self._catalog_guard(read, item["editionId"], item["catalogVersion"])
            manifest_key = (
                "catalog",
                "EDITION#" + item["editionId"],
                "V#" + str(item["catalogVersion"]),
            )
            manifest = read(manifest_key)
            if not manifest:
                raise Problem(503, "CATALOG_INTEGRITY_FAILURE")
            edition = manifest["edition"]
            today = now.astimezone(ZoneInfo("America/Sao_Paulo")).date()
            if date.fromisoformat(edition["date"]) > today:
                raise Problem(409, "EDITION_NOT_COMPLETABLE")
            distance = next(
                (d for d in edition["distances"] if d["id"] == item["distanceId"]), None
            )
            if distance is None:
                raise Problem(409, "EDITION_CHANGED")
            reference = payload["medalImageReference"]
            image_key = ("operations", pk, "IMAGE#" + reference)
            image = read(image_key)
            origin = "runner"
            if not image:
                official = distance.get("medalImageReference") or edition.get("medalImageReference")
                if official != reference:
                    raise Problem(422, "IMAGE_NOT_VALID")
                image_key = (
                    "operations",
                    "EDITION#" + item["editionId"],
                    "IMAGE#" + reference,
                )
                image = read(image_key)
                origin = "official"
            if not image or image.get("state") != "valid":
                raise Problem(422, "IMAGE_NOT_VALID")
            if origin == "runner" and (
                image.get("owner") != actor.subject or image.get("origin") != "runner"
            ):
                raise Problem(422, "IMAGE_NOT_VALID")
            if origin == "official" and image.get("origin") != "admin":
                raise Problem(422, "IMAGE_NOT_VALID")
            review_key = ("history", pk, "P#" + participation_id + "#REVIEW")
            medal_key = ("history", pk, "P#" + participation_id + "#MEDAL")
            if read(review_key) or read(medal_key):
                raise Problem(503, "PARTICIPATION_INTEGRITY_FAILURE")
            claim_key = ("history", pk, "EDITION#" + item["editionId"] + "#CLAIM")
            claim = read(claim_key)
            if not claim or claim.get("participationId") != participation_id:
                raise Problem(503, "PARTICIPATION_INTEGRITY_FAILURE")
            event_id = str(uuid4())
            event_key = ("operations", pk, "EVENT#" + event_id)
            read(event_key)
            item.update(
                state="completed",
                version=item["version"] + 1,
                completedAt=stamp(now),
                updatedAt=stamp(now),
                medalImageReference=reference,
                publishToFeed=payload["publishToFeed"],
            )
            review = {
                "participationId": participation_id,
                "reviewVersion": 1,
                "effectVersion": 1,
                "ratings": payload["ratings"],
                "moderationState": "valid",
                "editionId": item["editionId"],
                "distanceId": item["distanceId"],
            }
            if payload.get("comment") is not None:
                review["comment"] = payload["comment"]
            medal = {
                "participationId": participation_id,
                "imageReference": reference,
                "imageOrigin": origin,
                "catalogVersion": item["catalogVersion"],
            }
            event = {
                "id": event_id,
                "type": "participation_completed",
                "state": "pending",
                "participationId": participation_id,
                "effectVersion": 1,
                "editionId": item["editionId"],
                "distanceId": item["distanceId"],
                "ratings": payload["ratings"],
                "occurredAt": stamp(now),
            }
            write(part_key, item)
            write(review_key, review)
            write(medal_key, medal)
            write(event_key, event)
            write(image_key, {**image, "refs": image.get("refs", 0) + 1})
            write(claim_key, {"participationId": participation_id, "version": item["version"]})
            return self.projection(item), {"id": participation_id}

        return self.identity.transact(
            actor, "completeParticipation", key, payload, work, admitted=True
        )

    def patch(self, actor, participation_id, key, payload):
        current = self.get(actor, participation_id)
        edition_id = payload.get("editionId", current["editionId"])
        distance_id = payload.get("distanceId", current["distanceId"])
        observed = self.catalog.require_draftable(actor, edition_id, distance_id)
        pk = "USER#" + actor.subject

        def work(read, write, account, now, replay):
            part_key = ("history", pk, "P#" + participation_id + "#PART")
            item = read(part_key)
            owner = read(("history", "PARTICIPATION#" + participation_id, "OWNER"))
            if not item or not owner or owner.get("owner") != actor.subject:
                raise Problem(404, "PARTICIPATION_NOT_FOUND")
            if replay is not None:
                return self.projection(item), replay
            if item.get("state") != "draft":
                raise Problem(409, "PARTICIPATION_NOT_DRAFT")
            if item["version"] != payload["expectedVersion"]:
                raise Problem(409, "VERSION_CONFLICT")
            self._catalog_guard(read, edition_id, observed["version"])
            old_edition = item["editionId"]
            if edition_id != old_edition:
                new_claim = ("history", pk, "EDITION#" + edition_id + "#CLAIM")
                if read(new_claim):
                    raise Problem(409, "PARTICIPATION_EXISTS")
                old_claim = ("history", pk, "EDITION#" + old_edition + "#CLAIM")
                existing = read(old_claim)
                if not existing or existing.get("participationId") != participation_id:
                    raise Problem(503, "PARTICIPATION_INTEGRITY_FAILURE")
                write(old_claim, None)
                write(
                    new_claim, {"participationId": participation_id, "version": item["version"] + 1}
                )
            else:
                claim_key = ("history", pk, "EDITION#" + old_edition + "#CLAIM")
                existing = read(claim_key)
                if not existing or existing.get("participationId") != participation_id:
                    raise Problem(503, "PARTICIPATION_INTEGRITY_FAILURE")
                write(
                    claim_key,
                    {"participationId": participation_id, "version": item["version"] + 1},
                )
            for field in (
                "editionId",
                "distanceId",
                "timeSeconds",
                "placement",
                "bibNumber",
                "showTime",
                "showPlacement",
            ):
                if field not in payload:
                    continue
                if payload[field] is None:
                    item.pop(field, None)
                else:
                    item[field] = payload[field]
            item["catalogVersion"] = observed["version"]
            item["version"] += 1
            item["updatedAt"] = stamp(now)
            write(part_key, item)
            return self.projection(item), {"id": participation_id}

        return self.identity.transact(
            actor, "patchParticipation", key, payload, work, admitted=True
        )

    def _binding(self, actor, state, limit):
        return hashlib.sha256(
            json.dumps(
                {
                    "actor": actor.subject,
                    "env": self.identity.environment,
                    "state": state,
                    "limit": limit,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()

    def list(self, actor, state, limit, cursor):
        self.identity.authorize(actor, admitted=True)
        after = None
        if cursor:
            try:
                data = json.loads(self.cipher.decrypt(cursor.encode(), ttl=899))
                if data["binding"] != self._binding(actor, state, limit):
                    raise ValueError()
                after = data["after"]
            except (InvalidToken, ValueError, KeyError, TypeError) as error:
                raise Problem(422, "INVALID_CURSOR") from error
        rows, next_key = self.store.query(
            "history", "USER#" + actor.subject, prefix="P#", after=after, limit=limit
        )
        items = [
            self.projection(item)
            for sk, item in rows
            if sk.endswith("#PART") and (state is None or item.get("state") == state)
        ]
        self.identity.authorize(actor, admitted=True)
        result = {"items": items}
        if next_key:
            result["nextCursor"] = self.cipher.encrypt(
                json.dumps(
                    {"binding": self._binding(actor, state, limit), "after": next_key}
                ).encode()
            ).decode()
        return result
