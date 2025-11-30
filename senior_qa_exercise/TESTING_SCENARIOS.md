# Testing Scenarios Guide

This document provides example testing scenarios to help guide your integration test implementation. These scenarios demonstrate the types of tests a Senior QA Engineer should create.

---

## Authentication & User Management Scenarios

### Scenario 1: User Registration Flow
```python
def test_user_registration_happy_path():
    """Test successful user registration."""
    # Test: Register a new user with valid data
    # Expected: User created successfully (201)
    # Validate: User can login after registration

def test_user_registration_duplicate_email():
    """Test that duplicate email registration fails."""
    # Test: Try to register same email twice
    # Expected: Second registration fails (400)

def test_user_registration_weak_password():
    """Test password validation."""
    # Test: Register with weak password (e.g., "12345678")
    # Expected: Should fail validation (422) OR succeed (reveals bug)
    # This test will reveal BUG #1 if password validation is weak
```

### Scenario 2: Login & Authentication Flow
```python
def test_login_successful():
    """Test successful login."""
    # Test: Login with valid credentials
    # Expected: Token returned, user info returned (200)

def test_login_invalid_credentials():
    """Test login with wrong password."""
    # Test: Login with wrong password
    # Expected: Authentication fails (401)

def test_login_nonexistent_user():
    """Test login with non-existent user."""
    # Test: Login with email that doesn't exist
    # Expected: Authentication fails (401)
    # Note: Should return same error as wrong password (security best practice)
    # This test reveals BUG #6 if errors differ

def test_token_required_for_protected_endpoints():
    """Test that protected endpoints require authentication."""
    # Test: Access protected endpoint without token
    # Expected: 403 Forbidden

def test_expired_token():
    """Test token expiration handling."""
    # Test: Use token after expiration time
    # Expected: Should fail (401) but might not (reveals BUG #3)
```

---

## Multi-User & Authorization Scenarios

### Scenario 3: Workspace Creation & Access Control
```python
def test_user_creates_own_workspace():
    """Test that user can create workspace for themselves."""
    # Setup: Login as user1@example.com
    # Test: Create workspace with owner_email=user1@example.com
    # Expected: Workspace created successfully (201)

def test_user_creates_workspace_for_other_user():
    """Test authorization - user tries to create workspace for someone else."""
    # Setup: Login as user1@example.com
    # Test: Create workspace with owner_email=user2@example.com
    # Expected: Should fail (403) OR succeed (reveals BUG #8)
    # This reveals authorization bug

def test_workspace_owner_can_view_workspace():
    """Test that workspace owner can view their workspace."""
    # Setup: user1 creates workspace
    # Test: user1 views workspace
    # Expected: Success (200)

def test_non_member_cannot_view_workspace():
    """Test that non-members cannot view workspace."""
    # Setup: user1 creates workspace, get workspace_id
    # Test: user2 (different user) tries to view workspace
    # Expected: Should fail (403) OR succeed (reveals BUG #9)
    # This reveals authorization bypass bug

def test_workspace_owner_can_delete_workspace():
    """Test that workspace owner can delete their workspace."""
    # Setup: user1 creates workspace
    # Test: user1 deletes workspace
    # Expected: Success (200)

def test_non_owner_cannot_delete_workspace():
    """Test that non-owners cannot delete workspace."""
    # Setup: user1 creates workspace
    # Test: user2 tries to delete user1's workspace
    # Expected: Should fail (403) OR succeed (reveals BUG #17)
    # This reveals critical authorization bug
```

### Scenario 4: Dataset Management & Authorization
```python
def test_workspace_member_can_create_dataset():
    """Test that workspace members can create datasets."""
    # Setup: user1 creates workspace, user1 is member
    # Test: user1 creates dataset in workspace
    # Expected: Success (201)

def test_non_member_cannot_create_dataset():
    """Test that non-members cannot create datasets."""
    # Setup: user1 creates workspace
    # Test: user2 tries to create dataset in user1's workspace
    # Expected: Should fail (403) OR succeed (reveals BUG #11)

def test_workspace_member_can_list_datasets():
    """Test that workspace members can list datasets."""
    # Setup: user1 creates workspace and datasets
    # Test: user1 lists datasets
    # Expected: Returns datasets (200)

def test_non_member_cannot_list_datasets():
    """Test that non-members cannot list datasets."""
    # Setup: user1 creates workspace and datasets
    # Test: user2 tries to list datasets
    # Expected: Should fail (403) OR succeed (reveals BUG #14)
```

### Scenario 5: Role-Based Access Control (RBAC)
```python
def test_admin_can_create_workspace_for_any_user():
    """Test that admin users have elevated permissions."""
    # Setup: Login as admin user
    # Test: Create workspace for user2@example.com
    # Expected: Success (201) - admin should have this permission

def test_regular_user_cannot_create_workspace_for_others():
    """Test that regular users cannot create workspaces for others."""
    # Setup: Login as regular user (not admin)
    # Test: Create workspace for user2@example.com
    # Expected: Should fail (403) OR succeed (reveals BUG #8)

def test_viewer_role_has_limited_permissions():
    """Test that viewer role has read-only access."""
    # Setup: Create user with viewer role
    # Test: Try to create/update/delete resources
    # Expected: Should fail (403) for write operations
```

---

## Data Validation & Edge Cases

### Scenario 6: Input Validation Testing
```python
def test_create_workspace_with_invalid_owner_email():
    """Test workspace creation with non-existent owner."""
    # Test: Create workspace with owner_email that doesn't exist
    # Expected: Should fail (400) OR succeed (reveals BUG #7)

def test_create_dataset_with_invalid_workspace_id():
    """Test dataset creation with non-existent workspace."""
    # Test: Create dataset with workspace_id that doesn't exist
    # Expected: Should fail (404) OR succeed (reveals BUG #10)

def test_create_dataset_with_negative_row_count():
    """Test dataset creation with invalid row_count."""
    # Test: Create dataset with row_count=-1
    # Expected: Should fail validation (422) OR succeed (reveals BUG #12)

def test_list_datasets_with_invalid_pagination():
    """Test pagination edge cases."""
    # Test: List datasets with limit=-1 or limit=1000000
    # Expected: Should validate OR accept (reveals BUG #13)
    # Test: List datasets with offset beyond dataset count
    # Expected: Should return empty list gracefully (reveals BUG #16)
```

### Scenario 7: Data Integrity Testing
```python
def test_delete_workspace_cascades_to_datasets():
    """Test that deleting workspace also deletes datasets."""
    # Setup: Create workspace and datasets
    # Test: Delete workspace
    # Test: Try to access datasets
    # Expected: Datasets should be deleted OR remain orphaned (reveals BUG #18)

def test_concurrent_user_registration():
    """Test race condition in user registration."""
    # Test: Send two registration requests simultaneously with same email
    # Expected: Only one should succeed OR both might succeed (reveals BUG #4)
```

---

## Security Testing Scenarios

### Scenario 8: Security Vulnerability Testing
```python
def test_password_hashing_security():
    """Test that passwords are securely hashed."""
    # Test: Register user, check password storage
    # Expected: Password should be hashed (not plaintext)
    # Note: SHA256 is weak - this reveals BUG #2

def test_login_rate_limiting():
    """Test that login endpoint has rate limiting."""
    # Test: Send 100 rapid login attempts
    # Expected: Should throttle after N attempts OR no throttling (reveals BUG #5)

def test_token_expiration():
    """Test that expired tokens are rejected."""
    # Test: Login, wait past expiration, use token
    # Expected: Should fail (401) OR succeed (reveals BUG #3)
```

---

## Test Organization Best Practices

### Test Structure Example
```python
class TestAuthentication:
    """Test authentication flows."""

    def test_register_user(self):
        """Test user registration."""
        pass

    def test_login_user(self):
        """Test user login."""
        pass

class TestWorkspaceAuthorization:
    """Test workspace authorization scenarios."""

    def test_owner_can_access_workspace(self):
        """Test workspace owner access."""
        pass

    def test_non_member_cannot_access_workspace(self):
        """Test non-member access restriction."""
        pass

class TestDatasetManagement:
    """Test dataset CRUD operations."""

    def test_create_dataset(self):
        """Test dataset creation."""
        pass

    def test_list_datasets(self):
        """Test dataset listing."""
        pass
```

### Test Data Factory Example
```python
class UserFactory:
    """Factory for creating test users."""

    @staticmethod
    def create_admin():
        """Create admin user."""
        return {
            "email": f"admin_{secrets.token_hex(4)}@example.com",
            "name": "Admin User",
            "password": "SecurePass123!",
            "role": "admin"
        }

    @staticmethod
    def create_regular_user():
        """Create regular user."""
        return {
            "email": f"user_{secrets.token_hex(4)}@example.com",
            "name": "Regular User",
            "password": "SecurePass123!",
            "role": "user"
        }
```

---

## Key Testing Principles

1. **Test with Different User Roles**: Always test with admin, regular user, and viewer roles
2. **Test Multi-User Scenarios**: Test interactions between different users
3. **Test Authorization**: Who can do what? Validate permissions work correctly
4. **Test Edge Cases**: Boundary conditions, invalid inputs, error states
5. **Test Security**: Authentication, authorization, input validation
6. **Document Findings**: When tests fail, document them as bugs

---

## Expected Test Coverage

A comprehensive test suite should include:

- ✅ **15-20+ integration tests**
- ✅ **Tests covering all user roles** (admin, user, viewer)
- ✅ **Authorization tests** (who can access what)
- ✅ **Multi-user scenarios** (user A creates, user B accesses)
- ✅ **Edge case tests** (invalid inputs, boundary conditions)
- ✅ **Security tests** (authentication, token validation)
- ✅ **Data validation tests** (input validation, data integrity)

---

**Remember**: Your role is to **validate features work correctly** and **discover bugs**, not to fix them. Focus on comprehensive integration testing with different user scenarios.
