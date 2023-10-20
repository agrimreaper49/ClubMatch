from django.test import TestCase
from django.contrib.auth.models import User
from .models import Club, Membership
from .forms import ClubForm, EventForm
# Create your tests here.

class FormsTestCase(TestCase):
    
    def test_club_form_is_valid(self):
        form_data = {
            'club_name': 'club',
            'description': 'description.'
        }
        form = ClubForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_club_form_is_not_valid(self):
        form_data = {}
        form = ClubForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_event_form_is_valid(self):
        form_data = {
            'event_name': 'test event',
            'description': 'description.',
            'date': '2023-12-31',
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'location': 'test location'
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_is_not_valid(self):
        form_data = {}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())


class MembershipModelTestCase(TestCase):
    def setUp(self):
        # Create a user and a club for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.club = Club.objects.create(owner=self.user, name='Test Club')
    
    def test_membership_creation(self):
        # Create a membership for the user and club
        membership = Membership.objects.create(user=self.user, club=self.club, role='pending')

        # Check that the membership was created with the correct data
        self.assertEqual(membership.user, self.user)
        self.assertEqual(membership.club, self.club)
        self.assertEqual(membership.role, 'pending')

    def test_membership_approval(self):
        # Create a membership with a 'pending' role
        membership = Membership.objects.create(user=self.user, club=self.club, role='pending')
        membership.approve()

        self.assertEqual(membership.role, 'member')

    def test_membership_string_representation(self):
        # Create a membership
        membership = Membership.objects.create(user=self.user, club=self.club, role='member')

        # Check the string representation of the membership
        expected_str = f'{self.user.username} is member of {self.club.name}'
        self.assertEqual(str(membership), expected_str)
        
