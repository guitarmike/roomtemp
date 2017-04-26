from django.test import TestCase, Client

class RoomTest(TestCase):

    def test_home(self):
        c = Client()
        # Perform a vote on the poll by mocking a POST request.
        response = c.get("/")
        # In the vote view we redirect the user, so check the
        # response status code is 302.
        self.assertEqual(response.status_code, 200)
