from django.db import models


# Create your models here.
class locations(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.TextField()
    city = models.ForeignKey('cities', models.PROTECT)
    intercity = models.BooleanField()

    def __str__(self):
        return self.location + ", " + (cities.objects.filter(id=self.city_id)[0]).city


class cities(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.TextField()


class routes(models.Model):
    id = models.AutoField(primary_key=True)
    distance = models.PositiveSmallIntegerField()
    city_a = models.ForeignKey('locations', models.PROTECT, related_name='city_b')
    city_b = models.ForeignKey('locations', models.PROTECT, related_name='city_a')


class drones(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey('locations', models.PROTECT)
    job = models.BooleanField()
    user = models.ForeignKey('user_system.users', models.SET(0), null=True)
    route = models.ForeignKey('routes', models.PROTECT, null=True)
    job_start_time = models.DateTimeField(null=True)
    job_duration = models.PositiveIntegerField(null=True)
    job_finish_time = models.DateTimeField(null=True)
    origin = models.ForeignKey('locations', models.PROTECT, null=True, related_name='destination_id')
    destination = models.ForeignKey('locations', models.PROTECT, null=True, related_name='origin_id')
    future_booking = models.ForeignKey('future_bookings', models.SET_NULL, null=True)


class bases(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey('locations', models.PROTECT)
    job = models.BooleanField()
    user = models.ForeignKey('user_system.users', models.SET(0), null=True)
    route = models.ForeignKey('routes', models.PROTECT, null=True)
    job_start_time = models.DateTimeField(null=True)
    job_duration = models.PositiveIntegerField(null=True)
    job_finish_time = models.DateTimeField(null=True)
    origin = models.ForeignKey('locations', models.PROTECT, null=True, related_name='id_destination')
    destination = models.ForeignKey('locations', models.PROTECT, null=True, related_name='id_origin')
    future_booking = models.ForeignKey('future_bookings', models.SET_NULL, null=True)


class future_bookings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user_system.users', models.SET(0))
    route = models.ForeignKey('routes', models.PROTECT)
    job_start_time = models.DateTimeField()
    job_duration = models.PositiveIntegerField(null=True)
    job_finish_time = models.DateTimeField(null=True)
    origin = models.ForeignKey('locations', models.PROTECT, related_name='destination')
    destination = models.ForeignKey('locations', models.PROTECT, related_name='origin')


class world_data(models.Model):
    items = models.TextField()
    data = models.IntegerField()
