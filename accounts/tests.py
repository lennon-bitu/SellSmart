from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class AccountsUrlsTest(TestCase):

    #testando o pytest
    def test_the_pytest_is_ok(self):
        assert 1 == 1

    def test_login_url_is_correct(self):
        login_url = reverse('accounts:login/')
        self.assertEqual(login_url, 'accounts/login/')