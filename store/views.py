from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, Category
from django.views.generic import ListView
# Create your views here.

class HomeView(ListView):
    model = Product  # indica il modello da cui prendere i dati
    template_name = 'store/home.html'  # il tuo template personalizzato
    context_object_name = 'products'  # variabile usata nel template ({{ products }})

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category_id=self.request.GET.get('category')
        min_price=self.request.GET.get('min_price')
        max_price=self.request.GET.get('max_price')
        name=self.request.GET.get('name')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context=super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def product_detail(request,product_id):
    product=Product.objects.get(pk=product_id)
    return render(request, 'store/product_detail.html', {"product":product})