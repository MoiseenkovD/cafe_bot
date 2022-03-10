from django.contrib import admin
from .models import Restaurants, Cities, Users


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'city_name',
        'phone_number',
        'address',
        'open_at',
        'close_at',
        'image',
        'rating',
        'is_delivery',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(RestaurantsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['city'].label_from_instance = lambda inst: f"{inst.name}"
        return form


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'city_name',
        'username',
        'chat_id',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(UsersAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['city'].label_from_instance = lambda inst: f"{inst.name}"
        return form

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

