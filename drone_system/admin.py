from django.contrib import admin
from .models import locations, routes, drones, world_data, future_bookings


# Register your models here.
admin.site.register(locations)
admin.site.register(routes)
admin.site.register(drones)
admin.site.register(world_data)
admin.site.register(future_bookings)
