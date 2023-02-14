from django.test import TestCase
from password.pwd import create_new_file

from django.contrib.auth.models import User


class PagesTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'temporary',
            'password': 'temporary',
        }

        self.test_user = User.objects.create_user(**self.user)

    def test_get_home_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_home_redirect(self):
        response = self.client.get("/", follow=True)
        self.assertRedirects(response, "/users/login/?next=/pwd/")

    def test_home_redirect_logged(self):
        self.client.login(username='temporary', password='temporary')
        session = self.client.session
        create_new_file(self.test_user.id, '1234')
        session["pwd_db"] = '1234'
        session.save()
        response = self.client.get("/", follow=True)
        self.assertRedirects(response, "/pwd/")

    def test_about_status(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
