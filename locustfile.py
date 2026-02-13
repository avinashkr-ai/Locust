import random
from locust import HttpUser, task, between

class APIPerformanceUser(HttpUser):
    """
    Load testing user that simulates realistic API usage patterns.
    
    Task weights:
    - test_get_item (4): Most common operation - users viewing specific products
    - test_get_all (2): Moderate usage - browsing the catalog
    - test_create_item (1): Less frequent - adding new products
    """
    
    # Wait between 0.5 and 2 seconds between tasks to simulate real user behavior
    wait_time = between(0.5, 2)
    
    # Track IDs that exist in the system (starting with seed data)
    existing_ids = list(range(1, 51))  # IDs 1-50 from seed data

    def on_start(self):
        """Called when a simulated user starts - optional setup"""
        # You could add authentication or other initialization here
        pass

    @task(4)
    def test_get_item(self):
        """
        Simulates users viewing specific products.
        Weight: 4 (most common operation)
        """
        target_id = random.choice(self.existing_ids)
        with self.client.get(f"/items/{target_id}", name="/items/[id]", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Item might have been deleted by another user
                response.failure("Item not found")
            else:
                response.failure(f"Unexpected status code: {response.status_code}")

    @task(2)
    def test_get_all(self):
        """
        Simulates browsing the full catalog.
        Weight: 2 (moderate usage)
        """
        with self.client.get("/items/", catch_response=True) as response:
            if response.status_code == 200:
                items = response.json()
                if isinstance(items, list):
                    response.success()
                else:
                    response.failure("Expected a list of items")
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(1)
    def test_create_item(self):
        """
        Simulates adding a new product.
        Weight: 1 (less frequent operation)
        """
        payload = {
            "name": f"LoadTest Item {random.randint(1000, 9999)}",
            "price": round(random.uniform(10.0, 999.99), 2)
        }
        
        with self.client.post("/items/", json=payload, name="/items/", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    new_item = response.json()
                    new_id = new_item.get("id")
                    if new_id:
                        # Add the new ID to our list so we can test it later
                        self.existing_ids.append(new_id)
                        response.success()
                    else:
                        response.failure("No ID in response")
                except Exception as e:
                    response.failure(f"Failed to parse response: {str(e)}")
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(1)
    def test_get_nonexistent_item(self):
        """
        Tests error handling by requesting items that don't exist.
        Weight: 1
        """
        # Try to get an item with a very high ID that likely doesn't exist
        fake_id = random.randint(10000, 99999)
        with self.client.get(f"/items/{fake_id}", name="/items/[id] (404)", catch_response=True) as response:
            if response.status_code == 404:
                response.success()  # Expected 404
            else:
                response.failure(f"Expected 404, got {response.status_code}")
