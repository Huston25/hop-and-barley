from django.db.models import Q, Avg
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_active=True)
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category_slug = self.request.GET.get('category')
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort', 'new')


        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)


        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(short_description__icontains=query) |
                Q(description__icontains=query)
            )
        if sort == "price_asc":
            queryset = queryset.order_by('price')
        elif sort == "price_desc":
            queryset = queryset.order_by('-price')
        elif sort == "new":
            queryset = queryset.order_by('-created_at')
        elif sort == "rating":
            queryset = queryset.annotate(rating=Avg('reviews__rating')).order_by('-rating')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['sort'] = self.request.GET.get('sort', 'new')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        return context