from django.db import models
from django.utils.html import mark_safe
from bot_app import model_choices as mch
from cafe_bot import settings


class Cities(models.Model):
    name = models.CharField(max_length=155)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'Cities'
        db_table = "cities"


class Restaurants(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    open_at = models.CharField(max_length=20)
    close_at = models.CharField(max_length=20)
    photo = models.FileField(upload_to='photos')
    rating = models.FloatField()
    is_delivery = models.BooleanField()
    lat = models.FloatField(default=None, blank=True, null=True)
    lng = models.FloatField(default=None, blank=True, null=True)
    city = models.ForeignKey('bot_app.Cities', on_delete=models.CASCADE, verbose_name='city')

    def city_name(self):
        return self.city.name

    def image(self):
        if self.photo != '':
            return mark_safe('<img src="/%s" width="50" height="40" />' % (self.photo))

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'Restaurants'
        db_table = "restaurants"


class Users(models.Model):
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    username = models.CharField(max_length=100, default=None, blank=True, null=True)
    chat_id = models.CharField(max_length=20)
    city = models.ForeignKey('bot_app.Cities',
                             on_delete=models.CASCADE,
                             verbose_name='city',
                             default=None,
                             blank=True,
                             null=True)

    def city_name(self):
        if self.city is None:
            return '-'
        return self.city.name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'
        db_table = "users"


class RestaurantsMenu(models.Model):
    restaurant = models.ForeignKey(
        'bot_app.Restaurants',
        on_delete=models.CASCADE,
        verbose_name='restaurant',
        default=None,
        blank=True,
        null=True
    )
    image = models.FileField(upload_to='photos')
    type = models.CharField(max_length=10, choices=mch.TYPE_CHOICES, default=mch.MENU)

    def restaurant_name(self):
        return self.restaurant.name

    def photo(self):
        if self.image != '':
            return mark_safe('<img src="/%s" width="50" height="40" />' % (self.image))

    class Meta:
        verbose_name = 'restaurant_menu'
        verbose_name_plural = 'Restaurants Menu'
        db_table = "restaurants_menu"
