"""
# Authorization Methods

This example works through five different ways to authorize users to take actions on resources in an API.
They methods of authorization start simple and get more complex as we go on.
"""

from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

"""
## Authorization Methods

- ACL (Access Control Lists): Permissions are assigned directly to users for specific resources.
- RBAC (Role-Based Access Control): Permissions are assigned to roles, and users are assigned to roles.
- ABAC (Attribute-Based Access Control): Access is granted based on attributes of users, resources, and the environment.
- ReBAC (Relationship-Based Access Control): Access is determined based on relationships between users and resources.
- PBAC (Policy-Based Access Control): Access is governed by policies that define rules for access based on various conditions.
"""

AUTHZ_ACL = "acl"
AUTHZ_RBAC = "rbac"
AUTHZ_ABAC = "abac"
AUTHZ_REBAC = "rebac"
AUTHZ_PBAC = "pbac"

AUTHZ_METHODS = [AUTHZ_ACL, AUTHZ_RBAC, AUTHZ_ABAC, AUTHZ_REBAC, AUTHZ_PBAC]

"""
## Sample Data

To demonstrate the different methods of authorization, we'll take a look at a document management system for Cola Co.
Cola Co has five defined users: Avery, Jordan, Riley, Morgan, and Taylor.

Avery is the senior engineer in the engineering department and has admin access.
Jordan runs the marketing department. 
Riley is a sales associate. 
Morgan works in HR. 
Taylor is an engineering intern.

We define these users below with their given departments, titles, and roles.
"""

USERS = {
    1: {
        "name": "Avery Chen",
        "dept": "Engineering",
        "title": "senior engineer",
        "role": "admin",
    },
    2: {
        "name": "Jordan Malik",
        "dept": "Marketing",
        "title": "marketing manager",
        "role": "editor",
    },
    3: {
        "name": "Riley Nguyen",
        "dept": "Sales",
        "title": "sales associate",
        "role": "viewer",
    },
    4: {
        "name": "Morgan Patel",
        "dept": "HR",
        "title": "HR specialist",
        "role": "editor",
    },
    5: {
        "name": "Taylor Brooks",
        "dept": "engineering",
        "title": "intern",
        "role": "viewer",
    },
}

"""
The crew at Cola Co have created a few documents that they work on collaboratively. 

Morgan, the head of HR, has written a document called "How to Behave Like an Adult at Work". The document does not have any other collaborators. 

Avery is working on a document called "Top Secret Next Generation AI Application".


"""

DOCUMENTS = {
    1: {
        "title": "How to Behave Like an Adult at Work",
        "author_id": 4,
        "collaborator_ids": [],
        "content": "Be kind to others. Respect their time and opinions. Communicate clearly. Stay organized. Take responsibility for your actions.",
    },
    2: {
        "title": "Top Secret Next Generation AI Application",
        "author_id": 1,
        "collaborator_ids": [5],
        "content": "This is a super neat idea for an AI application that will change the world. It involves advanced machine learning techniques and cutting-edge algorithms. The details are classified. Handle with care. My plan is to have a soda machine that prompts the user with 20 yes/no questions and then dispenses a soda based on the answers.",
    },
    3: {
        "title": "What I Did This Summer at Cola Co",
        "author_id": 5,
        "collaborator_ids": [1, 2, 4],
        "content": "Hi, my name is Taylor. This Summer, I worked at Cola Co as an engineering intern. I learned a lot about the beverage industry and got to work on some cool projects. I also made some great friends and had a lot of fun.",
    },
}

"""
## API Endpoints

To create, read, update, and delete documents, we'll add the following endpoints:
- POST /documents
- GET /documents/{id}
- PATCH /documents/{id}
- DELETE /documents/{id}
"""


@app.post("/documents")
async def create_document(
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
            return {"message": "Document created using ACLs"}
        case "rbac":
            return {"message": "Document created using RBAC"}
        case "abac":
            return {"message": "Document created using ABAC"}
        case "rebac":
            return {"message": "Document created using ReBAC"}
        case "pbac":
            return {"message": "Document created using PBAC"}

    return {
        "error": "Invalid authorization method",
        "suggestion": "Choose from: " + ", ".join(AUTHZ_METHODS),
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
            return await fetch_document_using_rbac(user_id, id)
        case "abac":
            return await fetch_document_using_abac(user_id, id)
        case "rebac":
            return await fetch_document_using_rebac(user_id, id)
        case "pbac":
            return await fetch_document_using_pbac(user_id, id)

    return {
        "error": "Invalid authorization method",
        "suggestion": "Choose from: " + ", ".join(AUTHZ_METHODS),
    }


@app.patch("/documents/{id}")
async def update_document(
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
            return {"message": "Document updated using ACLs"}
        case "rbac":
            return {"message": "Document updated using RBAC"}
        case "abac":
            return {"message": "Document updated using ABAC"}
        case "rebac":
            return {"message": "Document updated using ReBAC"}
        case "pbac":
            return {"message": "Document updated using PBAC"}

    return {
        "error": "Invalid authorization method",
        "suggestion": "Choose from: " + ", ".join(AUTHZ_METHODS),
    }


@app.delete("/documents/{id}")
async def delete_document(
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
            return {"message": "Document deleted using ACLs"}
        case "rbac":
            return {"message": "Document deleted using RBAC"}
        case "abac":
            return {"message": "Document deleted using ABAC"}
        case "rebac":
            return {"message": "Document deleted using ReBAC"}
        case "pbac":
            return {"message": "Document deleted using PBAC"}

    return {
        "error": "Invalid authorization method",
        "suggestion": "Choose from: " + ", ".join(AUTHZ_METHODS),
    }


"""
## Authorization Implementations

### ACLs (Access Control Lists)
"""

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


"""
### RBAC (Role-Based Access Control)
"""

ROLES = {
    1: "admin",
    2: "editor",
    3: "viewer",
}

USER_ROLES = {
    1: [1],  # User 1 is an admin
    2: [2],  # User 2 is an editor
    3: [3],  # User 3 is a viewer
}

ROLE_PERMISSIONS = {
    "admin": {1: ["read", "write"], 2: ["read", "write"], 3: ["read", "write"]},
    "editor": {1: ["read", "write"], 2: ["read", "write"], 3: ["read"]},
    "viewer": {1: ["read"], 2: ["read"], 3: ["read"]},
}


async def check_rbac(user_id: int, document_id: int, action: str) -> bool:
    roles = USER_ROLES.get(user_id, [])
    for role_id in roles:
        role_name = ROLES.get(role_id)
        if role_name:
            permissions = ROLE_PERMISSIONS.get(role_name, {})
            document_permissions = permissions.get(document_id, [])
            if action in document_permissions:
                return True
    return False


async def fetch_document_using_rbac(user_id: int, document_id: int):
    if await check_rbac(user_id, document_id, "read"):
        return DOCUMENTS.get(document_id, {"error": "Document not found"})
    else:
        return {"error": "Access denied"}


"""
### ABAC (Attribute-Based Access Control)
"""


async def fetch_document_using_abac(user_id: int, document_id: int):
    # Placeholder for ABAC authorization logic
    pass


"""
### ReBAC (Relationship-Based Access Control)
"""


async def fetch_document_using_rebac(user_id: int, document_id: int):
    # Placeholder for ReBAC authorization logic
    pass


"""
### PBAC (Policy-Based Access Control)
"""


async def fetch_document_using_pbac(user_id: int, document_id: int):
    # Placeholder for PBAC authorization logic
    pass
