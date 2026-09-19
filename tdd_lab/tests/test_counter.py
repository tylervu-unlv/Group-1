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

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_get_counter(self, client):
        """It should retrieve an existing counter"""
        client.post('/counters/foo')
        result = client.get('/counters/foo')
        assert result.status_code == status.HTTP_200_OK
        assert result.get_json() == {"foo": 0}

    # ===========================
    # Test: List All Counters
    # Author: Barron McCarthy
    # Date: 2026-09-18
    # Description: Ensures all existing counters and their values are returned
    # ===========================
    def test_list_all_counters(self, client):
        """It should list all counters"""
        client.post('/counters/foo')
        client.post('/counters/bar')

        result = client.get('/counters')

        assert result.status_code == status.HTTP_200_OK
        assert result.get_json() == {
            "foo": 0,
            "bar": 0
        }
    # ===========================
    # Test: Incrementing Counter & Prevent updating non-existent counter
    # Author: Christopher Flores
    # Date: 2026-09-17
    # Description: Ensures a counter increments properly & prevents updating a non-existent counter
    # ===========================
    def test_increment_counter(self, client):
        """It should increment an existing counter"""
        client.post('/counters/increment')
        result = client.put('/counters/increment')
        assert result.status_code == status.HTTP_200_OK
        assert result.get_json()['increment'] == 1

    def test_non_existent_counter(self, client):
        """It should prevent updating a non-existent counter"""
        result = client.put('/counters/noCounter')
        assert result.status_code == status.HTTP_404_NOT_FOUND
    # Test: Delete a counter
    # Author: FinnWant
    # Date: 2026-09-16
    # Description: Ensure a counter can be deleted and deleting a non-existent counter is prevented
    # ===========================
    def test_delete_counter(self, client):
        """It should delete an existing counter"""
        client.post('/counters/bar')
        result = client.delete('/counters/bar')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED

    def test_delete_counter_not_found(self, client):
        """It should not delete a counter that doesn't exist"""
        result = client.delete('/counters/missing')
        assert result.status_code == status.HTTP_404_NOT_FOUND
