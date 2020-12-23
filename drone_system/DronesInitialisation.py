from DroneNav.wsgi import *
from drone_system.models import drones, locations


for _ in range(0, 22):
    drone = drones(location_id=(locations.objects.get(id=1)).pk, job=False)
    drone.save()

for _ in range(0, 8):
    drone = drones(location_id=(locations.objects.get(id=2)).pk, job=False)
    drone.save()

for _ in range(0, 11):
    drone = drones(location_id=(locations.objects.get(id=3)).pk, job=False)
    drone.save()

for _ in range(0, 19):
    drone = drones(location_id=(locations.objects.get(id=4)).pk, job=False)
    drone.save()

for _ in range(0, 15):
    drone = drones(location_id=(locations.objects.get(id=5)).pk, job=False)
    drone.save()

for _ in range(0, 18):
    drone = drones(location_id=(locations.objects.get(id=6)).pk, job=False)
    drone.save()

for _ in range(0, 7):
    drone = drones(location_id=(locations.objects.get(id=7)).pk, job=False)
    drone.save()
