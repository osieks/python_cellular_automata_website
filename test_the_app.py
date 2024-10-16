import unittest
import json
import numpy as np
from app import app, update_data

class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_route(self):
        """Test that the home route returns the index.html."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if the response contains HTML (since it's rendering index.html)
        self.assertIn(b'<!DOCTYPE html>', response.data)
    
    def test_init_route(self):
        """Test the /init route to initialize the cellular automata with given window size."""
        window_size = {'width': 400, 'height': 400}
        response = self.app.post('/init', data=json.dumps(window_size), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Ensure the returned array is of the correct shape (20x20)
        self.assertEqual(len(data), 20)
        self.assertEqual(len(data[0]), 20)
        # Check if the data is initialized to zero
        self.assertTrue(all(all(cell == 0 for cell in row) for row in data))

    def test_update_route(self):
        """Test the /update route to ensure that the cellular automata updates correctly."""
        # Initialize with a simple state (5x5 grid)
        initial_state = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        
        # Send the initial state as a POST request
        response = self.app.post('/update', data=json.dumps(initial_state), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Check the response for the next state after updating
        next_state = json.loads(response.data)
        expected_next_state = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        
        self.assertEqual(next_state, expected_next_state)

    def test_update_data(self):
        """Test the update_data function with a manual grid state."""
        # Initial state with a simple blinker (vertical line)
        initial_data = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ], dtype=int)
        
        # Apply the update
        updated_data = update_data(initial_data)
        
        # Expected next state (horizontal line)
        expected_data = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ], dtype=int)
        
        # Verify the update matches the expected state
        np.testing.assert_array_equal(updated_data, expected_data)

if __name__ == '__main__':
    unittest.main()
