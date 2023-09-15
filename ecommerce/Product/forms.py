from django import forms
from .models import Product, Category, Size, Color, Price


class ProductForm(forms.ModelForm):

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    
    color = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    
    size = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'images', 'category', 'color', 'size']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__' 

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size    
        fields = '__all__'

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = '__all__'



