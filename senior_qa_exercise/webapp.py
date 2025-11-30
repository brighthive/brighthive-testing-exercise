"""
BrightHive Data Workspace - Web Application
===========================================

This web application simulates a data workspace management system.
It contains several intentional bugs that candidates must identify, document, and test.

WARNING: This application contains intentional bugs for testing purposes.
Do not use in production!
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BrightHive Data Workspace API",
    version="1.0.0",
    description="A data workspace management system API for QA automation testing"
)
security = HTTPBearer()

# In-memory storage (simulating database)
users_db: Dict[str, Dict] = {}
workspaces_db: Dict[str, Dict] = {}
datasets_db: Dict[str, Dict] = {}

# Authentication tokens (simplified)
valid_tokens: Set[str] = set()


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class WorkspaceStatus(str, Enum):
    """Workspace status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class UserCreate(BaseModel):
    """User creation model."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER
    password: str = Field(..., min_length=8)

    @validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        # BUG #1: Missing password complexity validation
        # Should check for uppercase, lowercase, numbers, special chars
        return v


class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    name: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None


class WorkspaceCreate(BaseModel):
    """Workspace creation model."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    owner_email: EmailStr


class WorkspaceResponse(BaseModel):
    """Workspace response model."""
    id: str
    name: str
    description: Optional[str]
    owner_email: str
    status: WorkspaceStatus
    created_at: datetime
    member_count: int


class DatasetCreate(BaseModel):
    """Dataset creation model."""
    name: str = Field(..., min_length=1, max_length=200)
    workspace_id: str
    data_schema: Optional[Dict] = None
    row_count: Optional[int] = Field(None, ge=0)


class DatasetResponse(BaseModel):
    """Dataset response model."""
    id: str
    name: str
    workspace_id: str
    data_schema: Optional[Dict]
    row_count: Optional[int]
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    token: str
    user: UserResponse
    expires_at: datetime


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    # BUG #2: Using SHA256 for password hashing (should use bcrypt/argon2)
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == hashed


def generate_token() -> str:
    """Generate authentication token."""
    return secrets.token_urlsafe(32)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current authenticated user."""
    token = credentials.credentials

    # BUG #3: Token validation doesn't check expiration
    if token not in valid_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    # Find user by token (simplified)
    for user_id, user_data in users_db.items():
        if user_data.get("token") == token:
            return user_data

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found"
    )


@app.post("/api/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate) -> UserResponse:
    """
    Register a new user.

    Creates a new user account with the provided email, name, password, and role.
    Returns the created user information upon successful registration.
    """
    # Check if user already exists
    user_id = hash_password(user.email)  # Using hash as ID (not ideal)

    if user_id in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create user
    user_data = {
        "id": user_id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "password_hash": hash_password(user.password),
        "created_at": datetime.utcnow(),
        "last_login": None,
        "token": None
    }

    users_db[user_id] = user_data

    logger.info(f"User registered: {user.email}")

    return UserResponse(
        id=user_data["id"],
        email=user_data["email"],
        name=user_data["name"],
        role=user_data["role"],
        created_at=user_data["created_at"],
        last_login=user_data["last_login"]
    )


@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest) -> LoginResponse:
    """
    Authenticate user and return token.

    Validates user credentials and returns an authentication token along with
    user information and token expiration time.
    """
    # Find user by email
    user_id = None
    user_data = None

    for uid, udata in users_db.items():
        if udata["email"] == login_data.email:
            user_id = uid
            user_data = udata
            break

    if not user_data:
        # BUG #6: Information disclosure - reveals user existence
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(login_data.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate token
    token = generate_token()
    valid_tokens.add(token)
    user_data["token"] = token
    user_data["last_login"] = datetime.utcnow()

    expires_at = datetime.utcnow() + timedelta(hours=24)

    return LoginResponse(
        token=token,
        user=UserResponse(
            id=user_data["id"],
            email=user_data["email"],
            name=user_data["name"],
            role=user_data["role"],
            created_at=user_data["created_at"],
            last_login=user_data["last_login"]
        ),
        expires_at=expires_at
    )


@app.post("/api/v1/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace: WorkspaceCreate,
    current_user: Dict = Depends(get_current_user)
) -> WorkspaceResponse:
    """
    Create a new workspace.

    Creates a new workspace with the specified name, description, and owner.
    The authenticated user is automatically added as a member.
    """
    workspace_id = secrets.token_urlsafe(16)

    # Check if workspace name already exists
    for ws_id, ws_data in workspaces_db.items():
        if ws_data["name"] == workspace.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workspace with this name already exists"
            )

    workspace_data = {
        "id": workspace_id,
        "name": workspace.name,
        "description": workspace.description,
        "owner_email": workspace.owner_email,
        "status": WorkspaceStatus.ACTIVE,
        "created_at": datetime.utcnow(),
        "members": {current_user["email"]}  # Add creator as member
    }

    workspaces_db[workspace_id] = workspace_data

    logger.info(f"Workspace created: {workspace.name} by {current_user['email']}")

    return WorkspaceResponse(
        id=workspace_data["id"],
        name=workspace_data["name"],
        description=workspace_data["description"],
        owner_email=workspace_data["owner_email"],
        status=workspace_data["status"],
        created_at=workspace_data["created_at"],
        member_count=len(workspace_data["members"])
    )


@app.get("/api/v1/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    current_user: Dict = Depends(get_current_user)
) -> WorkspaceResponse:
    """
    Get workspace details.

    Retrieves detailed information about a workspace including its name,
    description, owner, status, creation date, and member count.
    """
    if workspace_id not in workspaces_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    workspace_data = workspaces_db[workspace_id]

    return WorkspaceResponse(
        id=workspace_data["id"],
        name=workspace_data["name"],
        description=workspace_data["description"],
        owner_email=workspace_data["owner_email"],
        status=workspace_data["status"],
        created_at=workspace_data["created_at"],
        member_count=len(workspace_data["members"])
    )


@app.post("/api/v1/workspaces/{workspace_id}/datasets", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    workspace_id: str,
    dataset: DatasetCreate,
    current_user: Dict = Depends(get_current_user)
) -> DatasetResponse:
    """
    Create a dataset in a workspace.

    Creates a new dataset within the specified workspace. The dataset can include
    an optional schema definition and row count.
    """
    dataset_id = secrets.token_urlsafe(16)

    # Check if dataset name already exists in workspace
    for ds_id, ds_data in datasets_db.items():
        if ds_data["name"] == dataset.name and ds_data["workspace_id"] == workspace_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dataset with this name already exists in workspace"
            )

    now = datetime.utcnow()
    dataset_data = {
        "id": dataset_id,
        "name": dataset.name,
        "workspace_id": workspace_id,
        "data_schema": dataset.data_schema,
        "row_count": dataset.row_count,
        "created_at": now,
        "updated_at": now
    }

    datasets_db[dataset_id] = dataset_data

    logger.info(f"Dataset created: {dataset.name} in workspace {workspace_id}")

    return DatasetResponse(
        id=dataset_data["id"],
        name=dataset_data["name"],
        workspace_id=dataset_data["workspace_id"],
        data_schema=dataset_data["data_schema"],
        row_count=dataset_data["row_count"],
        created_at=dataset_data["created_at"],
        updated_at=dataset_data["updated_at"]
    )


@app.get("/api/v1/workspaces/{workspace_id}/datasets", response_model=List[DatasetResponse])
async def list_datasets(
    workspace_id: str,
    current_user: Dict = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
) -> List[DatasetResponse]:
    """
    List datasets in a workspace.

    Retrieves a paginated list of datasets within the specified workspace.
    Supports limit and offset parameters for pagination.
    """
    datasets = [
        DatasetResponse(
            id=ds_data["id"],
            name=ds_data["name"],
            workspace_id=ds_data["workspace_id"],
            data_schema=ds_data["data_schema"],
            row_count=ds_data["row_count"],
            created_at=ds_data["created_at"],
            updated_at=ds_data["updated_at"]
        )
        for ds_id, ds_data in datasets_db.items()
        if ds_data["workspace_id"] == workspace_id
    ]

    # BUG #16: Pagination logic doesn't handle edge cases properly
    return datasets[offset:offset + limit]


@app.delete("/api/v1/workspaces/{workspace_id}")
async def delete_workspace(
    workspace_id: str,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Delete a workspace.

    Permanently deletes the specified workspace and all associated data.
    This action cannot be undone.
    """
    if workspace_id not in workspaces_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    workspace_name = workspaces_db[workspace_id]["name"]
    del workspaces_db[workspace_id]

    logger.info(f"Workspace deleted: {workspace_name} by {current_user['email']}")

    return {"message": f"Workspace {workspace_name} deleted successfully"}


@app.get("/api/v1/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)) -> UserResponse:
    """Get current user information."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        role=current_user["role"],
        created_at=current_user["created_at"],
        last_login=current_user["last_login"]
    )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
