from django.contrib import admin
from .models import User, ContentItem, Category


# Register the User model (if it's a custom model)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'address', 'city', 'state', 'country', 'pincode']
    search_fields = ['username', 'email', 'phone']
    ordering = ['username']

admin.site.register(User, UserAdmin)

# Register the ContentItem model
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'summary']  # assuming you have a 'created_at' field
    search_fields = ['title', 'author__username', 'summary']
    list_filter = ['author', 'categories']

admin.site.register(ContentItem, ContentItemAdmin)

# Register the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
