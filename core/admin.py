from django.contrib import admin
from core.models import *

admin.site.register(ParentCategory)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


admin.site.register(Category, CategoryAdmin)

admin.site.register(ProductManufacturer)

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_search',)
    list_filter = ('category', 'manufacturer',)
    prepopulated_fields = {
        'slug': ('name',),
    }
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_handled')


admin.site.register(Order, OrderAdmin)

admin.site.register(FAQ)
admin.site.register(Feedback)
admin.site.register(ContactRequest)








class TuserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'step', 'phone',)

admin.site.register(Tuser, TuserAdmin)