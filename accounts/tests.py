from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.urls import reverse
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()


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
        self.user1.save()
        self.user2.save()

        client = APIClient()
        self.token = Token.objects.create(user=self.user1)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_success(self):
        login_url = reverse('api_auth:login')
        data = {'email': self.user1.email,
                'password': self.user1.password}
        response = self.client.post(login_url, data)
        resp = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user1.first_name)

    def test_login_invalid(self):
        login_url = reverse('api_auth:login')
        data = {'email': self.user2.email,
                'password': self.user2.password}
        response = self.client.post(login_url, data)
        resp = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp['message'], "Login Invalid")

    def test_get_user_data_auth(self):
        profile_url = reverse('user_router:user_profile', kwargs={'pk': self.user1})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name', 'last_name'], self.user1.first_name, self.user1.last_name)

    def test_get_user_data_un_auth(self):
        profile_url = reverse('user_router', kwargs={'pk': self.user2.id})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_data_auth(self):
        profile_url = reverse('user_router', kwargs={'pk': self.user1.id})
        data = {'first_name': 'Test_first_name_update',
                'last_name': 'Test_last_name_update',
                'position': 'Test_position_update'}
        response = self.client.patch(profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=self.user1.id)
        self.assertEqual(user.first_name, 'Test_first_name_update')
        self.assertEqual(user.last_name, 'Test_last_name_update')
        self.assertEqual(user.position, 'Test_position_update')
