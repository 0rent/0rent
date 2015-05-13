from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.contrib import messages
from django.db.models import Count
from orentapp.models import Product, Use, User, Profil, Group
from orentapp.forms import ProductForm, ProductUpdateForm, AddUserToGroupForm
from orentapp.mixin import UserCanAccessProductMixin


# View Index
class Index(TemplateView):
    template_name = 'orentapp/index.html'


# View Product List
class ProductListView(ListView):
    model = Product
    # template_name = 'orentapp/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['form'] = ProductForm()
        context['public_product_list'] = Product.objects.filter(is_public=True)
        group_list = Group.objects.filter(user=self.request.user)
        context['private_product_list'] = Product.objects.filter(is_public=False, private_group=group_list)
        return context


# View Product Details
class ProductDetailView(UserCanAccessProductMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'orentapp/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['add_user_to_group_form'] = AddUserToGroupForm(instance = self.object.private_group)
        context['use_list'] = Use.objects.filter(product_id=self.kwargs['pk'])
        # Liste des propriétaire avec nombre d'utilisations
        context['owner_list'] = context['use_list'].values('user__username').annotate(
            counter=Count('user_id')).order_by('-counter')
        return context


# View Product Use
def ProductUseView(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.add_use_for(request.user)
    messages.success(request, "L'utilisation a été prise en compte")
    return redirect(reverse_lazy('product_detail', kwargs={'pk': product_id}))


# View Form Add Product
class ProductCreateView(CreateView):
    form_class = ProductForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.first_owner = user
        messages.success(self.request, "Le nouveau produit a été ajouté")
        return super(ProductCreateView, self).form_valid(form)

    def form_invalid(self, form):
        # Attention les erreurs du form ne seront pas affichées
        return HttpResponseRedirect(self.success_url)


# View Form Update Product
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # la fonction est-elle nécessaire pour afficher le message?
        messages.success(self.request, "Le produit a été mis à jour")
        return super(ProductUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)


# View AddUserToGroup
class AddUserToGroupView(UpdateView):
    model = Group
    form_class = AddUserToGroupForm

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.product.id})

    def form_valid(self, form):
        user = form.cleaned_data['user']
        group = self.object
        user.groups.add(group)
        messages.success(self.request, "L'utilisateur a bien été ajouté")
        return super(AddUserToGroupView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)
