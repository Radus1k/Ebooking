from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import SignInViaEmailForm, SignUpForm, RestorePasswordViaEmailOrUsernameForm
from django.contrib.messages import get_messages
from .models import Profile
from .views import LogInView, RestorePasswordView, ChangeProfileView, ChangePasswordView




User = get_user_model()


class SignInViaEmailFormTest(TestCase):
    def setUp(self):
        self.credentials = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'test_password'
        }
        User.objects.create_user(**self.credentials)

    def test_sign_in_with_valid_credentials(self):
        form = SignInViaEmailForm(data=self.credentials)
        self.assertTrue(form.is_valid())

    def test_sign_in_with_invalid_credentials(self):
        credentials = self.credentials.copy()
        credentials['password'] = 'wrong_password'
        form = SignInViaEmailForm(data=credentials)
        self.assertFalse(form.is_valid())

    def test_sign_in_with_empty_data(self):
        form = SignInViaEmailForm(data={})
        self.assertFalse(form.is_valid())


class SignUpFormTest(TestCase):
    def test_sign_up_with_valid_data(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_sign_up_with_existing_email(self):
        User.objects.create_user(
            email='test@example.com',
            password='test_password',
            username='testuser'
        )
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())

    def test_sign_up_with_password_mismatch(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'wrong_password'
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())


class RestorePasswordViaEmailOrUsernameFormTest(TestCase):
    def setUp(self):
        self.credentials = {
            'email': 'test@example.com',
            'password': 'test_password',
             'username': 'testuser'
        }
        User.objects.create_user(**self.credentials)

    def test_restore_password_with_valid_email(self):
        form = RestorePasswordViaEmailOrUsernameForm(data={'email_or_username': 'test@example.com'})
        self.assertTrue(form.is_valid())

    def test_restore_password_with_valid_username(self):
        form = RestorePasswordViaEmailOrUsernameForm(data={'email_or_username': self.credentials['email']})
        self.assertTrue(form.is_valid())

    def test_restore_password_with_invalid_data(self):
        form = RestorePasswordViaEmailOrUsernameForm(data={'email_or_username': 'invalid@example.com'})
        self.assertFalse(form.is_valid())


# Views tests

class LogInViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        profile = Profile.objects.create(user=self.user, phone="123456")
        self.user.profile = profile
        self.user.save()

        self.client = Client()
        self.url = reverse('accounts:login')

    def test_login_success(self):
        data = {
            'username':'testuser', 
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, '/home')

    def test_login_failure(self):
        data = {
            'username':'testuser', 
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/home')

class GuestOnlyViewTestCase(TestCase):
    def test_redirect_authenticated_user(self):
        client = Client()
        user = User.objects.create_user('testuser', 'testuser@test.com', 'testpassword')
        profile = Profile.objects.create(user=user, phone="123456")
        user.profile = profile
        user.save()
        client.force_login(user)
        response = client.get(reverse('accounts:log_in'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_guest_user(self):
        client = Client()
        response = client.get(reverse('accounts:log_in'))
        self.assertEqual(response.status_code, 200)

class LogInViewTestCase(TestCase):
    def test_form_valid(self):
        user = User.objects.create_user('testuser', 'testuser@test.com', 'testpassword')
        profile = Profile.objects.create(user=user, phone="123456")
        user.profile = profile
        user.save()
        data = {
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }

        form = SignInViaEmailForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('accounts:log_in'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home')

    def test_form_invalid(self):
        data = {
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }
        form = SignInViaEmailForm(data=data)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('accounts:log_in'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/log-in/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '  Credențialele introduse sunt greșite.')

class SignupViewTestCase(TestCase):
    def test_form_valid(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'phone': '1234567890'
        }
        response = self.client.post(reverse('accounts:sign_up'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Account created succcesfully! check email for more info!')

        user = User.objects.get(email='johndoe@test.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.profile.phone, '1234567890')

    def test_form_invalid(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'password1': 'testpassword',
            'password2': 'wrongpassword',
            'phone': '1234567890'
        }
        response = self.client.post(reverse('accounts:sign_up'), data=data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertIn('Parolele din cele două câmpuri trebuie să fie identice!', messages[0].message)