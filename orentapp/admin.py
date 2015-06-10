from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from orentapp.models import Product, Use, Profil, Ownership


# Profil Administration => Inline with User Administration
class ProfilAdmin(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profils'


# User Administration
class UserAdmin(UserAdmin):
    inlines = (ProfilAdmin, )


# Product Administration
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost', 'post_date', 'update_date', 'is_public', 'private_group')


# Use Administration
class UseAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'date')

# Ownership Administration
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ratio')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Use, UseAdmin)
admin.site.register(Ownership, OwnershipAdmin)
