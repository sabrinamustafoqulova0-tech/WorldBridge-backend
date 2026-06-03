from fastapi.testclient import TestClient
from main import app
import json
from fastapi.exceptions import ResponseValidationError

client = TestClient(app)

try:
    response = client.get("/api/v1/programs/us-work-travel")
    print("STATUS:", response.status_code)
except ResponseValidationError as e:
    print("ERRORS:", e.errors())
except Exception as e:
    print("OTHER:", repr(e))
