from django.test import TestCase
from django.test import TestCase
from baza.form import RegisterForm
from django.urls import reverse
from django.contrib.auth.models import User

class TestCaseViewAccount(TestCase):
    
    
    def setUp(self) -> None:
        self.form_data={
            'username' : 'Говноед',
            'email' : 'emkall@gmail.com',
            'password1' : '12345678_',
            'password2' : '12345678_',
        }
    def test_register_view(self):
        RegisterForm(data=self.form_data)
        self.client.post(reverse('register'), data=self.form_data)
        user = User.objects.filter(username=self.form_data['username']).exists()
        self.assertTrue(user)
