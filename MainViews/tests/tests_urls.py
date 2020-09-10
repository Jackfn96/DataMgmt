# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from MainViews.views import contracts, home, view_data, new_contract, state_change, revoke, org_contracts, org_request, \
#     accept_req, reject_req, release, recent_activity, terminate,
#
# class TestUrls(SimpleTestCase):
#
#     def test_check(self):
#         url = reverse('contracts')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, contracts)
#
#     def test_check2(self):
#         url = reverse('home')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, home)
#
#     def test_check3(self):
#         url = reverse('view_data')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, view_data)
#
#     def test_check4(self):
#         url = reverse('new_contract')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, new_contract)
#
#     def test_check5(self):
#         url = reverse('state_change')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, state_change)
#
#     def test_check6(self):
#         url = reverse('terminate')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, terminate)
#
#     def test_check7(self):
#         url = reverse('reject_req')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, reject_req)
#
#     def test_check8(self):
#         url = reverse('accept_req')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, accept_req)
#
#     def test_check9(self):
#         url = reverse('revoke')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, revoke)
#
#     def test_check10(self):
#         url = reverse('release')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, release)
#
#     def test_check11(self):
#         url = reverse('org_contracts')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, org_contracts)
#
#     def test_check12(self):
#         url = reverse('org_request')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, org_request)
#
#     def test_check13(self):
#         url = reverse('recent_activity')
#         print(resolve(url))
#         self.assertEquals(resolve(url).func, recent_activity)