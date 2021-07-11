from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from website import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('search/', views.ProductList, name='search'),

    path('category/', views.CategoryListPage.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailPage.as_view(), name='category-detail'),
    path('products/<slug:slug>/', views.ProductDetailPage.as_view(), name='product-detail'),
    path('products/<slug:slug>/order/', views.ProductOrderPage.as_view(), name='product-order'),
    path('contactRequest/', views.ContactRequestFormHandler.as_view(), name='contact-request'),
    path('orderSuccess/', views.OrderSuccessPage.as_view(), name='order-success'),
    path('contactRequestSuccess/', views.OrderSuccessPage.as_view(), name='contact-request-success'),
    path('cooperate/', views.Cooperate, name='cooperate')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
