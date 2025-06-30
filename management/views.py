from logging import raiseExceptions
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django_countries import countries
from order.models import Order, OrderItem
from .decorators import is_manager
from store.models import Product, Category
from accounts.models import CustomUser
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.db.models.functions import Concat
from django.db.models import Value
from django.db.models.functions import Lower
from django.db.models import Q
from django.contrib.auth.models import Group
# Create your views here.


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_vision(request):
    return render(request, 'management/manager_vision.html')

@permission_required('store_addproduct', raise_exception=True)
@permission_required('store_changeproduct', raise_exception=True)
@permission_required('store_deleteproduct', raise_exception=True)
def manage_product(request,product_id):
    product=Product.objects.get(id=product_id)
    if request.method=="POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category_id = request.POST.get('category')
        product.is_active = request.POST.get('is_active')=="on"
        product.quantity = request.POST.get('quantity')
        if 'front_image' in request.FILES:
            product.front_image = request.FILES['front_image']
        product.save()
        return redirect('manage_products')
    else:
        categories= Category.objects.all()
        return render(request,"management/product_edit.html",{'product':product,'categories':categories})

@permission_required('store_changecategory', raise_exception=True)
@permission_required('store_addcategory', raise_exception=True)
@permission_required('store_deletecategory', raise_exception=True)
def m_categories_list(request):
    if request.method=="POST":
        action=request.POST.get('action')
        name=request.POST.get('name')
        category_id=request.POST.get('category_id')

        if action=="add":
            if name:
                Category.objects.create(name=name)
                messages.success(request,'Category added')
        elif action=="update":
            if category_id:
                Category.objects.filter(id=category_id).update(name=name)
                messages.success(request,'Category changed')
        elif action=="delete":
            if category_id:
                no_categorized = Product.objects.filter(category_id=category_id).count()
                Category.objects.filter(id=category_id).delete()
                if no_categorized==0:
                    messages.success(request,'Category deleted. No products changed')
                elif no_categorized==1:
                    messages.success(request,f"Category deleted. Now {no_categorized} product have no category")
                else:
                    messages.success(request, f"Category deleted. Now {no_categorized} products have no category")
        return redirect('manage_categories')
    else:
        categories = Category.objects.all()
        return render(request,'management/manage_categories.html',{'categories':categories})

@permission_required('accounts_viewcustomuser', raise_exception=True)
@permission_required('accounts_changecustomuser', raise_exception=True)
@user_passes_test(is_manager)
def m_users(request):
    if request.method=="POST":
        user_id=request.POST.get('user_id')
        user=CustomUser.objects.get(id=user_id)
        action=request.POST.get('action')
        if request.user==user:
            messages.error(request,"You can't change your own role")
            return redirect('manage_users')

        if action=="make_manager":
            group = Group.objects.get(name='Manager')
            user.groups.clear()
            user.groups.add(group)
            messages.success(request, f"{user.username} è ora Manager")
        if action=="make_customer":
            group = Group.objects.get(name='Customer')
            user.groups.clear()
            user.groups.add(group)
            messages.success(request, f"{user.username} è ora Customer")
        return redirect('manage_users')
    else:
        users = CustomUser.objects.filter()
        context_name = request.GET.get('user_search')
        if context_name:
            users = CustomUser.objects.annotate(
                full_name_db=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(username__icontains=context_name) |
                Q(first_name__icontains=context_name) |
                Q(last_name__icontains=context_name) |
                Q(full_name_db__icontains=context_name)
            )
        return render(request,'management/manage_users.html',{'users':users,'searched':context_name})

class ManagerOrderView(PermissionRequiredMixin, ListView):
    model=Order
    template_name='management/manage_orders.html'
    context_object_name='orders'
    permission_required=['order_vieworder',
                         'order_vieworderitem',
                         'order_changeorder']

    def get_queryset(self):
        queryset = Order.objects.all()
        user_context=self.request.GET.get('user')
        product_name=self.request.GET.get('product')
        category_id=self.request.GET.get('category')
        country_code=self.request.GET.get('country')
        city=self.request.GET.get('city')

        if product_name:
            queryset=queryset.filter(items__product__name__icontains=product_name)
        if category_id:
            queryset=queryset.filter(items__product__category_id=category_id)
        if country_code:
            queryset = queryset.filter(shipment_country=country_code)
        if city:
            queryset = queryset.filter(Q(**{ 'shipment_city__icontains': city }))
        if user_context:
            queryset = queryset.annotate(
                full_name_db=Concat('customer__first_name', Value(' '), 'customer__last_name'),
            ).filter(
                Q(customer__username__icontains=user_context) |
                Q(customer__first_name__icontains=user_context) |
                Q(customer__last_name__icontains=user_context) |
                Q(full_name_db__icontains=user_context)
            )
        return queryset

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        used_codes = Order.objects.values_list('shipment_country', flat=True).distinct()
        used_countries = [(code, countries.name(code)) for code in used_codes if code]
        context['countries'] = list(used_countries)
        return context
def order_detail(request,order_id):
    order = Order.objects.get(id=order_id)
    order_status_choices=Order._meta.get_field('status').choices

    if request.method=="POST":
        new_status=request.POST.get('status')
        if new_status in dict(order_status_choices):
            order.status=new_status
            order.save()
            messages.success(request,f"Order status changed to {new_status}")
        else:
            messages.error(request,f"Invalid order status")
        return redirect('order_detail',order_id=order_id)
    else:
        return render(request,'management/order_detail.html',{'order':order,'status_choices':order_status_choices})
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