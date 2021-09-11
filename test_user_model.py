"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

from unittest import TestCase
import os
from app import app
from models import db, User, Message, Follows


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


class UserModelTestCase(TestCase):
    """Test views for users."""

    @classmethod
    def setUpClass(cls):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        user1 = User.signup("test1", "test1@email.com", "testpw", None)
        user2 = User.signup("test2", "test2@email.com", "testpw", None)
        user3 = User.signup("test3", "test3@email.com", "testpw", None)
        user4 = User.signup("test4", "test4@email.com", "testpw", None)

    def setUp(self):
        """add test client"""

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u1 = User.query.get(1)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_repr(self):
        """Tests the repr function for correct output """

        u1 = User.query.get(1)
        represent = repr(u1)

        self.assertEqual("<User #1: test1, test1@email.com>", represent)

    def test_is_following(self):
        """tests whether is_following successfully detects when user1 is following user2"""

        u1 = User.query.get(1)
        u2 = User.query.get(2)

        new_follow = Follows(user_being_followed_id=2, user_following_id=1)
        db.session.add(new_follow)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))

    def test_is_not_following(self):
        """tests whether is_following successfully detects when user1 is not following user2"""
        u1 = User.query.get(1)
        u2 = User.query.get(2)

        Follows.query.delete()

        self.assertFalse(u1.is_following(u2))

    def test_is_followed_by(self):
        """Tests whether is_followed_by successfully detects when user1 is followed by user2"""

        u1 = User.query.get(1)
        u2 = User.query.get(2)

        new_follow = Follows(user_being_followed_id=1, user_following_id=2)
        db.session.add(new_follow)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))

    def test_is_not_followed_by(self):
        """tests whether is_followed_by successfully detect when user1 is not followed by user2?"""

        u1 = User.query.get(1)
        u2 = User.query.get(2)

        Follows.query.delete()

        self.assertFalse(u1.is_followed_by(u2))

    def test_user_signup(self):
        """Does User.create successfully create a new user given valid credentials?"""

        User.signup(username='test5', email='test5@email.com',
                    password='testpw', image_url=None)

        self.assertTrue(User.query.get(5))

    def test_user_signup_fail(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        # missing imageURL
        with self.assertRaises(TypeError):
            User.signup(username='test6', email='test6@email.com',
                        password='testpw')

        # need further help

    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        self.assertTrue(User.authenticate(
            username='test1', password='testpw'))

    def test_user_authenticate_username_fail(self):
        """Does User.authenticate fail to return a user when the username is invalid"""

        self.assertFalse(User.authenticate(
            username='wrongusername', password='testpw'))

    def test_user_authenticate_pw_fail(self):
        """Does User.authenticate fail to return a user when the password is invalid """

        self.assertFalse(User.authenticate(
            username='test1', password='wrongpassword'))
