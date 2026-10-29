"""Explicit AWS composition, called only by a separately authorized environment entry point."""

from dataclasses import dataclass

from .api import create_app
from .catalog import CatalogService
from .identity import CognitoDirectory, CognitoVerifier, JwksProvider
from .participation import ParticipationService
from .service import IdentityService
from .store import DynamoStore
from .upload import UploadService


@dataclass(frozen=True)
class AwsSettings:
    runner_issuer: str
    runner_client_id: str
    environment: str
    identity_table: str
    operations_table: str
    erasure_table: str
    erasure_hmac_key: bytes
    catalog_table: str | None = None
    cursor_encryption_key: bytes | None = None
    history_table: str | None = None


def create_aws_app(settings: AwsSettings, dynamodb_client, cognito_client, blob_store=None):
    store = DynamoStore(
        dynamodb_client,
        {
            "identity": settings.identity_table,
            "operations": settings.operations_table,
            "erasure": settings.erasure_table,
            **({"catalog": settings.catalog_table} if settings.catalog_table else {}),
            **({"history": settings.history_table} if settings.history_table else {}),
        },
    )
    verifier = CognitoVerifier(
        settings.runner_issuer,
        settings.runner_client_id,
        JwksProvider(settings.runner_issuer),
        CognitoDirectory(cognito_client),
    )
    service = IdentityService(
        store,
        settings.erasure_hmac_key,
        environment=settings.environment,
        identity_namespace=settings.runner_issuer,
    )
    catalog = None
    participations = None
    if settings.catalog_table and settings.cursor_encryption_key:
        catalog = CatalogService(service, settings.cursor_encryption_key)
        if settings.history_table:
            participations = ParticipationService(service, catalog, settings.cursor_encryption_key)
    uploads = UploadService(service, blob_store) if blob_store is not None else None
    return create_app(service, verifier, catalog, participations, uploads)
