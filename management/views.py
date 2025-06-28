from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from .decorators import is_manager
from store.models import Product, Category
from django.views.generic import ListView
# Create your views here.



@user_passes_test(is_manager)
def manager_vision(request):
    return render(request, 'management/manager_vision.html')

@permission_required('store_addproduct', raise_exception=True)
@permission_required('store_changeproduct', raise_exception=True)
@permission_required('store_deleteproduct', raise_exception=True)
def manage_product(request):
    return render(request, 'management/manage_products.html')

@permission_required('store_changecategory', raise_exception=True)
@permission_required('store_addcategory', raise_exception=True)
@permission_required('store_deletecategory', raise_exception=True)
def m_categories_list(request):
    pass

@permission_required('accounts_changeuser', raise_exception=True)
def m_users_list(request):
    pass

@permission_required('order_vieworder', raise_exception=True)
@permission_required('order_vieworderitem', raise_exception=True)
def m_orders_list(request):
    pass

class ManagerProductView(PermissionRequiredMixin, ListView):
    model = Product  # indica il modello da cui prendere i dati
    template_name = 'management/manage_products.html'  # il tuo template personalizzato
    context_object_name = 'products'
    permission_required = ['store_addproduct',
                           'store_changeproduct',
                           'store_deleteproduct']

    def get_queryset(self):
        queryset = Product.objects.filter()
        category_id=self.request.GET.get('category')
        name=self.request.GET.get('name')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context=super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context