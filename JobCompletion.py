from DroneNav.wsgi import *

import time
from datetime import datetime
from django.utils import timezone

from drone_system.models import drones

if __name__ == '__main__':
    while True:
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
        time.sleep(120)
