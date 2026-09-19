"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status
from src.counter import COUNTERS

@pytest.fixture(autouse=True)
def reset_counters():
    """COUNTERS is module-level state shared by every test.

    Without this, tests leak state into each other and the suite only passes
    in the order the functions happen to appear in this file. Clearing it
    before each test keeps every test independent.
    """
    COUNTERS.clear()
    yield
    COUNTERS.clear()

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        response = client.post('/counters/test_counter')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.get_json() == {"test_counter": 0}

    def test_prevent_duplicate_counter(self, client):
        """It should not allow duplicate counters"""
        client.post('/counters/test_counter')
        response = client.post('/counters/test_counter')
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_retrieve_existing_counter(self, client):
        """It should retrieve an existing counter"""
        client.post('/counters/test_counter')
        response = client.get('/counters/test_counter')
        assert response.status_code == status.HTTP_200_OK
        assert response.get_json() == {"test_counter": 0}

    def test_return_404_for_non_existent_counter(self, client):
        """It should return 404 if counter does not exist"""
        response = client.get('/counters/non_existent')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_increment_counter(self, client):
        """It should increment an existing counter"""
        client.post('/counters/test_counter')
        response = client.put('/counters/test_counter')
        assert response.status_code == status.HTTP_200_OK
        assert response.get_json() == {"test_counter": 1}

    def test_prevent_updating_non_existent_counter(self, client):
        """It should return 404 if trying to increment a non-existent counter"""
        response = client.put('/counters/non_existent')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_counter(self, client):
        """It should delete an existing counter"""
        client.post('/counters/test_counter')
        response = client.delete('/counters/test_counter')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_prevent_deleting_non_existent_counter(self, client):
        """It should return 404 if trying to delete a non-existent counter"""
        response = client.delete('/counters/non_existent')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_reset_all_counters(self, client):
        """It should reset all counters"""
        client.post('/counters/test_counter')
        response = client.post('/counters/reset')
        assert response.status_code == status.HTTP_200_OK
        assert response.get_json() == {"message": "All counters have been reset"}

    def test_list_all_counters(self, client):
        """It should list all counters"""
        client.post('/counters/test_counter1')
        client.post('/counters/test_counter2')
        response = client.get('/counters')
        assert response.status_code == status.HTTP_200_OK
        assert response.get_json() == {"test_counter1": 0, "test_counter2": 0}

    def test_handle_invalid_http_methods(self, client):
        """It should return 405 for unsupported HTTP methods"""
        response = client.patch('/counters/test_counter')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    
    """Test cases for Extended Counter API"""

    # ===========================
    # Test: Retrieve total count of all counters
    # Author: Student 1
    # Modification: Add assertion to check the total value is correct.
    # ===========================
    def test_get_total_counters(self, client):
        """It should return the total sum of all counter values"""
        client.post('/counters/test1')
        client.post('/counters/test2')
        client.put('/counters/test1')

        response = client.get('/counters/total')

        assert response.status_code == status.HTTP_200_OK
        
        # TODO: Add an assertion to check the correct total value

    # ===========================
    # Test: Retrieve top N highest counters
    # Author: Student 2
    # Modification: Ensure the API returns exactly N counters.
    # ===========================
    def test_top_n_counters(self, client):
        """It should return the top N highest counters"""
        client.post('/counters/reset')
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/a')
        client.put('/counters/b')
        client.put('/counters/b')

        response = client.get('/counters/top/2')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.get_json()) <= 2  

        # TODO: Add an assertion to ensure the returned counters are sorted correctly

    # ===========================
    # Test: Retrieve top N lowest counters
    # Author: Student 3
    # Modification: Ensure lowest counter has value 0.
    # ===========================
    def test_bottom_n_counters(self, client):
        """It should return the bottom N lowest counters"""
        client.post('/counters/reset')
        client.post('/counters/a')
        client.post('/counters/b')

        response = client.get('/counters/bottom/1')

        assert response.status_code == status.HTTP_200_OK
        assert min(response.get_json().values()) == 0  

        # TODO: Add an assertion to check that 'b' is indeed in the response

    # ===========================
    # Test: Set a counter to a specific value
    # Author: Student 4
    # Modification: Ensure setting a counter to the same value does nothing.
    # ===========================
    def test_set_counter_to_value(self, client):
        """It should set a counter to a specific value"""
        client.post('/counters/test1')
        response = client.put('/counters/test1/set/5')

        assert response.status_code == status.HTTP_200_OK
        assert response.get_json() == {"test1": 5}

        # TODO: Add an assertion to check setting to the same value does not change it again

    # ===========================
    # Test: Prevent negative counter values
    # Author: Student 5
    # Modification: Ensure setting a counter to zero is allowed.
    # ===========================
    def test_prevent_negative_counter_values(self, client):
        """It should prevent setting a counter to a negative value"""
        client.post('/counters/test1')

        response_zero = client.put('/counters/test1/set/0')
        response_negative = client.put('/counters/test1/set/-3')

        assert response_zero.status_code == status.HTTP_200_OK  
        assert response_negative.status_code == status.HTTP_400_BAD_REQUEST  
        
        # TODO: Add an assertion to verify the response message contains a clear error

    # ===========================
    # Test: Reset a single counter
    # Author: Student 6
    # Modification: Ensure counter still exists after reset.
    # ===========================
    def test_reset_single_counter(self, client):
        """It should reset a specific counter"""
        client.post('/counters/test1')
        client.put('/counters/test1/set/5')

        response = client.post('/counters/test1/reset')

        assert response.status_code == status.HTTP_200_OK
        assert response.get_json() == {"test1": 0}

        # TODO: Add an assertion to check that retrieving the counter still works

    # ===========================
    # Test: Prevent resetting a non-existent counter
    # Author: Student 7
    # Modification: Ensure resetting a non-existent counter does not create it.
    # ===========================
    def test_prevent_resetting_non_existent_counter(self, client):
        """It should return an error when resetting a non-existent counter"""
        response = client.post('/counters/non_existent/reset')

        assert response.status_code == status.HTTP_404_NOT_FOUND

        # TODO: Add an assertion to verify the error message contains the word 'not found'

    # ===========================
    # Test: Get total number of counters
    # Author: Student 8
    # Modification: Add assertion to check count is an integer.
    # ===========================
    def test_get_total_number_of_counters(self, client):
        """It should return the total number of counters"""
        client.post('/counters/reset')
        client.post('/counters/test1')
        client.post('/counters/test2')

        response = client.get('/counters/count')

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.get_json()["count"], int)  

        # TODO: Add an assertion to check the exact count value

    # ===========================
    # Test: Retrieve counters with values greater than a threshold
    # Author: Student 9
    # Modification: Ensure the threshold is exclusive.
    # ===========================
    def test_counters_greater_than_threshold(self, client):
        """It should return counters greater than the threshold"""
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/a/set/10')

        response = client.get('/counters/greater/10')

        assert response.status_code == status.HTTP_200_OK

        # TODO: Add an assertion to check that 'a' (value=10) is **excluded**.

    # ===========================
    # Test: Retrieve counters with values less than a threshold
    # Author: Student 10
    # Modification: Ensure threshold is exclusive.
    # ===========================
    def test_counters_less_than_threshold(self, client):
        """It should return counters less than the threshold"""
        client.post('/counters/reset')
        client.post('/counters/a')
        client.post('/counters/b')
        client.put('/counters/a/set/5')

        response = client.get('/counters/less/5')

        assert response.status_code == status.HTTP_200_OK

        # TODO: Add an assertion to ensure 'b' (value=0) is returned as the lowest.

    # ===========================
    # Test: Validate counter names (prevent special characters)
    # Author: Student 11
    # Modification: Ensure error message is specific.
    # ===========================
    def test_validate_counter_name(self, client):
        """It should prevent creating counters with special characters"""
        response = client.post('/counters/test@123')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # TODO: Add an assertion to verify the error message specifically says 'Invalid counter name'
