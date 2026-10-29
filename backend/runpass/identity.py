"""Verified Cognito identity and current operator authorization, with injected I/O."""

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone

import jwt
from botocore.exceptions import BotoCoreError, ClientError

from .store import Unavailable


class AuthFailure(Exception):
    pass


@dataclass(frozen=True)
class Principal:
    subject: str
    verified_email: bool
    audience: str = "runner"
    token_digest: str = ""


class CognitoVerifier:
    def __init__(self, issuer, client_id, key_provider, directory, audience="runner"):
        self.issuer, self.client_id = issuer, client_id
        self.key_provider, self.directory, self.audience = key_provider, directory, audience

    def __call__(self, token):
        try:
            header = jwt.get_unverified_header(token)
            if header.get("alg") != "RS256" or not isinstance(header.get("kid"), str):
                raise AuthFailure()
            claims = jwt.decode(
                token,
                self.key_provider(header["kid"]),
                algorithms=["RS256"],
                issuer=self.issuer,
                options={
                    "require": ["exp", "iat", "iss", "sub", "client_id", "token_use"],
                    "verify_aud": False,
                },
            )
            if claims["token_use"] != "access" or claims["client_id"] != self.client_id:
                raise AuthFailure()
            if not isinstance(claims["sub"], str) or not claims["sub"]:
                raise AuthFailure()
            verified = self.directory(token, claims["sub"])
            return Principal(
                claims["sub"], verified, self.audience, hashlib.sha256(token.encode()).hexdigest()
            )
        except jwt.InvalidTokenError as error:
            raise AuthFailure() from error


class CognitoDirectory:
    def __init__(self, client):
        self.client = client

    def __call__(self, token, subject):
        try:
            response = self.client.get_user(AccessToken=token)
        except BotoCoreError as error:
            raise Unavailable() from error
        except ClientError as error:
            if error.response["Error"]["Code"] in (
                "NotAuthorizedException",
                "UserNotFoundException",
            ):
                raise AuthFailure() from error
            raise Unavailable() from error
        attributes = {a["Name"]: a["Value"] for a in response["UserAttributes"]}
        if attributes.get("sub") != subject:
            raise AuthFailure()
        return attributes.get("email_verified") == "true"


class JwksProvider:
    """Only the configured issuer is contacted; token-supplied jku/x5u are ignored."""

    def __init__(self, issuer):
        if not re.fullmatch(
            r"https://cognito-idp[.]sa-east-1[.]amazonaws[.]com/sa-east-1_[A-Za-z0-9]+", issuer
        ):
            raise ValueError("Expected configured Cognito issuer")
        self.client = jwt.PyJWKClient(issuer.rstrip("/") + "/.well-known/jwks.json", timeout=3)

    def __call__(self, kid):
        try:
            return self.client.get_signing_key(kid).key
        except jwt.PyJWKClientConnectionError as error:
            raise Unavailable() from error
        except jwt.PyJWKClientError as error:
            raise AuthFailure() from error


def require_operator(store, principal, permission, now=None):
    now = now or datetime.now(timezone.utc)
    if principal.audience != "operator":
        raise AuthFailure()
    access = store.get(("identity", f"OPERATOR#{principal.subject}", "ACCESS"))
    session = store.get(
        ("operations", f"OPERATOR#{principal.subject}", f"SESSION#{principal.token_digest}")
    )
    if (
        not access
        or access.get("state") != "active"
        or permission not in access.get("permissions", [])
        or not session
        or session.get("accessVersion") != access["_rev"]
        or session.get("expiresAt", 0) <= int(now.timestamp())
        or session.get("factor") != "SOFTWARE_TOKEN_MFA"
    ):
        raise AuthFailure()
    return True
