import json

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token

from django.urls import reverse
from rest_framework import status

from .serializers import CustomUserSerializer
from accounts.models import CustomUser

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {'email': 'test_email@gmail.com',
                'first_name': 'Test_first_name',
                'last_name': 'Test_last_name',
                'position': 'Test_position',
                'password': 'test_password'}
        responce = self.client.post('api_auth', data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)


class loginTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='test_email_1@gmail.com',
                                         first_name='Test_first_name_1',
                                         last_name='Test_last_name_1',
                                         position='Test_position_1',
                                         password='test_password')
        self.user2 = User.objects.create(email='test_email_2@gmail.com',
                                         first_name='Test_first_name_2',
                                         last_name='Test_last_name_2',
                                         position='Test_position_2',
                                         password='test_password')
        self.token = Token.objects.create(user=self.user1)
        self.api_token_auth()

    def api_token_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_success(self):
        login_url = reverse('api_auth')
        data = {'email': self.user1.email,
                'password': self.user1.password}
        response = self.client.post(login_url, data)
        resp = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['message'], "Login Successful")

    def test_login_invalid(self):
        login_url = reverse('api_auth')
        data = {'email': self.user2.email,
                'password': self.user2.password}
        response = self.client.post(login_url, data)
        resp = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp['message'], "Login Invalid")

    def test_get_user_data_auth(self):
        profile_url = reverse('api/user/', kwargs={'pk': self.user1.id})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name', 'last_name'], self.user1.first_name, self.user1.last_name)

    def test_get_user_data_un_auth(self):
        profile_url = reverse('api/user/', kwargs={'pk': self.user2.id})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_data_auth(self):
        profile_url = reverse('api/user/', kwargs={'pk': self.user1.id})
        data = {'first_name': 'Test_first_name_update',
                'last_name': 'Test_last_name_update',
                'position': 'Test_position_update'}
        response = self.client.patch(profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.user1.id).first_name, 'Test_first_name_update')
        self.assertEqual(User.objects.get(id=self.user1.id).last_name, 'Test_last_name_update')
        self.assertEqual(User.objects.get(id=self.user1.id).position, 'Test_position_update')
