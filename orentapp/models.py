import decimal
from decimal import Decimal
from django.db import models, transaction
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Model Product
class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)
    # Coût de départ
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    # Date de publication
    post_date = models.DateField(auto_now_add=True)
    # Date de dernière modification
    update_date = models.DateField(auto_now=True)
    # Utilisateur qui a mis en ligne
    first_owner = models.ForeignKey(User)
    # TRUE = Public (affiché pour tout le monde) FALSE = Privé
    is_public = models.BooleanField(default=True)
    # Groupe dans le cas d'un produit privé
    private_group = models.OneToOneField(Group, null=True, blank=True)
    # Step = marche pour remboursement progressif
    step = models.DecimalField(max_digits=8, decimal_places=2,
                               null=True, blank=True)

    def __str__(self):
        return self.name

    # compte le nombre d'utilisation
    @property
    def nb_use(self):
        return self.use_set.count()

    # retourne le prix de la prochaine utilisation
    @property
    def price(self):
        nb_use = self.nb_use
        step = self.step
        cost = self.cost
        if step and nb_use * step < cost:
            price = step
        else:
            price = cost / (1 + nb_use)
            price = price.quantize(Decimal('0.01'), decimal.ROUND_UP)
        return price

    # rembourse les utilisateurs précedents
    def recompute_use_balances(self):
        nb_use = self.nb_use
        price = self.price
        step = self.step
        cost = self.cost
        if step:
            # l'utilisation ne suffit pas pour atteindre le cost
            if (nb_use + 1) * step < cost:
                # remboursement du first owner
                profil = self.first_owner.profil
                profil.balance = profil.balance + price
                profil.save()
            # l'utilisation permet d'atteindre le cost
            if nb_use * step < cost <= (nb_use + 1) * step:
                # remboursement du first owner jusqu'a atteindre le cost
                profil = self.first_owner.profil
                profil.balance = profil.balance + (cost - nb_use * step)
                profil.save()
            # l'utilisation précedente a permis d'atteindre le cost
            if (nb_use - 1) * step < cost <= nb_use * step:
                # remboursement des utilisateurs précedents
                # en prenant en compte l'excedent du passage du cost
                for use in self.use_set.all():
                    profil = use.user.profil
                    profil.balance = profil.balance + (step - price)
                    profil.save()
            # le cost a déjà été atteint depuis 2 utilisations ou +
            if cost <= (nb_use - 1) * step:
                # calcul du prix précedent
                previous_price = cost / (nb_use)
                previous_price = previous_price.quantize(Decimal('0.01'),decimal.ROUND_UP)
                # remboursement des utilisateurs précedents
                for use in self.use_set.all():
                    profil = use.user.profil
                    profil.balance = profil.balance + (previous_price - price)
                    profil.save()
        else:
            # le produit a déjà été utilisé
            if nb_use:
                # calcul du prix précedent
                previous_price = cost / (nb_use)
                previous_price = previous_price.quantize(Decimal('0.01'), decimal.ROUND_UP)
                # remboursement des utilisateurs précedents
                for use in self.use_set.all():
                    profil = use.user.profil
                    profil.balance = profil.balance + (previous_price - price)
                    profil.save()
            # le produit n'a jamais été utilisé
            else:
                # remboursement du first owner
                profil = self.first_owner.profil
                profil.balance = profil.balance + price
                profil.save()

    # Ajout complet d'une utilisation
    # (remboursement, maj balance utilisateur et création use)
    def add_use_for(self, user):
        with transaction.atomic():
            self.recompute_use_balances()
            profil = user.profil
            profil.balance = profil.balance - self.price
            profil.save()
            # use = Use(product = self, user= request.user)
            # use.save()
            self.use_set.create(user=user)


# Model Use
class Use(models.Model):
    #  related_name='uses' : uses à la place de use_set
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)


# Model Profil
class Profil(models.Model):
        user = models.OneToOneField(User)
        balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)


# Model PrivateGroup (Non utilisé)
class PrivateGroup(Group):
    product = models.ForeignKey(Product)


# SIGNAUX

# Création du groupe pour un nouveau produit
@receiver(post_save, sender=Product)
def create_group_for_product(sender, instance, created, **kwargs):

    if created:
        # product.check()
        group = Group(name='ppg@{}'.format(instance.id))
        group.save()

        instance.first_owner.groups.add(group)
        instance.private_group = group


# Création du profil pour un nouvel utilisateur
@receiver(post_save, sender=User)
def create_profil_for_user(sender, instance, created, **kwargs):

    if created:
        Profil.objects.create(user=instance)
