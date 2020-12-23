from .models import drones
from .models import locations
from user_system.models import users


def get_drones_of_user(username):
    drones_data = []
    try:
        user = users.objects.filter(username=username)
        user_id = user[0]
        drones_booked_by_user = drones.objects.filter(user_id=user_id)
        for drone in drones_booked_by_user:
            origin_data = locations.objects.filter(id=drone.origin_id)
            origin = (origin_data[0]).location
            destination_data = locations.objects.filter(id=drone.destination_id)
            destination = (destination_data[0]).location
            drone_data = [drone.id, origin, destination, drone.job_finish_time]
            drones_data.append(drone_data)
        return drones_data
    except drones.DoesNotExist:
        return drones_data
