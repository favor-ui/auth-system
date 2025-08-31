# Install pytest if not already installed
pip install pytest pytest-django pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest users/tests/test_auth.py -v

# Run specific test function
pytest users/tests/test_auth.py::test_register_and_login_flow -v