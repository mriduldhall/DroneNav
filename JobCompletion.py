from DroneNav.wsgi import *

import time
from datetime import datetime, timedelta
from django.utils import timezone

from drone_system.drones import _calculate_job_duration
from drone_system.models import drones, future_bookings, routes


def complete_jobs():
    drones_list = drones.objects.filter(job=True)
    if drones_list:
        for drone in drones_list:
            job_finish_time = drone.job_finish_time
            if datetime.now(tz=timezone.utc) >= job_finish_time:
                drone.location_id = drone.destination_id
                drone.job = False
                drone.user_id = None
                drone.route_id = None
                drone.job_start_time = None
                drone.job_duration = None
                drone.job_finish_time = None
                drone.origin_id = None
                drone.destination_id = None
                drone.save()


def assign_future_jobs():
    drones_list = (drones.objects.filter(job=False)).exclude(future_booking_id=None)
    if drones_list:
        for drone in drones_list:
            future_booking = future_bookings.objects.filter(id=drone.future_booking_id)
            future_booking = future_booking[0]
            if datetime.now(tz=timezone.utc) >= future_booking.job_start_time:
                drone.job = True
                drone.user_id = future_booking.user_id
                drone.route_id = future_booking.route_id
                drone.job_start_time = datetime.now(tz=timezone.utc)
                if future_booking.origin_id < future_booking.destination_id:
                    drone.job_duration = _calculate_job_duration((routes.objects.filter(city_a_id=future_booking.origin_id, city_b_id=future_booking.destination_id)[0]).distance)
                else:
                    drone.job_duration = _calculate_job_duration((routes.objects.filter(city_a_id=future_booking.destination_id, city_b_id=future_booking.origin_id)[0]).distance)
                drone.job_finish_time = drone.job_start_time + timedelta(minutes=drone.job_duration)
                drone.origin_id = future_booking.origin_id
                drone.destination_id = future_booking.destination_id
                drone.future_booking_id = None
                drone.save()
                future_booking.delete()


if __name__ == '__main__':
    while True:
        complete_jobs()
        assign_future_jobs()
        time.sleep(120)
