from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_link', 'price', 'quantity', 'size', 'get_total_price']
    fields = ['product_link', 'price', 'quantity', 'size', 'get_total_price']
    
    def product_link(self, obj):
        if obj.product:
            url = reverse('admin:products_product_change', args=[obj.product.pk])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return "No product"
    product_link.short_description = "Product"
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = "Total"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'status', 'total_amount', 'items_count', 'created_at', 'status_badge']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['user__username', 'email', 'first_name', 'last_name', 'id']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'total_amount', 'items_summary']
    inlines = [OrderItemInline]
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount', 'items_summary')
        }),
        ('Customer Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def order_number(self, obj):
        return f"#{obj.id:06d}"
    order_number.short_description = "Order #"
    
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = "Customer"
    
    def items_count(self, obj):
        count = obj.items.count()
        return f"{count} item{'s' if count != 1 else ''}"
    items_count.short_description = "Items"
    
    def items_summary(self, obj):
        items = obj.items.all()[:3]
        summary = "<br>".join([f"• {item.quantity}x {item.product.name}" for item in items])
        if obj.items.count() > 3:
            summary += f"<br>• ... and {obj.items.count() - 3} more items"
        return mark_safe(summary)
    items_summary.short_description = "Items Summary"
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffeaa7',
            'processing': '#74b9ff',
            'shipped': '#a29bfe',
            'delivered': '#00b894',
            'cancelled': '#fab1a0'
        }
        color = colors.get(obj.status, '#ddd')
        return format_html(
            '<span style="background: {}; color: #333; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    # Custom actions
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.', messages.SUCCESS)
    mark_as_processing.short_description = "Mark as Processing"
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.', messages.SUCCESS)
    mark_as_shipped.short_description = "Mark as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.', messages.SUCCESS)
    mark_as_delivered.short_description = "Mark as Delivered"
