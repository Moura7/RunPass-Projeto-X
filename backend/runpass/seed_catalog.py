"""Review synthetic catalog locally. Never creates an AWS client or a persistent user."""

import json
from pathlib import Path

from cryptography.fernet import Fernet

from .catalog import CatalogFilters, CatalogService, seed_synthetic
from .identity import Principal
from .service import IdentityService
from .store import MemoryStore


def main():
    identity = IdentityService(MemoryStore(), b"synthetic-demo-local-key-not-real!")
    catalog = CatalogService(identity, Fernet.generate_key())
    fixture = Path(__file__).resolve().parents[1] / "fixtures/catalog.synthetic.json"
    count = seed_synthetic(catalog, fixture)
    seed_synthetic(catalog, fixture)
    actor = Principal("synthetic-seed", True)
    identity.create_profile(
        actor, "profile", {"displayName": "Sintético", "username": "synthetic_seed"}
    )
    identity.admit(actor, "admit", {"birthDate": "1990-01-01", "declaresAdult": True})
    print(
        json.dumps(
            {
                "environment": "local-memory",
                "synthetic": True,
                "editions": count,
                "ids": [e["id"] for e in catalog.list(actor, CatalogFilters())["items"]],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
