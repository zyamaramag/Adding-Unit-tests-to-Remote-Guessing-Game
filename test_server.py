import unittest
from unittest.mock import Mock
from server import get_rating, handle_client

class TestServer(unittest.TestCase):

    def test_get_rating(self):
        self.assertEqual(get_rating(3), "Excellent")
        self.assertEqual(get_rating(10), "Very Good")
        self.assertEqual(get_rating(30), "Good/Fair")

    def test_handle_client_correct_guess(self):
        mock_socket = Mock()

       
        mock_socket.recv.side_effect = [
            b'maramag',
            b'20',    
            b'80',  
            b'50'     
        ]

        sent_data = []
        mock_socket.send.side_effect = lambda msg: sent_data.append(msg.decode())

        handle_client(mock_socket, secret_number=50)

        self.assertIn("Welcome, Client!", sent_data[0])
        self.assertIn("Access granted", sent_data[1])
        self.assertIn("Too low", sent_data[2])
        self.assertIn("Too high", sent_data[3])
        self.assertTrue(any("Correct!" in msg for msg in sent_data))

    def test_handle_client_wrong_password(self):
        mock_socket = Mock()
        mock_socket.recv.side_effect = [b'wrongpass']
        sent_data = []
        mock_socket.send.side_effect = lambda msg: sent_data.append(msg.decode())

        handle_client(mock_socket, secret_number=42)

        self.assertIn("Incorrect password", sent_data[1])

if __name__ == "__main__":
    unittest.main()
