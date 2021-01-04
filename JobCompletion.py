from DroneNav.wsgi import *

import time
from datetime import datetime, timedelta
from django.utils import timezone
from itertools import chain


from drone_system.drones import _calculate_job_duration
from drone_system.models import drones, bases, future_bookings, routes


def complete_jobs():
    drones_list = drones.objects.filter(job=True)
    bases_list = bases.objects.filter(job=True)
    vehicles_list = chain(drones_list, bases_list)
    if vehicles_list:
        for vehicle in vehicles_list:
            job_finish_time = vehicle.job_finish_time
            if datetime.now(tz=timezone.utc) >= job_finish_time:
                vehicle.location_id = vehicle.destination_id
                vehicle.job = False
                vehicle.user_id = None
                vehicle.route_id = None
                vehicle.job_start_time = None
                vehicle.job_duration = None
                vehicle.job_finish_time = None
                vehicle.origin_id = None
                vehicle.destination_id = None
                vehicle.save()


def assign_future_jobs():
    drones_list = (drones.objects.filter(job=False)).exclude(future_booking_id=None)
    bases_list = (bases.objects.filter(job=False)).exclude(future_booking_id=None)
    vehicles_list = chain(drones_list, bases_list)
    if vehicles_list:
        for vehicle in vehicles_list:
            future_booking = future_bookings.objects.filter(id=vehicle.future_booking_id)
            future_booking = future_booking[0]
            if datetime.now(tz=timezone.utc) >= future_booking.job_start_time:
                vehicle.job = True
                vehicle.user_id = future_booking.user_id
                vehicle.route_id = future_booking.route_id
                if future_booking.job_start_time is None:
                    vehicle.job_start_time = datetime.now(tz=timezone.utc)
                else:
                    vehicle.job_start_time = future_booking.job_start_time
                if future_booking.origin_id < future_booking.destination_id:
                    if future_booking.job_duration is None:
                        if isinstance(vehicle, drones):
                            vehicle.job_duration = _calculate_job_duration((routes.objects.filter(city_a_id=future_booking.origin_id, city_b_id=future_booking.destination_id)[0]).distance, "Drone")
                        else:
                            vehicle.job_duration = _calculate_job_duration((routes.objects.filter(city_a_id=future_booking.origin_id, city_b_id=future_booking.destination_id)[0]).distance, "Base")
                    else:
                        vehicle.job_duration = future_booking.job_duration
                else:
                    if future_booking.job_duration is None:
                        if isinstance(vehicle, drones):
                            vehicle.job_duration = _calculate_job_duration((routes.objects.filter(city_a_id=future_booking.destination_id, city_b_id=future_booking.origin_id)[0]).distance, "Drone")
                        else:
                            vehicle.job_duration = _calculate_job_duration((routes.objects.filter(city_a_id=future_booking.destination_id, city_b_id=future_booking.origin_id)[0]).distance, "Base")
                    else:
                        vehicle.job_duration = future_booking.job_duration
                if future_booking.job_finish_time is None:
                    vehicle.job_finish_time = vehicle.job_start_time + timedelta(minutes=vehicle.job_duration)
                else:
                    vehicle.job_finish_time = future_booking.job_finish_time
                vehicle.origin_id = future_booking.origin_id
                vehicle.destination_id = future_booking.destination_id
                vehicle.future_booking_id = None
                vehicle.save()
                future_booking.delete()


if __name__ == '__main__':
    while True:
        complete_jobs()
        assign_future_jobs()
        time.sleep(120)
