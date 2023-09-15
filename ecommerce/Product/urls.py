from django.urls import path,include
from . import views


urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('sizes/', views.SizeListView.as_view(), name='size_list'),
    path('size/<int:pk>/', views.SizeDetailView.as_view(), name='size_detail'),
    path('size/create/', views.SizeCreateView.as_view(), name='size_create'),
    path('size/update/<int:pk>/', views.SizeUpdateView.as_view(), name='size_update'),
    path('size/delete/<int:pk>/', views.SizeDeleteView.as_view(), name='size_delete'),

    path('colors/', views.ColorListView.as_view(), name='color_list'),
    path('color/<int:pk>/', views.ColorDetailView.as_view(), name='color_detail'),
    path('color/create/', views.ColorCreateView.as_view(), name='color_create'),
    path('color/update/<int:pk>/', views.ColorUpdateView.as_view(), name='color_update'),
    path('color/delete/<int:pk>/', views.ColorDeleteView.as_view(), name='color_delete'),

    path('prices/', views.PriceListView.as_view(), name='price_list'),
    path('prices/<int:pk>', views.PriceDetailView.as_view(), name='price_detail'),
    path('price/create/',views.PriceCreateView.as_view(), name='create_price'),
    path('price/delete/<int:pk>/',views.PriceDeleteView.as_view(), name='delete_price'),
    path('price/update/<int:pk>/',views.PriceUpdateView.as_view(), name='update_price'),
    path('price/create/',views.PriceCreateView.as_view(), name='create_price'),
    # path('au/', include('authapp.urls')),
    path('', views.PublicDashboard.as_view(), name='home'),

]
