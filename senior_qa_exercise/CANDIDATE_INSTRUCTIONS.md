# Senior QA Automation Engineer - Technical Exercise

## Your Mission

The web application (`webapp.py`) contains **multiple bugs**. Your job is to:

1. **Start with Ticket #001** - Test the reported workspace deletion issue (see `TICKET_001.md`)
2. **Build automated tests** to find bugs
3. **Document the bugs** you discover (create your own bug report format)
4. **Find as many bugs as you can**
5. **Present your findings**

---

## Requirements

### ⚠️ AUTOMATED TESTING ONLY

- ✅ **REQUIRED**: Automate Swagger UI (`/docs`) - simulate human behavior (Playwright, Cypress, Selenium)
- ✅ **ACCEPTABLE**: Also test API directly if you want (pytest, requests, etc.)
- ✅ **REQUIRED**: Tests must run via command line and produce reports
- ❌ **NOT ACCEPTABLE**: Manual testing (clicking, screenshots, one-off requests)

**Bottom line**: You **MUST** automate the Swagger UI to simulate real user behavior. Additional API testing is optional.

---

## What to Do

### 1. Build Automated Test Framework

Create automated integration tests that:
- **Automate Swagger UI** (`/docs`) - click buttons, fill forms, submit requests like a human would
- Test authentication flows (registration, login, tokens)
- Test CRUD operations (workspaces, datasets)
- Test authorization (who can access what)
- Test with different user roles (admin, user, viewer)
- Test edge cases and error handling

**Deliverable**: Executable test framework with comprehensive test coverage

### 2. Find and Document Bugs

- **Start with Ticket #001**: Test the workspace deletion authorization issue described in `TICKET_001.md`
- Run your tests and identify failures
- Write additional tests to find more bugs
- Document bugs using your own bug report format
- Create both technical and non-technical versions for at least one bug (your choice which one)

**Deliverable**: Bug reports with clear reproduction steps. Find as many bugs as you can!

### 3. Present Your Findings

- Walk through your test framework
- Show bugs you found
- Explain your testing approach

---

## Setup

```bash
# Create virtual environment
cd brighthive-testing-exercise/senior_qa_exercise
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the webapp
python webapp.py
# Or: uvicorn webapp:app --reload --port 8000
# Or: ./start.sh (recommended)

# App runs at http://localhost:8000
# Swagger UI at http://localhost:8000/docs (THIS IS WHAT YOU MUST AUTOMATE)
```

## Authentication Flow

The app has a working authentication system:

1. **Register** users with roles: `admin`, `user`, or `viewer`
2. **Login** to get authentication token
3. **Use token** in `Authorization: Bearer <token>` header for protected endpoints
4. **Test with different roles** - create multiple users with different roles

**Example Flow:**
- Register admin user → Login → Get token → Use token to access endpoints
- Register regular user → Login → Get token → Test authorization scenarios
- Test who can access what based on roles

**API Usage Example:**
```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "Test User", "password": "Pass123", "role": "user"}'

# Login to get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "Pass123"}'
# Returns: {"token": "abc123...", "user": {...}}

# Use token for protected endpoints
curl -X DELETE http://localhost:8000/api/v1/workspaces/workspace-id \
  -H "Authorization: Bearer abc123..."
```

---

## Submission

Submit:
1. **Test framework code** (executable tests that automate Swagger UI)
2. **Bug reports**
3. **README** with setup/execution instructions

---

## Resources

- `TICKET_001.md` - **Start here!** Sample ticket describing a broken feature
- `TESTING_SCENARIOS.md` - Example test scenarios (optional reference)
- Swagger UI: http://localhost:8000/docs ← **Automate this!**

**Note**: Create your own bug report format. No template provided - use whatever format you think is best for communicating bugs to developers and stakeholders.

---

## FAQ

**Q: What tool should I use for Swagger automation?**
A: Playwright, Cypress, or Selenium - whatever you prefer. Just automate the Swagger UI.

**Q: Can I also test the API directly?**
A: Yes, but Swagger UI automation is mandatory. Additional API testing is optional.

**Q: Can I use Postman?**
A: Postman alone doesn't automate Swagger UI. Use Playwright/Cypress/Selenium for Swagger automation.

**Q: Can I modify webapp.py?**
A: No. Test and document bugs, don't fix them.

---

**Good luck! Test the shit out of it! 🚀**
