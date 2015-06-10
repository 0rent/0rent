import decimal
import logging
from decimal import Decimal
from django.db import models, transaction
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save  # pre_save,
from django.dispatch import receiver

LOGGER = logging.getLogger(__name__)


# Model Product
class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)
    # Starting cost
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    # Publication date
    post_date = models.DateField(auto_now_add=True)
    # Last modification date
    update_date = models.DateField(auto_now=True)
    # Users who finance or make the product
    first_owners = models.ManyToManyField(User, through='Ownership')
    is_public = models.BooleanField(default=True)
    # Group (in case of private product)
    private_group = models.OneToOneField(Group, null=True, blank=True)
    # Step for progressive refund
    step = models.DecimalField(max_digits=8, decimal_places=2,
                               null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def nb_use(self):
        return self.use_set.count()

    @property
    def price(self):
        # next use price
        nb_use = self.nb_use
        step = self.step
        cost = self.cost
        if step and nb_use * step < cost:
            price = step
        else:
            price = cost / (1 + nb_use)
            price = price.quantize(Decimal('0.01'), decimal.ROUND_UP)
        return price

    def recompute_use_balances(self, hint_user=None):
        """
        Main function of orent app
        refund owners and/or previous users taking care that :
        - owners have been payed back as soon as possible
        - every users spend the same amount of money by use.
        """
        nb_use = self.nb_use
        price = self.price
        step = self.step
        cost = self.cost

        # If caller gives us a user on which to work on,
        # avoid a back-and-forth trip on the database by using
        # it directly. Problem spotted during test-cases write.
        hint_user_id = None if hint_user is None else hint_user.id

        def impact_all_uses(what):
            """ Refund all previous users"""

            for use in self.use_set.all():
                if use.user_id == hint_user_id:
                    profil = hint_user.profil
                else:
                    profil = use.user.profil

                profil.balance += what
                profil.save()

        def impact_first_owner(what):
            """ Refund first owners. """

            if self.first_owner_id == hint_user_id:
                profil = hint_user.profil
            else:
                profil = self.first_owner.profil

            profil.balance += what
            profil.save()

        if step:

            # use don't allow to reach cost
            if (nb_use + 1) * step < cost:
                # for ownership in self.ownership_set.all()
                    # ratio = ownership.ratio
                    # total_refunded = nb_use * price * ratio
                    # total_refunded = total_refunded.quantize(Decimal('0.01'), decimal.ROUND_DOWN)
                    # total_refund = (nb_use + 1)* price * ratio
                    # total_refund = total_refund.quantize(Decimal('0.01'), decimal.ROUND_DOWN)
                    # what = total_refund - total_refunded
                    # impact_first_owner(what)
                impact_first_owner(price)

            # use allow to reach cost
            if nb_use * step < cost <= (nb_use + 1) * step:
                # for ownership in self.ownership_set.all()
                    # ratio = ownership.ratio
                    # total_refunded = nb_use * price * ratio
                    # total_refunded = total_refunded.quantize(Decimal('0.01'), decimal.ROUND_DOWN)
                    # total_refund = cost * ratio
                    # total_refund = total_refund.quantize(Decimal('0.01'), decimal.ROUND_DOWN)
                    # what = total_refund - total_refunded
                    # impact_first_owner(what)
                # refund first owner up to the cost
                impact_first_owner(cost - nb_use * step)

            # previous use allowed to reach cost
            if (nb_use - 1) * step < cost <= nb_use * step:
                # refund previous users
                # taking into account overage of cost passing
                impact_all_uses(step - price)

            # cost have been reached for 2 uses or more
            if cost <= (nb_use - 1) * step:
                previous_price = cost / nb_use
                previous_price = previous_price.quantize(Decimal('0.01'),
                                                         decimal.ROUND_UP)
                impact_all_uses(previous_price - price)
        else:
            if nb_use:
                # product have been used
                previous_price = cost / nb_use
                previous_price = previous_price.quantize(Decimal('0.01'),
                                                         decimal.ROUND_UP)
                impact_all_uses(previous_price - price)
            else:
                # product have never been used
                impact_first_owner(price)

    # complete add of a use
    def add_use_for(self, user):
        with transaction.atomic():
            self.recompute_use_balances(hint_user=user)
            # HEADS UP: user needs to be created *AFTER* recomputation
            #           for the new user not to be refunded with his/her
            #           own user.
            profil = user.profil
            profil.balance -= self.price
            profil.save()
            self.use_set.create(user=user)
"""
    def check(self):
        # Vérifier private_group
        factory_private_group_name = 'ppg@{}'.format(self.id)

        if self.private_group:
            group = self.private_group
            if group.name != factory_private_group_name:
                group.name = factory_private_group_name
                group.save()

        else:
            group = Group(name=factory_private_group_name)
            group.save()
            self.first_owner.groups.add(group)
            self.private_group = group
"""


class Use(models.Model):
    #  related_name='uses' : uses à la place de use_set
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)


class Profil(models.Model):
        user = models.OneToOneField(User)
        balance = models.DecimalField(max_digits=8,
                                      decimal_places=2,
                                      default=0)


class Ownership(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    ratio = models.DecimalField(max_digits=3, decimal_places=2)


# SIGNAUX

# Group creation for new product
@receiver(post_save, sender=Product)
def create_group_for_product(sender, instance, created, **kwargs):

    if created:
        # product.check()
        group = Group(name='ppg@{}'.format(instance.id))
        group.save()

        instance.first_owner.groups.add(group)
        instance.private_group = group


# Profil creation for new user
@receiver(post_save, sender=User)
def create_profil_for_user(sender, instance, created, **kwargs):

    if created:
        Profil.objects.create(user=instance)
