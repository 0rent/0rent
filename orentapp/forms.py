import logging
from django import forms
from orentapp.models import Product, User
from django.contrib.auth.models import Group

LOGGER = logging.getLogger(__name__)


# Form add Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'cost', 'is_public', 'step']
        # exclude = ['first_owner'] # pour enlever le first owner
        # first_owner = user_id #comment récupérer l'utilisateur connecté?


# Form Update Product
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_public']


# Form Add User To Group
class AddUserToGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddUserToGroupForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
            queryset=User.objects.exclude(groups=self.instance), empty_label=None)
        LOGGER.info(self.instance)
        LOGGER.info(User.objects.exclude(groups=self.instance))

    class Meta:
        model = Group
        fields = []
    # user = forms.ModelChoiceField(queryset=User.objects.none())
