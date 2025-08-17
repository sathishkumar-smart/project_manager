from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTestCase(TestCase):
    """
    TestCase for the 'accounts' app.
    Tests registration and email-based login functionality.
    """

    def setUp(self):
        """
        Set up test client and create a default user for login tests.
        """
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123"
        )

    def test_register_user(self):
        """
        Test the user registration endpoint.
        Ensures that a new user can register and receives a token.
        """
        payload = {
            "email": "newuser@example.com",
            "password": "newpassword123"
        }

        # Send POST request to registration endpoint
        response = self.client.post("api/accounts/register/", payload, format="json")

        # Check that the response status is 201 CREATED
        self.assertEqual(response.status_code, 201)

        # Check that a token is returned
        self.assertIn("token", response.data)

        # Verify that the returned email matches the payload
        self.assertEqual(response.data["user"]["email"], payload["email"])

    def test_login_user(self):
        """
        Test the email-based login endpoint.
        Ensures that an existing user can log in and receives a token.
        """
        payload = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }

        # Send POST request to email login endpoint
        response = self.client.post("api/accounts/login/", payload, format="json")

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Ensure token is present in the response
        self.assertIn("token", response.data)

        # Verify that the returned email matches the user
        self.assertEqual(response.data["email"], self.user.email)
