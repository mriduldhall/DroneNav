from django.utils import timezone
from datetime import datetime, timedelta
from random import randint
from itertools import chain

from user_system.models import users
from .models import drones, bases, locations, cities, routes, world_data, future_bookings


def get_vehicles_of_user(username):
    vehicles_data = []
    try:
        user = users.objects.filter(username=username)
        user_id = user[0]
        drones_booked_by_user = (drones.objects.filter(user_id=user_id)).order_by('id')
        for drone in drones_booked_by_user:
            drone.type = "Air"
        bases_booked_by_user = (bases.objects.filter(user_id=user_id)).order_by('id')
        for base in bases_booked_by_user:
            base.type = "Ground"
        vehicles_booked_by_user = sorted(chain(drones_booked_by_user, bases_booked_by_user), key=lambda instance: instance.id)
        for vehicle in vehicles_booked_by_user:
            origin_data = locations.objects.filter(id=vehicle.origin_id)
            origin = (origin_data[0]).location
            origin_city_data = (cities.objects.filter(id=(origin_data[0]).city_id))[0]
            origin = origin + ", " + origin_city_data.city
            destination_data = locations.objects.filter(id=vehicle.destination_id)
            destination = (destination_data[0]).location
            destination_city_data = (cities.objects.filter(id=(destination_data[0]).city_id))[0]
            destination = destination + ", " + destination_city_data.city
            vehicle_data = [vehicle.type, vehicle.id, origin, destination, vehicle.job_finish_time]
            vehicles_data.append(vehicle_data)
        return vehicles_data
    except drones.DoesNotExist or bases.DoesNotExist:
        print("Dashboard error occurred")
        return vehicles_data


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
            vehicle = drones.objects.filter(future_booking_id=booking.id)
            if not vehicle:
                vehicle = bases.objects.filter(future_booking_id=booking.id)
                vehicle = vehicle[0]
                vehicle.type = "Ground"
            else:
                vehicle = vehicle[0]
                vehicle.type = "Air"
            booking_data = [vehicle.type, vehicle.id, origin, destination, booking.job_start_time]
            bookings_data.append(booking_data)
        bookings_data = sorted(bookings_data, key=lambda instance: instance[1])
        return bookings_data
    except drones.DoesNotExist or bases.DoesNotExist:
        print("Dashboard error occurred")
        return bookings_data


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


def find_earliest_vehicle(origin, transport):
    location_data = locations.objects.filter(location=origin)
    origin_id = (location_data[0]).id
    if transport == "Drone":
        available_vehicles = (drones.objects.filter(destination_id=origin_id, job=True, future_booking_id=None)).order_by('job_finish_time')
    else:
        available_vehicles = (bases.objects.filter(destination_id=origin_id, job=True, future_booking_id=None)).order_by('job_finish_time')
    if not available_vehicles:
        return None
    else:
        earliest_vehicle = available_vehicles[0]
        return earliest_vehicle


def assign_booking(vehicle, origin, destination, username, transport, job_start_time="", job_duration="", job_finish_time=""):
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
    if job_start_time == "":
        job_start_time = datetime.now(tz=timezone.utc)
    if job_duration == "":
        job_duration = _calculate_job_duration((route_data[0]).distance, transport)
    if job_finish_time == "":
        job_finish_time = job_start_time + timedelta(minutes=job_duration)
    assert origin_id == vehicle.location_id
    _save_data(vehicle, user_id, route_id, job_start_time, job_duration, job_finish_time, origin_id, destination_id)
    return job_finish_time


def create_future_booking(vehicle, origin, destination, username, transport="", job_start_time="", job_duration="", job_finish_time=""):
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
    if job_start_time == "":
        job_start_time = vehicle.job_finish_time
    if job_duration == "":
        job_duration = _calculate_job_duration((route_data[0]).distance, transport)
    if job_finish_time == "":
        job_finish_time = job_start_time + timedelta(minutes=job_duration)
    future_booking = future_bookings(user_id=user_id, route_id=route_id, job_start_time=job_start_time, job_duration=job_duration, job_finish_time=job_finish_time, origin_id=origin_id, destination_id=destination_id)
    future_booking.save()
    future_booking_id = future_booking.pk
    vehicle.future_booking_id = future_booking_id
    vehicle.save()
    return job_finish_time


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
        lowest_speed = world_data.objects.filter(items=transport + " lowest speed")
        lowest_speed = (lowest_speed[0]).data
        highest_speed = world_data.objects.filter(items=transport + " highest speed")
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


def form_time(raw_time):
    if raw_time >= datetime.time(datetime.now(tz=timezone.utc)):
        time = datetime.now(tz=timezone.utc)
        time = time.replace(hour=raw_time.hour, minute=raw_time.minute, second=0, microsecond=0)
        return time
    else:
        time = datetime.now(tz=timezone.utc)
        time = time.replace(day=time.day + 1, hour=raw_time.hour, minute=raw_time.minute, second=0, microsecond=0)
        return time


def same_city(origin, destination):
    origin_data = (locations.objects.filter(location=origin))[0]
    origin_city_data = (cities.objects.filter(id=origin_data.city_id))[0]
    destination_data = (locations.objects.filter(location=destination))[0]
    destination_city_data = (cities.objects.filter(id=destination_data.city_id))[0]
    if origin_city_data.city == destination_city_data.city:
        return True
    else:
        return False


def check_intercity_travel(location):
    location_data = (locations.objects.filter(location=location))[0]
    if location_data.intercity:
        return True
    else:
        return False


def find_intercity_location(location):
    location_data = (locations.objects.filter(location=location))[0]
    intracity_location = (locations.objects.filter(city_id=location_data.city_id, intercity=True))[0]
    return intracity_location.location


def index_in_list(list, index):
    return index < len(list)


def plan_route(origin, destination):
    book_status = ""
    vehicles = []
    vehicles_types = []
    route_locations = []
    if not same_city(origin, destination):
        origin_intercity_location = find_intercity_location(origin)
        destination_intercity_location = find_intercity_location(destination)
        if origin_intercity_location != origin:
            base = find_available_vehicle(origin, "Base")
            if not base:
                base = find_earliest_vehicle(origin, "Base")
                book_status = "Later"
            vehicles.append(base)
            route_locations.append(origin)
        drone = find_available_vehicle(origin_intercity_location, "Drone")
        if not drone:
            drone = find_earliest_vehicle(origin_intercity_location, "Drone")
            book_status = "Later"
        vehicles.append(drone)
        route_locations.append(origin_intercity_location)
        if destination_intercity_location != destination:
            base = find_available_vehicle(destination, "Base")
            if not base:
                base = find_earliest_vehicle(destination, "Base")
                book_status = "Later"
            vehicles.append(base)
            route_locations.append(destination_intercity_location)
    else:
        base = find_available_vehicle(origin, "Base")
        if not base:
            find_earliest_vehicle(origin, "Base")
            book_status = "Later"
        vehicles.append(base)
        route_locations.append(origin)
    route_locations.append(destination)
    for vehicle in vehicles:
        if isinstance(vehicle, drones):
            vehicles_types.append("Drone")
        else:
            vehicles_types.append("Base")
    return vehicles, vehicles_types, route_locations, book_status


def plan_time(vehicles, route_locations):
    route_locations_id = []
    start_times = []
    durations = []
    end_times = []
    for location in route_locations:
        route_locations_id.append((locations.objects.filter(location=location))[0].id)
    for counter in range(len(vehicles)):
        if vehicles[counter].job:
            if counter == 0:
                start_time = vehicles[counter].job_finish_time
            elif vehicles[counter].job_finish_time > end_times[counter-1]:
                start_time = vehicles[counter].job_finish_time
            else:
                start_time = end_times[counter - 1]
        else:
            if counter == 0:
                start_time = datetime.now(tz=timezone.utc)
            else:
                start_time = end_times[counter-1]
        if route_locations_id[counter] < route_locations_id[counter+1]:
            distance = (routes.objects.filter(city_a_id=route_locations_id[counter], city_b_id=route_locations_id[counter+1]))[0].distance
        else:
            distance = (routes.objects.filter(city_a_id=route_locations_id[counter+1], city_b_id=route_locations_id[counter]))[0].distance
        if isinstance(vehicles[counter], drones):
            transport = "Drone"
        else:
            transport = "Base"
        job_duration = _calculate_job_duration(distance, transport)
        end_time = start_time + timedelta(minutes=job_duration)
        start_times.append(start_time)
        durations.append(job_duration)
        end_times.append(end_time)
    return start_times, durations, end_times


def plan_future_time(vehicles, route_locations, start_time):
    route_locations_id = []
    start_times = []
    durations = []
    end_times = []
    for location in route_locations:
        route_locations_id.append((locations.objects.filter(location=location))[0].id)
    for counter in range(len(vehicles)):
        if vehicles[counter].job:
            if counter == 0:
                if vehicles[counter].job_finish_time > start_time:
                    start_time = None
                    start_times.append(start_time)
                    break
            elif vehicles[counter].job_finish_time > end_times[counter - 1]:
                start_time = None
                start_times.append(start_time)
                break
            else:
                start_time = end_times[counter-1]
        else:
            if counter == 0:
                pass
            else:
                start_time = end_times[counter-1]
        if route_locations_id[counter] < route_locations_id[counter + 1]:
            distance = (routes.objects.filter(city_a_id=route_locations_id[counter], city_b_id=route_locations_id[counter + 1]))[0].distance
        else:
            distance = (routes.objects.filter(city_a_id=route_locations_id[counter + 1], city_b_id=route_locations_id[counter]))[0].distance
        if isinstance(vehicles[counter], drones):
            transport = "Drone"
        else:
            transport = "Base"
        job_duration = _calculate_job_duration(distance, transport)
        end_time = start_time + timedelta(minutes=job_duration)
        start_times.append(start_time)
        durations.append(job_duration)
        end_times.append(end_time)
    return start_times, durations, end_times


def book_journey(vehicles, vehicles_types, route_locations, start_times, durations, end_times, username, future=False):
    if not future:
        if vehicles[0].job:
            create_future_booking(vehicles[0], route_locations[0], route_locations[1], username, vehicles_types[0], start_times[0], durations[0], end_times[0])
        else:
            assign_booking(vehicles[0], route_locations[0], route_locations[1], username, vehicles_types[0], start_times[0], durations[0], end_times[0])
    else:
        create_future_booking(vehicles[0], route_locations[0], route_locations[1], username, vehicles_types[0], start_times[0], durations[0], end_times[0])
    del vehicles[0], route_locations[0], vehicles_types[0], start_times[0], durations[0], end_times[0]
    for counter in range(len(vehicles)):
        create_future_booking(vehicles[counter], route_locations[counter], route_locations[counter+1], username, vehicles_types[counter], start_times[counter], durations[counter], end_times[counter])


def convert_vehicles_to_ids(vehicles):
    vehicles_ids = []
    for vehicle in vehicles:
        vehicles_ids.append(vehicle.id)
    return vehicles_ids


def convert_vehicle_ids_to_vehicles(vehicles_ids, vehicle_types):
    vehicles = []
    for counter in range(len(vehicles_ids)):
        if vehicle_types[counter] == "Drone":
            vehicles.append(drones.objects.filter(id=vehicles_ids[counter])[0])
        else:
            vehicles.append(bases.objects.filter(id=vehicles_ids[counter])[0])
    return vehicles


def convert_locations_to_ids(route_locations):
    route_locations_ids = []
    for location in route_locations:
        route_locations_ids.append((locations.objects.filter(location=location))[0].id)
    return route_locations_ids


def convert_locations_ids_to_locations(route_locations_ids):
    route_locations = []
    for id in route_locations_ids:
        route_locations.append(locations.objects.filter(id=id)[0].location)
    return route_locations


def serialize_datetime(raw_time_list):
    time_list = []
    for time in raw_time_list:
        time_list.append(str(time))
    return time_list


def deserialize_datetime(raw_time_list):
    time_list = []
    for time in raw_time_list:
        time_list.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f%z'))
    return time_list


def get_locations_data():
    locations_data = []
    all_locations = (locations.objects.all()).order_by('id')
    for location in all_locations:
        city_data = (cities.objects.filter(id=location.city_id))[0]
        location_data = [location.location, city_data.city, location.intercity]
        locations_data.append(location_data)
    return locations_data
