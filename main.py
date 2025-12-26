from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

AUTHZ_ACL = "acl"
AUTHZ_RBAC = "rbac"
AUTHZ_ABAC = "abac"
AUTHZ_REBAC = "rebac"
AUTHZ_PBAC = "pbac"

AUTHZ_METHODS = [AUTHZ_ACL, AUTHZ_RBAC, AUTHZ_ABAC, AUTHZ_REBAC, AUTHZ_PBAC]

USERS = {
    1: {
        "name": "Avery Chen",
    },
    2: {
        "name": "Jordan Malik",
    },
    3: {
        "name": "Riley Nguyen",
    },
    4: {
        "name": "Morgan Patel",
    },
    5: {
        "name": "Taylor Brooks",
    },
}

DOCUMENTS = {
    1: {"title": "Document 1", "content": "Content of document 1."},
    2: {"title": "Document 2", "content": "Content of document 2."},
    3: {"title": "Document 3", "content": "Content of document 3."},
}


@app.get("/documents/{id}")
async def read_document(
    id: int, authz_method: str, authorization: Annotated[str | None, Header()] = None
):
    if authz_method not in AUTHZ_METHODS:
        return {
            "error": "Invalid authorization method",
            "suggestion": "Choose from: " + ", ".join(AUTHZ_METHODS),
        }

    if authorization is None:
        return {
            "error": "Authorization header missing",
            "suggestion": "Provide a valid authorization token",
        }

    user_id = int(authorization.split(" ")[1])

    match authz_method:
        case "acl":
            return await fetch_document_using_acls(user_id, id)
        case "rbac":
            # Placeholder for RBAC authorization logic
            pass
        case "abac":
            # Placeholder for ABAC authorization logic
            pass
        case "rebac":
            # Placeholder for ReBAC authorization logic
            pass
        case "pbac":
            # Placeholder for PBAC authorization logic
            pass

    return {
        "error": "Invalid authorization method",
        "suggestion": "Choose from: " + ", ".join(AUTHZ_METHODS),
    }


# ACLs
ACLs = {
    1: {1: ["read", "write"], 2: ["read"]},  # User 1 permissions
    2: {2: ["read", "write"], 3: ["read"]},  # User 2 permissions
    3: {1: ["read"], 3: ["read", "write"]},  # User 3 permissions
}


async def check_acl(user_id: int, document_id: int, action: str) -> bool:
    user_acls = ACLs.get(user_id, {})
    document_permissions = user_acls.get(document_id, [])
    return action in document_permissions


async def fetch_document_using_acls(user_id: int, document_id: int):
    if await check_acl(user_id, document_id, "read"):
        return DOCUMENTS.get(document_id, {"error": "Document not found"})
    else:
        return {"error": "Access denied"}
