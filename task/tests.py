# import datetime
#
# from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token
#
# from django.urls import reverse
# from rest_framework import status
#
# from task.models import Task
#
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class TaskTestCase(APITestCase):
#
#     def setUp(self):
#         self.user1 = User.objects.create(email='test_email_1@gmail.com',
#                                          first_name='Test_first_name_1',
#                                          last_name='Test_last_name_1',
#                                          position='Test_position_1',
#                                          password='test_password')
#         self.user2 = User.objects.create(email='test_email_2@gmail.com',
#                                          first_name='Test_first_name_2',
#                                          last_name='Test_last_name_2',
#                                          position='Test_position_2',
#                                          password='test_password')
#
#         self.token = Token.objects.create(user=self.user1)
#         client = APIClient()
#         client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.user1.save()
#
#         self.token = Token.objects.create(user=self.user1)
#         client = APIClient()
#         client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.user2.save()
#
#         self.data_time = datetime.datetime.today()
#         self.task1 = Task(user=self.user1,
#                           title='Test task1',
#                           description='Test description1',
#                           deadline_date=self.data_time,
#                           status='finished',
#                           priority='medium')
#         self.task2 = Task(user=self.user1,
#                           title='Test task2',
#                           description='Test description2',
#                           deadline_date=self.data_time,
#                           status='todo',
#                           priority='medium')
#         self.task1.save()
#         self.task1.save()
#
#     def test_task_list_auth_user(self):
#         list_url = reverse('task_router')
#         response = self.client.post(list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_task_list_un_auth_user(self):
#         list_url = reverse('task_router')
#         self.client.force_authenticate(user=None)
#         response = self.client.post(list_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_task_detail_at_user1(self):
#         list_url = reverse('task_router', kwargs={'pk': self.task1.pk})
#         data = {'email': self.user1.email,
#                 'password': self.user1.password}
#         response = self.client.post(list_url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_task_detail_at_user2(self):
#         list_url = reverse('task_router', kwargs={'pk': self.task2})
#         data = {'email': self.user2.email,
#                 'password': self.user2.password}
#         response = self.client.post(list_url, data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_search(self):
#         response = self.client.get(reverse('task_router') + '?search=task1')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'])
#
#     def test_search_none(self):
#         response = self.client.get(reverse('task_router') + '?search=task3')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'])
#
#     def test_important(self):
#         self.assertEqual(self.task1.importance, False)
#         response = self.client.post(reverse('task-task-importance', kwargs={'pk': self.task1.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task1.pk).importance, True)
#
#     def test_set_status_todo(self):
#         self.task1.status = 'finished'
#         self.assertEqual(self.task1.status, 'finished')
#         response = self.client.post(reverse('task-set-status-todo', kwargs={'pk': self.task1.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task1.pk).status, 'todo')
#
#     def test_set_status_in_progress(self):
#         self.assertEqual(self.task1.status, 'finished')
#         response = self.client.post(reverse('task-set-status-in-progress', kwargs={'pk': self.task1.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task1.pk).status, 'in_progress')
#
#     def test_set_status_blocked(self):
#         self.assertEqual(self.task1.status, 'finished')
#         response = self.client.post(reverse('task-set-status-blocked', kwargs={'pk': self.task1.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task1.pk).status, 'blocked')
#
#     def test_set_status_finished(self):
#         self.assertEqual(self.task2.status, 'todo')
#         response = self.client.post(reverse('task-set-status-finished', kwargs={'pk': self.task2.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task2.pk).status, 'finished')
#
#     def test_set_priority_as_low(self):
#         self.assertEqual(self.task2.priority, 'medium')
#         response = self.client.post(reverse('task-set-priority-low', kwargs={'pk': self.task2.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task2.pk).priority, 'low')
#
#     def test_set_priority_as_high(self):
#         self.assertEqual(self.task1.priority, 'medium')
#         response = self.client.post(reverse('task-set-priority-high', kwargs={'pk': self.task1.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Task.objects.get(id=self.task1.pk).priority, 'high')
#
#     def test_filter_todo(self):
#         response = self.client.get(reverse('task_router') + '?status=todo')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'])
#
#     def test_filter_in_progress(self):
#         response = self.client.get(reverse('task_router') + '?status=in_progress')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'])
#
#     def test_filter_blocked(self):
#         response = self.client.get(reverse('task_router') + '?status=blocked')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'])
#
#     def test_filter_finished(self):
#         response = self.client.get(reverse('task_router') + '?status=finished')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'])
