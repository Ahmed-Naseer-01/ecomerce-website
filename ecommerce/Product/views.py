import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Category, Color, Size, Price
from .forms import ProductForm, CategoryForm, ColorForm, SizeForm, PriceForm
from django.forms import inlineformset_factory
logger = logging.getLogger(__name__)
from authapp.views import AdminGroupMixin
from django.contrib.auth.mixins import PermissionRequiredMixin



def public_product_list(request):
    products = Product.objects.all()
    return render(request, 'Product/public_dashboard.html', {'products': products})

class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'Product/product_list.html'
    context_object_name = 'products'
    ordering = ['name']
    permission_required = 'Product.view_product'

#  PermissionRequiredMixin, 
class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = 'Product/product_detail.html'
    context_object_name = 'product_details'
    permission_required = 'Product.view_product'

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'Product/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'Product.add_product'

    def form_valid(self, form):
        # Additional processing if needed
        form.save()
        logger.info('Product created successfully')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'Product/product_form.html'
    success_url = reverse_lazy('product_list')
    context_object_name = 'product'
    permission_required = 'Product.change_product'

    def form_valid(self, form):
        logger.info('Product updated successfully')
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        product = self.get_object()
        initial['categories'] = product.category.all()
        initial['colors'] = product.color.all()
        initial['sizes'] = product.size.all()
        return initial


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'Product/delete_product.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'Product.delete_product'


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Category
    template_name = 'Product/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']
    permission_required = 'Product.view_category'


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Category
    template_name = 'Product/category_detail.html'
    context_object_name = 'category'
    permission_required = 'Product.view_category'


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Product/create_category.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'Product.add_category'  


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'Product/update_category.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'Product.change_category'   
    
    def form_valid(self, form):
        logger.info('Category updated successfully')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'Product/delete_category.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'Product.delete_category'  


class SizeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Size
    template_name = 'Product/size_list.html'
    context_object_name = 'sizes'
    permission_required = 'Product.view_size'


class SizeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Size
    template_name = 'Product/size_detail.html'
    context_object_name = 'size_details'
    permission_required = 'Product.view_size'


class SizeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Size
    form_class = SizeForm
    template_name = 'Product/size_form.html'
    success_url = reverse_lazy('size_list')
    permission_required = 'Product.add_size'


class SizeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Size
    form_class = SizeForm
    template_name = 'Product/size_form.html'
    success_url = reverse_lazy('size_list')
    permission_required = 'Product.change_size'
    
    def form_valid(self, form):
        logger.info('Size updated successfully')
        return super().form_valid(form)
        


class SizeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Size
    template_name = 'Product/delete_size.html'
    success_url = reverse_lazy('size_list')
    permission_required = 'Product.delete_size'


class ColorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Color
    template_name = 'Product/color_list.html'
    context_object_name = 'colors'
    permission_required = 'Product.view_color'


class ColorDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Color
    template_name = 'Product/color_detail.html'
    context_object_name = 'color_details'
    permission_required = 'Product.view_color'


class ColorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Color
    form_class = ColorForm
    template_name = 'Product/color_form.html'
    success_url = reverse_lazy('color_list')
    permission_required = 'Product.add_color'


class ColorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Color
    form_class = ColorForm
    template_name = 'Product/color_form.html'
    success_url = reverse_lazy('color_list')
    permission_required = 'Product.change_color'
    
    def form_valid(self, form):
        logger.info('Color updated successfully')
        return super().form_valid(form)

class ColorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Color
    template_name = 'Product/delete_Color.html'
    success_url = reverse_lazy('color_list')
    permission_required = 'Product.delete_color'


class PriceDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Price
    template_name = 'Product/price_detail.html'
    context_object_name = 'price_details'
    permission_required = 'Product.view_price'

class PriceListView(ListView):
    model = Price
    template_name = 'Product/price_list.html'
    context_object_name = 'Prices'
    permission_required = 'Product.view_price'


class PriceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Price
    form_class = PriceForm
    template_name = 'Product/price_form.html'
    success_url = reverse_lazy('price_list')
    permission_required = 'Product.add_price'


class PriceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Price
    form_class = PriceForm
    template_name = 'Product/price_form.html'
    permission_required = 'Product.change_price'


class PriceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Price
    template_name = 'Product/delete_price.html'
    success_url = reverse_lazy('price_list')
    permission_required = 'Product.delete_price'

class AdminView(TemplateView):
    template_name = "Product/admin.html"

class PublicDashboard(TemplateView):
    template_name = 'public_dashboard.html'




















# class DashboardView(View):
#     template_name = 'Product/dashboard.html'

#     def get(self, request):
#         # Display a form to create a new product
#         form = ProductForm()
#         products = Product.objects.all()
#         return render(request, self.template_name, {'form': form, 'products': products})

#     def post(self, request):
#         # Handle form submission for creating a new product
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = form.save()
#             logger.info('Product created successfully')
#             return redirect('dashboard')

#         # If form is not valid, redisplay the dashboard with errors
#         products = Product.objects.all()
#         return render(request, self.template_name, {'form': form, 'products': products})

#     def put(self, request, pk):
#         # Handle form submission for updating an existing product
#         product = get_object_or_404(Product, pk=pk)
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             logger.info('Product updated successfully')
#         return redirect('dashboard')

#     def delete(self, request, pk):
#         # Handle product deletion
#         product = get_object_or_404(Product, pk=pk)
#         product.delete()
#         logger.info('Product deleted successfully')
#         return redirect('dashboard')























































# class CRUDView(View):
#     template_name = 'Product/crud_template.html'

#     def get(self, request, *args, **kwargs):
#         products = Product.objects.all()
#         # categories = Category.objects.all()
#         # colors = Color.objects.all()
#         # sizes = Size.objects.all()
#         # prices = Price.objects.all()
#         return render(request, self.template_name, {
#             'products': products,
#             # 'categories': categories,
#             # 'colors': colors,
#             # 'sizes': sizes,
#             # 'prices': prices,
#             'product_form': ProductForm(),  
#             # 'category_form': CategoryForm(),  
#             # 'color_form': ColorForm(),  
#             # 'size_form': SizeForm(),  
#             # 'price_form': PriceForm(),  
#         })

#     def post(self, request, *args, **kwargs):
#         if 'create_product' in request.POST:
#             product_form = ProductForm(request.POST, request.FILES)
#             if product_form.is_valid():
#                 product_form.save()
#                 return redirect(reverse_lazy('crud_view'))


#         products = Product.objects.all()
#         categories = Category.objects.all()
#         colors = Color.objects.all()
#         sizes = Size.objects.all()
#         prices = Price.objects.all()
#         return render(request, self.template_name, {
#             'products': products,
#             'categories': categories,
#             'colors': colors,
#             'sizes': sizes,
#             'prices': prices,
#             'product_form': ProductForm(),
#             'category_form': CategoryForm(),
#             'color_form': ColorForm(),
#             'size_form': SizeForm(),
#             'price_form': PriceForm(),
#         })
    

# class PriceViewsMixin:
#     model = Price

#     # Detail View
#     template_name_detail = 'Product/price_detail.html'
#     context_object_name_detail = 'price_details'

#     # List View
#     template_name_list = 'Product/price_list.html'
#     context_object_name_list = 'Prices'

#     # Create View
#     template_name_create = 'Product/price_form.html'
#     form_class_create = PriceForm
#     success_url_create = reverse_lazy('price_list')

#     # Update View
#     template_name_update = 'Product/price_form.html'
#     form_class_update = PriceForm

#     # Delete View
#     template_name_delete = 'Product/delete_price.html'
#     success_url_delete = reverse_lazy('price_list')

# class PriceDetailView(PriceViewsMixin, DetailView):
#     template_name = PriceViewsMixin.template_name_detail
#     context_object_name = PriceViewsMixin.context_object_name_detail

# class PriceListView(PriceViewsMixin, ListView):
#     template_name = PriceViewsMixin.template_name_list
#     context_object_name = PriceViewsMixin.context_object_name_list

# class PriceCreateView(PriceViewsMixin, CreateView):
#     template_name = PriceViewsMixin.template_name_create
#     form_class = PriceViewsMixin.form_class_create
#     success_url = PriceViewsMixin.success_url_create

# class PriceUpdateView(PriceViewsMixin, UpdateView):
#     template_name = PriceViewsMixin.template_name_update
#     form_class = PriceViewsMixin.form_class_update

# class PriceDeleteView(PriceViewsMixin, DeleteView):
#     template_name = PriceViewsMixin.template_name_delete
#     success_url = PriceViewsMixin.success_url_delete