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

# Student 2: Test invalid email input
# - Ensure invalid email formats raise a validation error.
# Target Method: validate_email()

# ===========================
# Test: Invalid Email Input
# Author: Daniela Lopez
# Date: 2026-09-10
# Description: Ensure validate_email() rejects invalid email formats.
# ===========================

def test_invalid_email_format():
    """Test that an invalid email raises DataValidationError"""
    account = Account(name="John Doe", email="not-an-email")

    with pytest.raises(DataValidationError):
        account.validate_email()
        
# Student 3: Test missing required fields
# - Ensure a DataValidationError is raised when name or email is missing.
# - Note: SQLAlchemy does not validate on construction, so Account() itself
#   never raises. Call the validation method on the constructed object.
# Target Method: validate_required_fields()

# ===========================
# Test: Missing Required Fields
# Author: Daniela Lopez
# Date: 2026-09-10
# Description: Ensure validate_required_fields() raises DataValidationError when required fields are missing.
# ===========================

def test_missing_name_raises_error():
    """Test that a missing name raises DataValidationError"""
    account = Account(name="", email="johndoe@example.com")

    with pytest.raises(DataValidationError):
        account.validate_required_fields()

def test_missing_email_raises_error():
    """Test that a missing email raises DataValidationError"""
    account = Account(name="John Doe", email="")

    with pytest.raises(DataValidationError):
        account.validate_required_fields()

# Student 4: Test positive deposit
# - Verify that depositing a positive amount correctly increases the balance.
# Target Method: deposit()

# ===========================
# Test: Positive deposit
# Author: Christopher Flores
# Date: 2026-9-11
# Description: Makes sure that depositing a positive amount increases the balance. 
# ===========================

def test_positive_deposit():
    """Test depositing a positive amount"""
    account = Account(name = "Chris Flores", email = "chrisflores@gmai.com", balance = 0.0)
    account.deposit(100)
    assert account.balance == 100



# Student 5: Test deposit with zero/negative values
# - Ensure zero or negative deposits are rejected.
# Target Method: deposit()

# ===========================
# Test: deposit with zero/negative values
# Author: Christopher Flores
# Date: 2026-9-11
# Description: Makes sure that depositing a zero or negative value gets rejected 
# ===========================

@pytest.mark.parametrize("values", [(0), (0.0), (-100), (-100.0)])
def test_negative_or_zero_result(values):
    """Test an amount of negative/zero"""
    account = Account(name = "Chris Flores", email = "chrisflores@gmail.com", balance = 0.0)
    with pytest.raises(DataValidationError):
        account.deposit(values) 
        assert account.balance == 0.0
    


# Student 6: Test valid withdrawal
# - Verify that withdrawing a valid amount correctly decreases the balance.
# Target Method: withdraw()

# ===========================
# Test: Valid Withdrawal
# Author: Finn Wantland
# Date: 2026-09-13
# Description: Ensure that withdrawing a valid amount (positive and no
#   greater than the current balance) correctly decreases the account
#   balance by the withdrawn amount.
# Issue: Add a test for valid withdrawal
# ===========================

def test_valid_withdrawal():
    """Test that a valid withdrawal correctly decreases the account balance"""
    account = Account(name="Jane Doe", email="janedoe@example.com", balance=100.0)

    # Withdraw a valid amount
    account.withdraw(40.0)

    # Balance should be reduced by exactly the withdrawn amount
    assert account.balance == 60.0

# Student 7: Test withdrawal with insufficient funds
# - Ensure withdrawal fails when balance is insufficient.
# Target Method: withdraw()

# ===========================
# Test: Withdrawal with Insufficient Funds
# Author: Finn Wantland
# Date: 2026-09-13
# Description: Ensure that attempting to withdraw more than the current
#   balance raises a DataValidationError and leaves the balance unchanged.
# Issue: Add a test for insufficient-funds withdrawal
# ===========================

def test_withdraw_insufficient_funds():
    """Test that withdrawing more than the available balance raises an error"""
    account = Account(name="Jane Doe", email="janedoe@example.com", balance=50.0)

    # Attempt to withdraw more than the balance
    with pytest.raises(DataValidationError):
        account.withdraw(100.0)

    # Balance should remain unchanged after the failed withdrawal
    assert account.balance == 50.0

# Student 8: Test password hashing
# - Ensure passwords are properly hashed.
# - Verify that password verification works correctly.
# Target Methods: set_password() / check_password()

# ===========================
# Test: Test password hashing
# Author: Barron McCarthy
# Date: 2026-09-16
# Description: Ensure passwords are properly hashed and
# verify that password verification works correctly.
# Issue: Add a test ensuring passwords are hashed, correct passwords are
# being accepted, and incorrect passwords are being rejected.
# ===========================

def test_account_password_hashing():
    """Test password hashing and verification"""
    account = Account(name = "John Doe", email = "johndoe@example.com")

    password = "Password123!"
    account.set_password(password)

    # Check if the the password is hashed by checking if equal to 'password'
    assert account.password_hash != password

    # Checks for correct password acceptance.
    assert account.check_password(password) is True

    # Checks for incorrect password rejection.
    assert account.check_password("Password1234!") is False

# Student 9: Test account deactivation/reactivation
# - Ensure accounts can be deactivated and reactivated correctly.
# Target Methods: deactivate() / reactivate()

# Student 10: Test email uniqueness enforcement
# - Ensure duplicate emails are not allowed.
# Target Method: validate_unique_email()

# Student 11: Test deleting an account
# - Verify that an account can be successfully deleted from the database.
# Target Method: delete()