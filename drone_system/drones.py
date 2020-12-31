from django.utils import timezone
from datetime import datetime, timedelta
from random import randint

from user_system.models import users
from .models import drones, bases, locations, cities, routes, world_data, future_bookings


def get_drones_of_user(username):
    drones_data = []
    try:
        user = users.objects.filter(username=username)
        user_id = user[0]
        drones_booked_by_user = (drones.objects.filter(user_id=user_id)).order_by('id')
        for drone in drones_booked_by_user:
            origin_data = locations.objects.filter(id=drone.origin_id)
            origin = (origin_data[0]).location
            origin_city_data = (cities.objects.filter(id=(origin_data[0]).city_id))[0]
            origin = origin + ", " + origin_city_data.city
            destination_data = locations.objects.filter(id=drone.destination_id)
            destination = (destination_data[0]).location
            destination_city_data = (cities.objects.filter(id=(destination_data[0]).city_id))[0]
            destination = destination + ", " + destination_city_data.city
            drone_data = [drone.id, origin, destination, drone.job_finish_time]
            drones_data.append(drone_data)
        return drones_data
    except drones.DoesNotExist:
        return drones_data


def get_all_drone_data():
    drones_data = []
    try:
        all_drones = drones.objects.all().order_by('id')
        for drone in all_drones:
            if drone.job:
                origin_data = locations.objects.filter(id=drone.origin_id)
                origin = (origin_data[0]).location
                origin_city_data = (cities.objects.filter(id=(origin_data[0]).city_id))[0]
                origin = origin + ", " + origin_city_data.city
                destination_data = locations.objects.filter(id=drone.destination_id)
                destination = (destination_data[0]).location
                destination_city_data = (cities.objects.filter(id=(destination_data[0]).city_id))[0]
                destination = destination + ", " + destination_city_data.city
            else:
                origin = None
                destination = None
            drone_data = [drone.id, drone.job, origin, destination, drone.job_finish_time]
            drones_data.append(drone_data)
        return drones_data
    except drones.DoesNotExist:
        return drones_data


def get_all_base_data():
    bases_data = []
    try:
        all_bases = bases.objects.all().order_by('id')
        for base in all_bases:
            if base.job:
                origin_data = locations.objects.filter(id=base.origin_id)
                origin = (origin_data[0]).location
                origin_city_data = (cities.objects.filter(id=(origin_data[0]).city_id))[0]
                origin = origin + ", " + origin_city_data.city
                destination_data = locations.objects.filter(id=base.destination_id)
                destination = (destination_data[0]).location
                destination_city_data = (cities.objects.filter(id=(destination_data[0]).city_id))[0]
                destination = destination + ", " + destination_city_data.city
            else:
                origin = None
                destination = None
            base_data = [base.id, base.job, origin, destination, base.job_finish_time]
            bases_data.append(base_data)
        return bases_data
    except bases.DoesNotExist:
        return bases_data


def find_available_vehicle(origin, transport):
    location_data = locations.objects.filter(location=origin)
    origin_id = (location_data[0]).id
    if transport == "Drone":
        available_vehicles = drones.objects.filter(location_id=origin_id, job=False, future_booking_id=None)
    else:
        available_vehicles = bases.objects.filter(location_id=origin_id, job=False, future_booking_id=None)
    if not available_vehicles:
        return None
    else:
        vehicle = available_vehicles[0]
        return vehicle


def assign_booking(vehicle, origin, destination, username, transport):
    user_data = users.objects.filter(username=username)
    user_id = user_data[0]
    origin_data = locations.objects.filter(location=origin)
    origin_id = (origin_data[0]).id
    destination_data = locations.objects.filter(location=destination)
    destination_id = (destination_data[0]).id
    if origin_id < destination_id:
        route_data = routes.objects.filter(city_a_id=origin_id, city_b_id=destination_id)
    else:
        route_data = routes.objects.filter(city_a_id=destination_id, city_b_id=origin_id)
    route_id = (route_data[0]).id
    job_start_time = datetime.now(tz=timezone.utc)
    job_duration = _calculate_job_duration((route_data[0]).distance, transport)
    job_finish_time = job_start_time + timedelta(minutes=job_duration)
    assert origin_id == vehicle.location_id
    _save_data(vehicle, user_id, route_id, job_start_time, job_duration, job_finish_time, origin_id, destination_id)


def _calculate_job_duration(distance, transport):
    traffic_probability = world_data.objects.filter(items=transport + " traffic probability")
    traffic_probability = (traffic_probability[0]).data
    current_traffic = 100 - (randint(1, 100))
    if traffic_probability <= current_traffic:
        lowest_speed = world_data.objects.filter(items=transport + " lowest traffic speed")
        lowest_speed = (lowest_speed[0]).data
        highest_speed = world_data.objects.filter(items=transport + " highest traffic speed")
        highest_speed = (highest_speed[0]).data
        speed = randint(lowest_speed, highest_speed)
    else:
        lowest_speed = world_data.objects.filter(items=transport + "lowest speed")
        lowest_speed = (lowest_speed[0]).data
        highest_speed = world_data.objects.filter(items=transport + "highest speed")
        highest_speed = (highest_speed[0]).data
        speed = randint(lowest_speed, highest_speed)
    job_duration = distance/speed
    run_speed = world_data.objects.filter(items="Run speed")
    run_speed = (run_speed[0]).data
    job_duration = job_duration / run_speed
    return int(job_duration * 60)


def _save_data(vehicle, user_id, route_id, job_start_time, job_duration, job_finish_time, origin_id, destination_id):
    vehicle.job = True
    vehicle.user_id = user_id
    vehicle.route_id = route_id
    vehicle.job_start_time = job_start_time
    vehicle.job_duration = job_duration
    vehicle.job_finish_time = job_finish_time
    vehicle.origin_id = origin_id
    vehicle.destination_id = destination_id
    vehicle.save()


def find_earliest_drone(origin):
    location_data = locations.objects.filter(location=origin)
    origin_id = (location_data[0]).id
    available_drones = (drones.objects.filter(destination_id=origin_id, job=True, future_booking_id=None)).order_by('job_finish_time')
    if not available_drones:
        return None
    else:
        earliest_drone = available_drones[0]
        return earliest_drone


def create_future_booking(drone_id, origin, destination, username, job_start_time=""):
    user_data = users.objects.filter(username=username)
    user_id = (user_data[0]).id
    origin_data = locations.objects.filter(location=origin)
    origin_id = (origin_data[0]).id
    destination_data = locations.objects.filter(location=destination)
    destination_id = (destination_data[0]).id
    if origin_id < destination_id:
        route_data = routes.objects.filter(city_a_id=origin_id, city_b_id=destination_id)
    else:
        route_data = routes.objects.filter(city_a_id=destination_id, city_b_id=origin_id)
    route_id = (route_data[0]).id
    drone = (drones.objects.filter(id=drone_id)[0])
    if job_start_time == "":
        job_start_time = drone.job_finish_time
    future_booking = future_bookings(user_id=user_id, route_id=route_id, job_start_time=job_start_time, origin_id=origin_id, destination_id=destination_id)
    future_booking.save()
    future_booking_id = future_booking.pk
    drone.future_booking_id = future_booking_id
    drone.save()


def form_time(raw_time):
    if raw_time >= datetime.time(datetime.now(tz=timezone.utc)):
        time = datetime.now(tz=timezone.utc)
        time = time.replace(hour=raw_time.hour, minute=raw_time.minute, second=0, microsecond=0)
        return time
    else:
        time = datetime.now(tz=timezone.utc)
        time = time.replace(day=time.day + 1, hour=raw_time.hour, minute=raw_time.minute, second=0, microsecond=0)
        return time


def get_future_bookings_of_user(username):
    bookings_data = []
    try:
        user = users.objects.filter(username=username)
        user_id = user[0]
        future_bookings_of_user = (future_bookings.objects.filter(user_id=user_id)).order_by('id')
        for booking in future_bookings_of_user:
            origin_data = locations.objects.filter(id=booking.origin_id)
            origin = (origin_data[0]).location
            origin_city_data = (cities.objects.filter(id=(origin_data[0]).city_id))[0]
            origin = origin + ", " + origin_city_data.city
            destination_data = locations.objects.filter(id=booking.destination_id)
            destination = (destination_data[0]).location
            destination_city_data = (cities.objects.filter(id=(destination_data[0]).city_id))[0]
            destination = destination + ", " + destination_city_data.city
            drone = (drones.objects.filter(future_booking_id=booking.id))[0]
            booking_data = [drone.id, origin, destination, booking.job_start_time]
            bookings_data.append(booking_data)
        return bookings_data
    except drones.DoesNotExist:
        return bookings_data


def same_city(origin, destination):
    origin_data = (locations.objects.filter(location=origin))[0]
    origin_city_data = (cities.objects.filter(id=origin_data.city_id))[0]
    destination_data = (locations.objects.filter(location=destination))[0]
    destination_city_data = (cities.objects.filter(id=destination_data.city_id))[0]
    if origin_city_data.city == destination_city_data.city:
        return True
    else:
        return False
