import decimal
from decimal import Decimal
from django.test import TestCase
from orentapp.models import Product, User, Profil, Use


class ProductMethodTests(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.user_1.profil.balance = self.user_1.profil.balance + 100
        self.user_2.profil.balance = self.user_2.profil.balance + 100
        self.product_1 = Product.objects.create(name='Product_1', description='',
                                                cost=decimal.Decimal('100'),
                                                first_owner=self.user_1)

    def test_product_first_price(self):
        self.assertEqual(self.product_1.price, 100)

    def test_product_after_1_use(self):
        self.product_1.add_use_for(self.user_2)
        self.assertEqual(self.product_1.price, 50)
        self.assertEqual(self.user_1.profil.balance, 200)
        self.assertEqual(self.user_2.profil.balance, 0)

    def test_product_after_2_use(self):
        self.product_1.add_use_for(self.user_1)
        self.assertEqual(self.product_1.price, 33.34)
        self.assertEqual(self.user_1.profil.balance, 150)
        self.assertEqual(self.user_2.profil.balance, 50)

    def test_product_after_3_use(self):
        self.product_1.add_use_for(self.user_2)
        self.assertEqual(self.product_1.price, 25)
        self.assertEqual(self.user_1.profil.balance, 166.66)
        self.assertEqual(self.user_2.profil.balance, 33.32)
