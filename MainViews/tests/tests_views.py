# from django.test import TestCase, Client
# from django.urls import reverse
# import json
#
#
# class TestViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.home = reverse('home')
#         self.contracts = reverse('contracts')
#         self.state_change = reverse('state_change')
#         self.revoke = reverse('revoke')
#         self.terminate = reverse('terminate')
#         self.org_request = reverse('org_request')
#         self.org_contracts = reverse('org_contracts')
#         self.release = reverse('release')
#         self.reject_req = reverse('reject_req')
#         self.accept_req = reverse('accept_req')
#         self.view_data = reverse('view_data')
#         self.recent_activity = reverse('recent_activity')
#         self.new_contract = reverse('new_contract')
#
#     def testing1(self):
#         response = self.client.get(self.home)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/home.html')
#
#     def testing2(self):
#         response = self.client.get(self.org_contracts)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/org_contracts.html')
#
#     def testing3(self):
#         response = self.client.get(self.state_change)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/state_change.html')
#
#     def testing4(self):
#         response = self.client.get(self.contracts)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/contracts.html')
#
#     def testing5(self):
#         response = self.client.get(self.revoke)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/contracts.html')
#
#     def testing6(self):
#         response = self.client.get(self.reject_req)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/contracts.html')
#
#     def testing7(self):
#         response = self.client.get(self.accept_req)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/contracts.html')
#
#     def testing8(self):
#         response = self.client.get(self.terminate)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/contracts.html')
#
#     def testing9(self):
#         response = self.client.get(self.release)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/contracts.html')
#
#     def testing10(self):
#         response = self.client.get(self.org_request)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/org_request.html')
#
#     def testing11(self):
#         response = self.client.get(self.state_change)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/state_change.html')
#
#     def testing12(self):
#         response = self.client.get(self.recent_activity)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'identity/recent_activity.html')
#
#
