# products/forms.py
from django import forms
from .models import Product, Category

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'available_sizes': forms.TextInput(attrs={
                'placeholder': 'Enter sizes separated by commas (e.g., S,M,L,XL)',
                'help_text': 'Available sizes for this product'
            }),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError("Stock cannot be negative")
        return stock