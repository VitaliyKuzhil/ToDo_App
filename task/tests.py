# from django.test import TestCase
# from rest_framework.test import APIRequestFactory
#
# from django.urls import reverse
# from rest_framework import status
#
# from serializers import TaskSerializer
# from task.models import Task
#
# from task.constants import TaskPriorityChoices, TaskStatusChoices
#
# import json
#
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class TaskTestCase(TestCase):
#     def test_task_list_auth_user(self):
#         list_url = reverse('task_router')
#         response = self.client.post(list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_task_list_un_auth_user(self):
#         list_url = reverse('task_router')
#         response = self.client.post(list_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_task_detail_auth_user(self):
#         list_url = reverse('task_router-detail', kwargs={'pk': 1})
#         response = self.client.post(list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_task_detail_un_auth_user(self):
#         list_url = reverse('task_router-detail', kwargs={'pk': 1})
#         response = self.client.post(list_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
