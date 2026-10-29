"""Trusted operator login. Expose only to a restricted infrastructure component, never HTTP."""

import hashlib
import time

from .identity import AuthFailure


def establish_session(
    client, client_id, verifier, store, username, password, totp, clock=time.time
):
    initial = client.initiate_auth(
        ClientId=client_id,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )
    # Tokens issued during onboarding, remembered-device flows or refresh are not MFA evidence.
    if initial.get("ChallengeName") != "SOFTWARE_TOKEN_MFA" or not initial.get("Session"):
        raise AuthFailure()
    final = client.respond_to_auth_challenge(
        ClientId=client_id,
        ChallengeName="SOFTWARE_TOKEN_MFA",
        Session=initial["Session"],
        ChallengeResponses={"USERNAME": username, "SOFTWARE_TOKEN_MFA_CODE": totp},
    )
    token = final.get("AuthenticationResult", {}).get("AccessToken")
    if not token or final.get("ChallengeName"):
        raise AuthFailure()
    actor = verifier(token)
    if actor.audience != "operator":
        raise AuthFailure()
    # Verification above is authoritative; decode is used only to read its verified expiry.
    import jwt

    claims = jwt.decode(token, options={"verify_signature": False})
    now = int(clock())
    access_key = ("identity", "OPERATOR#" + actor.subject, "ACCESS")
    access = store.get(access_key)
    if not access or access.get("state") != "active":
        raise AuthFailure()
    session_key = (
        "operations",
        "OPERATOR#" + actor.subject,
        "SESSION#" + hashlib.sha256(token.encode()).hexdigest(),
    )
    old = store.get(session_key)
    session = {
        "factor": "SOFTWARE_TOKEN_MFA",
        "accessVersion": access["_rev"],
        "issuer": claims["iss"],
        "clientId": client_id,
        "verifiedAt": now,
        "expiresAt": min(claims["exp"], now + 3600),
    }
    if session["expiresAt"] <= now:
        raise AuthFailure()
    store.commit({access_key: access, session_key: old}, {session_key: session})
    return token  # caller uses it in memory; never print or log credentials/session tokens
