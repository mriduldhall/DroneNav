from DroneNav.wsgi import *

import time
from random import randint
import random

from drone_system.drones import world_data, locations
from drone_system.drones import find_available_drone, assign_booking

if __name__ == '__main__':
    while True:
        lowest_jobs = world_data.objects.filter(items="Drone jobs minimum")
        lowest_jobs = (lowest_jobs[0]).data
        highest_jobs = world_data.objects.filter(items="Drone jobs maximum")
        highest_jobs = (highest_jobs[0]).data
        jobs = randint(lowest_jobs, highest_jobs)
        locations_list = []
        for _ in range(jobs):
            locations_data = locations.objects.all()
            for location in locations_data:
                locations_list.append(location.location)
            origin = random.choice(locations_list)
            locations_list.remove(origin)
            destination = random.choice(locations_list)
            if origin != destination:
                drone = find_available_drone(origin)
                if drone:
                    assign_booking(drone, origin, destination, "Emulator")
        time.sleep(360)
