from DroneNav.wsgi import *

import time
from random import randint
import random

from drone_system.models import drones, world_data, locations
from drone_system.drones import plan_route, plan_time, book_journey

if __name__ == '__main__':
    while True:
        minimum_drones = (world_data.objects.filter(items="Minimum drones"))[0].data
        if len((drones.objects.filter(job=False, future_booking_id=None))) <= minimum_drones:
            lowest_jobs = world_data.objects.filter(items="Jobs minimum")
            lowest_jobs = (lowest_jobs[0]).data
            highest_jobs = world_data.objects.filter(items="Jobs maximum")
            highest_jobs = (highest_jobs[0]).data
            jobs = randint(lowest_jobs, highest_jobs)
            for _ in range(jobs):
                locations_list = []
                locations_data = locations.objects.all()
                for location in locations_data:
                    locations_list.append(location.location)
                origin = random.choice(locations_list)
                locations_list.remove(origin)
                destination = random.choice(locations_list)
                assert origin != destination
                vehicles, vehicles_types, route_locations, book_status = plan_route(origin, destination)
                if None not in vehicles:
                    start_times, durations, end_times = plan_time(vehicles, route_locations)
                    if book_status == "":
                        print("--Job start--")
                        for vehicle in vehicles:
                            print("Assigning job to", vehicle)
                        book_journey(vehicles, vehicles_types, route_locations, start_times, durations, end_times, "Emulator")
                        print("--Job end--")
                    else:
                        future_booking_probability = world_data.objects.filter(items="Future booking probability")
                        future_booking_probability = (future_booking_probability[0]).data
                        future_booking_decision = randint(1, 100)
                        if future_booking_decision < future_booking_probability:
                            print("--Job start--")
                            for vehicle in vehicles:
                                print("Assigning future job to", vehicle)
                            book_journey(vehicles, vehicles_types, route_locations, start_times, durations, end_times, "Emulator")
                            print("--Job end--")
        time.sleep(360)
