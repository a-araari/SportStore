from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .forms import ProductAdminForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def product_count(self, obj):
        count = obj.product_set.count()
        return f"{count} product{'s' if count != 1 else ''}"
    product_count.short_description = "Products"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'image_preview', 'stock_status', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'stock']
    list_editable = ['price', 'stock', 'is_active']
    search_fields = ['name', 'description', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    actions = ['mark_as_active', 'mark_as_inactive', 'mark_as_out_of_stock', 'duplicate_product']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'available_sizes'),
            'description': 'Set the price and manage inventory'
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload product images'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Control product visibility'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return format_html('<div style="width: 100px; height: 100px; background: #f0f0f0; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: #666;">No image</div>')
    image_preview.short_description = "Preview"
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif obj.stock <= 5:
            return format_html('<span style="color: orange; font-weight: bold;">Low Stock</span>')
        else:
            return format_html('<span style="color: green;">In Stock</span>')
    stock_status.short_description = "Stock Status"
    
    # Custom actions
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products marked as active.', messages.SUCCESS)
    mark_as_active.short_description = "Mark selected products as active"
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products marked as inactive.', messages.SUCCESS)
    mark_as_inactive.short_description = "Mark selected products as inactive"
    
    def mark_as_out_of_stock(self, request, queryset):
        updated = queryset.update(stock=0)
        self.message_user(request, f'{updated} products marked as out of stock.', messages.SUCCESS)
    mark_as_out_of_stock.short_description = "Mark selected products as out of stock"
    
    def duplicate_product(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (Copy)"
            product.slug = f"{product.slug}-copy"
            product.save()
        count = queryset.count()
        self.message_user(request, f'{count} products duplicated successfully.', messages.SUCCESS)
    duplicate_product.short_description = "Duplicate selected products"