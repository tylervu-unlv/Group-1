"""
Test Cases for Account Model
"""
import json
from pathlib import Path
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open(Path(__file__).parent / 'fixtures' / 'account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture
def setup_account():
    """Fixture to create a test account"""
    account = Account(name="John businge", email="john.businge@example.com")
    db.session.add(account)
    db.session.commit()
    return account

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# Test Assignments

# Student 1: Test account serialization
# - Verify that the account object is correctly serialized to a dictionary.
# - Ensure all expected fields are included in the output.
# Target Method: to_dict()
# ===========================
# Test: Test account serialization
# Author: Tyler Vu
# Date: 2026-09-09
# Description: Ensure the account object is correctly serialized to a dictionary.
# ===========================
# create function to test
def test_account_serialization():
    """Test converting an account to a dictionary"""
    # sets account with random info to check
    account = Account(name="Tyler Vu", email = "tyler@gmail.com", role = "user",
                      phone_number="702-111-1234", balance = 500.0)
    # sets a password
    account.set_password("testing4life")
    db.session.add(account)
    db.session.commit()

    data = account.to_dict()

    #check outputs
    assert data["id"] == account.id
    assert data["name"] == "Tyler Vu"
    assert data["email"] == "tyler@gmail.com"
    assert data["role"] == "user"
    assert data["phone_number"] == "702-111-1234"
    assert data["disabled"] == account.disabled
    assert data["date_joined"] == account.date_joined
    assert data["balance"] == 500.0

    # verify if account is serialized
    assert "password_hash" not in data
    
    

# Student 2: Test invalid email input
# - Ensure invalid email formats raise a validation error.
# Target Method: validate_email()

# Student 3: Test missing required fields
# - Ensure a DataValidationError is raised when name or email is missing.
# - Note: SQLAlchemy does not validate on construction, so Account() itself
#   never raises. Call the validation method on the constructed object.
# Target Method: validate_required_fields()

# Student 4: Test positive deposit
# - Verify that depositing a positive amount correctly increases the balance.
# Target Method: deposit()

# Student 5: Test deposit with zero/negative values
# - Ensure zero or negative deposits are rejected.
# Target Method: deposit()

# Student 6: Test valid withdrawal
# - Verify that withdrawing a valid amount correctly decreases the balance.
# Target Method: withdraw()

# Student 7: Test withdrawal with insufficient funds
# - Ensure withdrawal fails when balance is insufficient.
# Target Method: withdraw()

# Student 8: Test password hashing
# - Ensure passwords are properly hashed.
# - Verify that password verification works correctly.
# Target Methods: set_password() / check_password()

# Student 9: Test account deactivation/reactivation
# - Ensure accounts can be deactivated and reactivated correctly.
# Target Methods: deactivate() / reactivate()

# Student 10: Test email uniqueness enforcement
# - Ensure duplicate emails are not allowed.
# Target Method: validate_unique_email()

# Student 11: Test deleting an account
# - Verify that an account can be successfully deleted from the database.
# Target Method: delete()
