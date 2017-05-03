from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from rtemp.models import Room

class RoomTest(TestCase):

    def setUp(self):
        room = Room.objects.create(
            owner = User.objects.create(username='user1'),
            text = "test",
            created_date = timezone.now(),
            room_type = "t",
            feed = "feed",
            caption_1 = "1",
            caption_2 = "2",
            caption_3 = "3",
            caption_4 = "4",
            vote_interval = datetime.timedelta(minutes=1),
            public = True,
            code = ""
        )

    def test_home(self):
        c = Client()
        # Perform a vote on the poll by mocking a POST request.
        response = c.get("/")
        # In the vote view we redirect the user, so check the
        # response status code is 302.
        self.assertEqual(response.status_code, 200)

    def test_code_length(self):
        room = Room.objects.get(text="test")
        room.makeCode()
        self.assertEqual(len(room.code), 5)

    def test_code_alpha(self):
        room = Room.objects.get(id=1)
        room.makeCode()
        self.assertEqual(room.code.isalpha(), True)
