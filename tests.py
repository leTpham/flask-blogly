from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )
        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.user_id_2 = second_user.id


        test_post = Post(
            title = 'test_title',
            content = 'test_content',
            user_id = self.user_id
        )

        db.session.add_all([test_post])
        db.session.commit()

        self.post = test_post





    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_user_profile(self):
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            
            self.assertIn("<!-- testing for /users/user_id -->", html)
            
            #Test post appears in user's list:
            self.assertIn(f'{self.post.title}',html)

    def test_user_edit_form(self):
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn(f"<!-- testing for route /users/{self.user_id}/edit -->", html)

    def test_user_edit_form_submit(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/edit',
                            data={'first_name': 'Keys',
                                    'last_name': 'Soun',
                                        'image_url': DEFAULT_IMAGE_URL
                            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Keys', html)

    def test_delete_user(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id_2}/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn("test_first_two", html)
    
    def test_show_post(self):
        with self.client as c:
            resp = c.get(f"/posts/{self.post.id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn(f"<!-- testing for route /posts/{self.post.id}-->", html)
    
    def test_post_form_submit(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/posts/new',
                          data = {'title': 'IMPORTANT SQL TIP',
                                  'content': 'REFERENTIAL INTEGRITY',
                                  'user_id': self.user_id},
                          follow_redirects=True)
            html = resp.get_data(as_text=True)
             
            self.assertEqual(resp.status_code, 200)
            self.assertIn('IMPORTANT SQL TIP', html)
            
    # test editing?
    
    def test_post_edit_form_submit(self):
        with self.client as c:
            resp = c.post(f'/posts/{self.post.id}/edit',
                             data = {'title': 'ANOTHER NEW TIP',
                                  'content': 'TABLES ARE CONFUSING'},
                             follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('ANOTHER NEW TIP', html)    
    
    def test_delete_post(self):
        with self.client as c:
            resp = c.post(f'/posts/{self.post.id}/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('ANOTHER NEW TIP', html)
