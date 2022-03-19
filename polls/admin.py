from django.contrib import admin

from .models import Food, Poll

# Register your models here.


# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(Food)
admin.site.register(Poll)
