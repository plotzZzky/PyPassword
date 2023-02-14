from django.test import TestCase
from django.contrib.auth.models import User

from password.pwd import create_new_file, add_password


class AppTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'temporary',
            'password': 'temporary',
        }
        self.test_user = User.objects.create_user(**self.user)

    def set_pwd_db(self):
        self.client.login(username='temporary', password='temporary')
        session = self.client.session
        create_new_file(self.test_user.id, '1234')
        session["pwd_db"] = '1234'
        add_password('1234', self.test_user.id, 'temporary', 'temporary', 'password', 'url')
        session.save()

    def test_app_status(self):
        response = self.client.get("/pwd/")
        self.assertEqual(response.status_code, 302)

    def test_app_status_redirect(self):
        response = self.client.get("/pwd/")
        self.assertRedirects(response, "/users/login/?next=/pwd/")

    def test_get_app_status_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/")
        self.assertEqual(response.status_code, 200)

    def test_get_app_redirect_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/")
        self.assertNotEqual(response, 302)

    def test_get_pwd_list_status(self):
        response = self.client.get("/pwd/list/")
        self.assertEqual(response.status_code, 302)

    def test_get_pwd_list_status_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/list/")
        self.assertEqual(response.status_code, 200)

    def test_get_pwd_list_content(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/list/")
        self.assertTemplateUsed(response, "leftbar.html")

    def test_get_pwd_list_content_error(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get("/pwd/list/")
        self.assertEqual(response.status_code, 500)

    def test_pwd_props_status(self):
        response = self.client.get("/pwd/props/name=test/")
        self.assertEqual(response.status_code, 302)

    def test_pwd_props_status_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/props/name=temporary/")
        self.assertEqual(response.status_code, 200)

    def test_pwd_props_content_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/props/name=temporary/")
        self.assertTemplateUsed(response, "pwd_props.html")

    def test_pwd_props_logged_input_new(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/props/name=new/")
        self.assertTemplateUsed(response, "pwd_props.html")

    def test_pwd_props_logged_input_temporary(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/props/name=temporary/")
        self.assertTemplateUsed(response, "pwd_props.html")

    def test_del_pwd_status(self):
        response = self.client.get("/pwd/del/name=temporary/")
        self.assertEqual(response.status_code, 302)

    def test_del_pwd_status_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/del/name=temporary/")
        self.assertEqual(response.status_code, 200)

    def test_del_pwd_status_logged_not_found(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/del/name=notfound/")
        self.assertEqual(response.status_code, 404)

    def test_del_pwd_status_logged_no_db_pwd(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get("/pwd/del/name=notfound/")
        self.assertEqual(response.status_code, 500)

    def test_pwd_download_status(self):
        response = self.client.get("/pwd/download/")
        self.assertEqual(response.status_code, 302)

    def test_pwd_download_status_logged(self):
        self.set_pwd_db()
        response = self.client.get("/pwd/download/")
        self.assertEqual(response.status_code, 200)

    def test_update_password_status(self):
        response = self.client.get("/pwd/new/")
        self.assertEqual(response.status_code, 302)

    def test_post_update_password_logged_new_password_status(self):
        self.set_pwd_db()
        data = {
            'pwd_db': '1234',
            'user_id': self.test_user.id,
            'title': 'temporary1',
            'new_title': 'temporary1',
            'username': 'temporary',
            'password': 'password',
            'url': 'url'
        }
        response = self.client.post("/pwd/new/", data)
        self.assertEqual(response.status_code, 201)

    def test_post_update_password_logged_update_password_status(self):
        self.set_pwd_db()
        data = {
            'pwd_db': '1234',
            'user_id': self.test_user.id,
            'title': 'temporary',
            'new_title': 'temporay1',
            'username': 'temporary',
            'password': 'password',
            'url': 'url'
        }
        response = self.client.post("/pwd/new/", data)
        self.assertEqual(response.status_code, 202)
