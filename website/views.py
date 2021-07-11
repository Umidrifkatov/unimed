from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from core.models import *
from website.forms import OrderForm, ContactRequestForm


class HomePage(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['faqs'] = FAQ.objects.all()
        context['feedbacks'] = Feedback.objects.all()
        return context

def ProductList(request):
    products = Product.objects.filter(name_search__icontains=request.GET.get('search').lower())
    context = {
        "products":products,
    }
    return render(request, "pages/products.html", context)


class CategoryListPage(ListView):
    model = ParentCategory
    template_name = 'pages/category-list.html'
    context_object_name = 'categories'


class CategoryDetailPage(DetailView):
    model = Category
    template_name = 'pages/category-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        return context


class ProductDetailPage(DetailView):
    model = Product
    template_name = 'pages/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        return context


class ProductOrderPage(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'pages/order-page.html'
    success_url = '/orderSuccess/'

    def form_valid(self, form):
        form.instance.chosen_product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['product'] = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return context


class OrderSuccessPage(TemplateView):
    template_name = 'pages/order-success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        return context


class ContactRequestFormHandler(CreateView):
    model = ContactRequest
    form_class = ContactRequestForm
    success_url = '/contactRequestSuccess/'


class ContactRequestSuccessPage(TemplateView):
    template_name = 'pages/contact-request-success.html'



def Cooperate(request):
    form = ContactRequestForm
    context =  {
        "form": form
    }
    return render(request, 'core/cooperation.html', context)