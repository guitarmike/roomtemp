from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.urlresolvers import reverse
from rtemp.models import Room, Attendee, Vote

class RoomTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        login = self.client.login(username='testuser1', password='12345')


        self.room = Room.objects.create(
            owner = self.user1,
            text = "test",
            created_date = timezone.now(),
            room_type = "t",
            feed = "feed",
            caption_1 = "1",
            caption_2 = "2",
            caption_3 = "3",
            caption_4 = "4",
            vote_interval = datetime.timedelta(minutes=10),
            public = False,
            code = ""
        )


        self.attendee = Attendee.objects.create(
            room = self.room,
            session = self.client.session.session_key,
            last_action = timezone.now()
        )

        self.vote = Vote.objects.create(
            room = self.room,
            attendee = self.attendee,
            created_date = timezone.now(),
            thumbs = "+"
        )






    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_thermometer_view(self):
        c = Client()
        response = c.get(reverse('detail', kwargs={'room_id': self.room.id}))
        self.assertEqual(response.status_code, 200)
        response = c.get(reverse('detail', kwargs={'room_id': 0}))
        self.assertEqual(response.status_code, 404)

    def test_code_length(self):
        self.room.makeCode()
        self.assertEqual(len(self.room.code), 5)

    def test_code_alpha(self):
        self.room.makeCode()
        self.assertEqual(self.room.code.isalpha(), True)

    def test_able_to_vote(self):
        self.assertFalse(self.room.able_to_vote(self.client.session.session_key))
        self.vote.created_date = timezone.now() - datetime.timedelta(days = 10)
        self.vote.save()
        self.assertTrue(self.room.able_to_vote(self.client.session.session_key))

    def test_attendee_count(self):
        self.assertEqual(self.room.attendee_count(),1)

    def test_vote_count(self):
        self.assertEqual(self.room.current_vote_count(),1)
        self.vote.created_date = timezone.now() - datetime.timedelta(days=10)
        self.vote.save()
        self.assertEqual(self.room.current_vote_count(),0)

    def test_owned_by(self):
        self.assertTrue(self.room.owned_by(self.user1))
        self.assertFalse(self.room.owned_by(self.user2))

    def test_show_widget(self):
        self.assertTrue(self.room.show_widget(self.user1))
        self.assertFalse(self.room.show_widget(self.user2))
        self.room.public = True
        self.room.save()
        self.assertTrue(self.room.show_widget(self.user2))

    def test_thumbs_count(self):
        self.assertEqual(self.room.thumbs_up_count(), 1)
        self.assertEqual(self.room.thumbs_down_count(), 0)

    def test_thumbs_ajax(self):
        response = self.client.get(reverse('vote', kwargs={'room_id': self.room.id}),{'payload':'+'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.room.vote_set.latest('created_date').thumbs, "+")
        response = self.client.get(reverse('vote', kwargs={'room_id': self.room.id}),{'payload':'-'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.room.vote_set.latest('created_date').thumbs, "-")
        response = self.client.get(reverse('vote', kwargs={'room_id': self.room.id}),{'payload':''})
        self.assertEqual(response.status_code, 500)
        response = self.client.get(reverse('vote', kwargs={'room_id': self.room.id}),{'payload':'?'})
        self.assertEqual(response.status_code, 500)
