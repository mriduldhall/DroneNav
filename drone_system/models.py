from django.db import models


# Create your models here.
class locations(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.TextField()


class routes(models.Model):
    id = models.AutoField(primary_key=True)
    distance = models.PositiveSmallIntegerField()
    city_a = models.ForeignKey('locations', models.PROTECT, related_name='city_b')
    city_b = models.ForeignKey('locations', models.PROTECT, related_name='city_a')


class drones(models.Model):
    id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey('locations', models.PROTECT)
    job = models.BooleanField()
    user_id = models.ForeignKey('user_system.users', models.SET(0), null=True)
    route_id = models.ForeignKey('routes', models.PROTECT, null=True)
    job_start_time = models.TimeField(null=True)
    job_duration = models.PositiveIntegerField(null=True)
    job_finish_time = models.TimeField(null=True)
    origin_id = models.ForeignKey('locations', models.PROTECT, null=True, related_name='destination_id')
    destination_id = models.ForeignKey('locations', models.PROTECT, null=True, related_name='origin_id')


class world_data(models.Model):
    items = models.TextField()
    data = models.IntegerField()
