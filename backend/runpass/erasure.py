"""Retriable local account erasure executor; real scheduling and restore proof belong to S09."""

from copy import deepcopy

from .service import Problem, stamp
from .store import Conflict


class ErasureProcessor:
    def __init__(self, identity):
        self.identity, self.store = identity, identity.store

    def step(self, owner, operation_id, limit=50):
        pk = "USER#" + owner
        job_key = ("operations", pk, "JOB#" + operation_id)
        job = self.store.get(job_key)
        if not job or job.get("type") != "erase_account":
            raise Problem(404, "ERASURE_JOB_NOT_FOUND")
        if job["state"] == "completed":
            return {"state": "completed"}
        if job.get("stage") == "compensate":
            rows, _ = self.store.query("projections", pk, prefix="CONTRIBUTION#", limit=limit)
            if rows:
                for sk, contribution in rows:
                    self._remove_contribution(pk, sk, contribution)
                return {"state": "pending", "stage": "compensate"}
            self._update_job(job_key, job, "erase")
            return {"state": "pending", "stage": "erase"}
        return self._erase(owner, job_key, job, limit)

    def _remove_contribution(self, pk, sk, contribution):
        contribution_key = ("projections", pk, sk)
        score_key = (
            "projections",
            "EDITION#" + contribution["editionId"],
            "SCORE#current",
        )
        for _ in range(20):
            current = self.store.get(contribution_key)
            if not current:
                return
            score = self.store.get(score_key)
            updated = deepcopy(score) if score else {"ratingSum": 0, "reviewCount": 0}
            updated["ratingSum"] -= current["ratingSum"]
            updated["reviewCount"] -= 1
            try:
                self.store.commit(
                    {contribution_key: current, score_key: score},
                    {contribution_key: None, score_key: updated},
                )
                return
            except Conflict:
                continue
        raise Problem(503, "CONCURRENT_RETRY_REQUIRED")

    def _update_job(self, key, job, stage):
        updated = {**job, "stage": stage, "updatedAt": stamp(self.identity.clock())}
        try:
            self.store.commit({key: job}, {key: updated})
        except Conflict as error:
            raise Problem(503, "CONCURRENT_RETRY_REQUIRED") from error

    def _erase(self, owner, job_key, job, limit):
        pk = "USER#" + owner
        candidates = []
        for table in ("identity", "history", "operations", "projections"):
            rows, _ = self.store.query(table, pk, limit=limit)
            for sk, item in rows:
                key = (table, pk, sk)
                if key == job_key:
                    continue
                candidates.append((key, item))
                if len(candidates) >= limit:
                    break
            if len(candidates) >= limit:
                break
        if len(candidates) < limit:
            for shard in range(16):
                rows, _ = self.store.query(
                    "operations", f"WORK#event#pending#{shard:02d}", limit=limit
                )
                for sk, item in rows:
                    if item.get("owner") == owner:
                        candidates.append(
                            (("operations", f"WORK#event#pending#{shard:02d}", sk), item)
                        )
                        if len(candidates) >= limit:
                            break
                if len(candidates) >= limit:
                    break
        if candidates:
            expected = {key: item for key, item in candidates}
            writes = {key: None for key, _ in candidates}
            for key, item in candidates:
                if key[0] == "history" and key[2].endswith("#PART") and item.get("id"):
                    reverse = ("history", "PARTICIPATION#" + item["id"], "OWNER")
                    expected[reverse] = self.store.get(reverse)
                    writes[reverse] = None
            try:
                self.store.commit(expected, writes)
            except Conflict as error:
                raise Problem(503, "CONCURRENT_RETRY_REQUIRED") from error
            return {"state": "pending", "stage": "erase"}

        work_key = ("operations", job["workPK"], job["workSK"])
        username_key = (
            ("identity", "USERNAME#" + job["username"], "CLAIM") if job.get("username") else None
        )
        keys = [job_key, work_key]
        if username_key:
            keys.append(username_key)
        expected = {key: self.store.get(key) for key in keys}
        writes = {key: None for key in keys}
        try:
            self.store.commit(expected, writes)
        except Conflict as error:
            raise Problem(503, "CONCURRENT_RETRY_REQUIRED") from error
        return {"state": "completed"}
