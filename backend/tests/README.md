# Test Suite - IT Support System

## 📁 Test Organization

The test suite is organized into logical categories:

```
tests/
├── auth/                    # Authentication tests
│   ├── test_auth_fix.py     # Auth persistence tests
│   └── test_aditi_user.py   # User-specific tests
├── api/                     # API endpoint tests
│   └── test_health.py       # Health check tests
├── integration/             # Integration tests
│   ├── test_backend.py      # Full backend tests
│   └── [other test files]   # Additional integration tests
├── run_tests.py             # Test runner script
└── README.md                # This file
```

## 🚀 Running Tests

### Run All Tests
```bash
cd backend
python tests/run_tests.py
```

### Run Specific Test Categories
```bash
# Authentication tests
cd backend/tests/auth
python test_auth_fix.py
python test_aditi_user.py

# API tests
cd backend/tests/api
python test_health.py

# Integration tests
cd backend/tests/integration
python test_backend.py
```

## 🧪 Test Categories

### Authentication Tests (`auth/`)
- **test_auth_fix.py**: Tests authentication persistence and token validation
- **test_aditi_user.py**: Specific tests for user "aditi_bansal" authentication

### API Tests (`api/`)
- **test_health.py**: Tests API health endpoints and basic connectivity

### Integration Tests (`integration/`)
- **test_backend.py**: Full backend integration tests
- Other integration tests for various components

## 🔧 Test Requirements

### Prerequisites
- Backend server must be running
- Required Python packages installed
- Database initialized (for database-backed tests)

### Server Setup
```bash
# For database-backed tests
python main_dynamic.py

# For in-memory tests
python working_server.py
```

## 📝 Writing New Tests

### Test File Naming
- Use `test_` prefix
- Use descriptive names: `test_auth_persistence.py`
- Place in appropriate category folder

### Test Structure
```python
#!/usr/bin/env python3
"""
Test description
"""

import requests
import json

def test_functionality():
    """Test specific functionality"""
    # Test implementation
    pass

if __name__ == "__main__":
    test_functionality()
```

### Best Practices
- Use descriptive test names
- Include setup and teardown
- Test both success and failure cases
- Use proper error handling
- Include clear output messages

## 🐛 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure backend server is running
   - Check correct port (8001 for main, 8002 for working)

2. **Import Errors**
   - Run tests from backend directory
   - Ensure all dependencies installed

3. **Test Failures**
   - Check server logs for errors
   - Verify test data and expectations
   - Ensure proper authentication tokens

### Debug Mode
Add debug output to tests:
```python
print(f"Debug: Response status: {response.status_code}")
print(f"Debug: Response data: {response.json()}")
```

## 📊 Test Results

The test runner provides:
- ✅ Passed tests
- ❌ Failed tests
- ⏰ Timeout tests
- 💥 Error tests
- 📊 Summary statistics

## 🔄 Continuous Integration

Tests can be integrated into CI/CD pipelines:
```bash
# Run tests in CI
cd backend
python tests/run_tests.py
```

This test suite ensures the IT Support System functions correctly across all components.
