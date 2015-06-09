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
        # product without step
        self.product_1 = Product.objects.create(name='Product_1', description='',
                                                cost=decimal.Decimal('100'),
                                                first_owner=self.user_1)
        # product with step which is a multiple of cost
        self.product_2 = Product.objects.create(name='Product_2', description='',
                                                cost=decimal.Decimal('100'),
                                                first_owner=self.user_1,
                                                step=20)
        # product with step which is not a multiple of cost
        self.product_3 = Product.objects.create(name='Product_3', description='',
                                                cost=decimal.Decimal('100'),
                                                first_owner=self.user_1,
                                                step=35)

# MAIN FUNCTION recompute_use balance TEST
# GENERAL CASE
    def test_product_first_price(self):
        self.assertEqual(self.product_1.price, 100)

    def test_product_after_1_use(self):
        self.product_1.add_use_for(self.user_2)
        self.assertEqual(self.product_1.price, 50)
        self.assertEqual(self.user_1.profil.balance, 200)
        self.assertEqual(self.user_2.profil.balance, 0)

    def test_product_after_2_use_with_fo_1(self):
        self.product_1.add_use_for(self.user_1)
        self.product_1.add_use_for(self.user_2)
        # Reload users to get fresh profiles / balances.
        self.user_1 = User.objects.get(id=self.user_1.id)
        self.assertEqual(self.product_1.price, decimal.Decimal('33.34'))
        self.assertEqual(self.user_1.profil.balance, 150)
        self.assertEqual(self.user_2.profil.balance, 50)

    def test_product_after_2_use_with_fo_2(self):
        self.product_1.add_use_for(self.user_2)
        self.product_1.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_1.price, decimal.Decimal('33.34'))
        self.assertEqual(self.user_1.profil.balance, 150)
        self.assertEqual(self.user_2.profil.balance, 50)

    def test_product_after_2_use_without_fo(self):
        self.product_1.add_use_for(self.user_2)
        self.product_1.add_use_for(self.user_2)
        self.assertEqual(self.product_1.price, decimal.Decimal('33.34'))
        self.assertEqual(self.user_1.profil.balance, 200)
        self.assertEqual(self.user_2.profil.balance, 0)

    def test_product_after_3_use(self):
        self.product_1.add_use_for(self.user_2)
        self.product_1.add_use_for(self.user_2)
        self.product_1.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_1.price, 25)
        self.assertEqual(self.user_1.profil.balance, decimal.Decimal('166.66'))
        self.assertEqual(self.user_2.profil.balance, decimal.Decimal('33.32'))

# TEST CASE : cost IS A MULTIPLE OF step
    def test_product_step_multiple_first_price(self):
        self.assertEqual(self.product_2.price, 20)

    def test_product_step_multiple_after_1_use(self):
        # function case : this use si not sufficient to obtain cost
        self.product_2.add_use_for(self.user_2)
        self.assertEqual(self.product_2.price, 20)
        self.assertEqual(self.user_1.profil.balance, 120)
        self.assertEqual(self.user_2.profil.balance, 80)

    def test_product_step_multiple_after_5_use(self):
        # function case : this use allow to have cost
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_1)
        self.product_2.add_use_for(self.user_1)
        self.product_2.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_2.price, decimal.Decimal('16.67'))
        self.assertEqual(self.user_1.profil.balance, 140)
        self.assertEqual(self.user_2.profil.balance, 60)

    def test_product_step_multiple_after_6_use(self):
        # function case : previous use allow to have cost
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_1)
        self.product_2.add_use_for(self.user_1)
        self.product_2.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_2.price, decimal.Decimal('14.29'))
        self.assertEqual(self.user_1.profil.balance, decimal.Decimal('149.99'))
        self.assertEqual(self.user_2.profil.balance, decimal.Decimal('49.99'))

    def test_product_step_multiple_after_7_use(self):
        # function case : cost obtained 2 uses before
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_2)
        self.product_2.add_use_for(self.user_1)
        self.product_2.add_use_for(self.user_1)
        self.product_2.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_2.price, decimal.Decimal('12.50'))
        self.assertEqual(self.user_1.profil.balance, decimal.Decimal('157.13'))
        self.assertEqual(self.user_2.profil.balance, decimal.Decimal('42.84'))

# TEST CASE : cost IS NOT A MULTIPLE OF step
    def test_product_step_not_multiple_first_price(self):
        self.assertEqual(self.product_3.price, 35)

    def test_product_step_not_multiple_after_1_use(self):
        # function case : this use si not sufficient to obtain cost
        self.product_3.add_use_for(self.user_2)
        self.assertEqual(self.product_3.price, 35)
        self.assertEqual(self.user_1.profil.balance, 135)
        self.assertEqual(self.user_2.profil.balance, 65)

    def test_product_step_not_multiple_after_3_use(self):
        # function case : this use allow to have cost
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_3.price, 25)
        self.assertEqual(self.user_1.profil.balance, 165)
        self.assertEqual(self.user_2.profil.balance, 30)

    def test_product_step_not_multiple_after_4_use(self):
        # function case : previous use allow to have cost
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_1)
        self.product_3.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_3.price, 20)
        self.assertEqual(self.user_1.profil.balance, 150)
        self.assertEqual(self.user_2.profil.balance, 50)

    def test_product_step_not_multiple_after_5_use(self):
        # function case : cost obtained 2 uses before
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_2)
        self.product_3.add_use_for(self.user_1)
        self.product_3.add_use_for(self.user_1)
        self.user_2 = User.objects.get(id=self.user_2.id)
        self.assertEqual(self.product_3.price, decimal.Decimal('16.67'))
        self.assertEqual(self.user_1.profil.balance, 160)
        self.assertEqual(self.user_2.profil.balance, 40)
