from django.test import TestCase
from django.contrib.auth.models import User


from password.pwd import create_new_file


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'zezin',
            'password': '1234x567',
            'pwd_db': '1234',
        }

        self.user = {
            'username': 'zezin',
            'password': '1234x567',
        }
        self.user_test = User.objects.create_user(**self.user)
        create_new_file(self.user_test.id, '1234')
        self.credentials_error = {'username': 'zekako', 'password': '12334555', 'pwd_db': '1234'}

    def test_get_login_status(self):
        response = self.client.get("/users/login/")
        self.assertEqual(response.status_code, 200)

    def test_post_login_status(self):
        response = self.client.post('/users/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_post_login_status_error(self):
        response = self.client.post('/users/login/', self.credentials_error, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_redirect_login_success(self):
        response = self.client.post('/users/login/', self.credentials, follow=True)
        self.assertRedirects(response, '/pwd/')

    def test_redirect_login_error(self):
        response = self.client.post('/users/login/', self.credentials_error, follow=True)
        self.assertRedirects(response, '/users/login/')

    # empty input
    def test_post_login_pwd_empty_status(self):
        credentials = {'username': 'zekaki', 'password': '', 'pwd_db': '1234'}
        response = self.client.post('/users/login/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_post_login_username_empty_status(self):
        credentials = {'username': ' ', 'password': '1234x567', 'pwd_db': '1234'}
        response = self.client.post('/users/login/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)


class RegisterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'zequinha',
            'email': 'zequinha@mail.com',
            'password1': '1234x567',
            'password2': '1234x567',
            'pwd_db': '1234'
        }

    def test_signup_user_success(self):
        response = self.client.post('/users/register/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_signup_status(self):
        response = self.client.post('/users/register/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_success_redirect(self):
        response = self.client.post('/users/register/', self.credentials, follow=True)
        self.assertRedirects(response, '/pwd/')

    # Error pwd1
    def test_signup_error_pwd1(self):
        credentials = {'username': 'zekaze', 'password1': '1234x555', 'password2': '1234x567', 'email': 'zekaze@mail.com', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_signup_error_pwd1_redirect(self):
        credentials = {'username': 'zekaze', 'password1': '1234x555', 'password2': '1234x567', 'email': 'zekaze@mail.com', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertRedirects(response, '/users/login/')

    # Error pwd2
    def test_signup_error_no_pwd2(self):
        credentials = {'username': 'zekaze', 'password1': '1234x567', 'email': 'zekaze@mail.com', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_signup_error_no_pwd2_redirect(self):
        credentials = {'username': 'zekaze', 'password1': '1234x567', 'email': 'zekaze@mail.com', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertRedirects(response, '/users/login/')

    # Error username
    def test_signup_error_username(self):
        credentials = {'password1': '1234x567', 'password2': '1234x567', 'email': 'zekaze@mail.com', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_signup_error_username_redirect(self):
        credentials = {'password1': '1234x567', 'password2': '1234x567', 'email': 'zekaze@mail.com', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertRedirects(response, '/users/login/')

    def test_signup_error_username_empty(self):
        credentials = {'username': ' ', 'password1': '1234x567', 'password2': '1234x567', 'email': 'zekaze@mail.com',
                       'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_signup_error_username_empty_redirect(self):
        credentials = {'username': ' ', 'password1': '1234x567', 'password2': '1234x567', 'email': 'zekaze@mail.com',
                       'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertRedirects(response, '/users/login/')

    # Error username
    def test_signup_error_email(self):
        credentials = {'password1': '1234x567', 'password2': '1234x567', 'email': ' ', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_signup_error_email_redirect(self):
        credentials = {'password1': '1234x567', 'password2': '1234x567', 'email': ' ', 'pwd_db': '1234'}
        response = self.client.post('/users/register/', credentials, follow=True)
        self.assertRedirects(response, '/users/login/')


class EditTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'dolinho8',
            'password1': '1234x567',
            'password2': '1234x567',
            'email': 'zekako@mail.com',
            'pwd_db': '1111',
        }
        self.user = {
            'username': 'zekazz',
            'password': '1234x567',
        }
        self.test_user = User.objects.create_user(**self.user)
        create_new_file(self.test_user.id, '1234')

    def test_get_edit_status(self):
        self.client.login(username=self.user['username'], password=self.user['password'])
        response = self.client.get("/users/config/")
        self.assertEqual(response.status_code, 200)

    def test_post_edit_status(self):
        self.client.login(username=self.user['username'], password=self.user['password'], pwd_db='1234')
        create_new_file(self.test_user.id, '1234')
        session = self.client.session
        session["pwd_db"] = '1234'
        session.save()
        response = self.client.post('/users/config/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_redirect_success(self):
        self.client.login(username=self.user['username'], password=self.user['password'], pwd_db='1234')
        create_new_file(self.test_user.id, '1234')
        session = self.client.session
        session["pwd_db"] = '1234'
        session.save()
        response = self.client.post('/users/config/', self.credentials, follow=True)
        self.assertRedirects(response, '/pwd/')

    # Change user attributes
    def test_post_edit_change_username(self):
        self.client.login(username=self.user['username'], password=self.user['password'])
        create_new_file(self.test_user.id, '1234')
        session = self.client.session
        session["pwd_db"] = '1234'
        session.save()
        response = self.client.post('/users/config/', self.credentials, follow=True)
        self.assertEqual(response.context['user'].username, self.credentials['username'])

    def test_post_edit_change_email(self):
        self.client.login(username=self.user['username'], password=self.user['password'])
        create_new_file(self.test_user.id, '1234')
        session = self.client.session
        session["pwd_db"] = '1234'
        session.save()
        response = self.client.post('/users/config/', self.credentials, follow=True)
        self.assertEqual(response.context['user'].email, self.credentials['email'])

    def test_post_edit_change_pwd(self):
        self.client.login(username=self.user['username'], password=self.user['password'])
        create_new_file(self.test_user.id, '1234')
        session = self.client.session
        session["pwd_db"] = '1234'
        session.save()
        self.client.post('/users/config/', self.credentials, follow=True)
        user = User.objects.get(username=self.credentials['username'])
        self.assertEqual(user.check_password(self.credentials['password1']), True)
