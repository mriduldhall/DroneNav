from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BookForm, ChangePassword, DeleteAccount, FutureBook
from .settings import validate_password, change_password, delete_account
from .drones import get_vehicles_of_user, get_all_drone_data, get_all_base_data, form_time, get_future_bookings_of_user, plan_route, plan_time, plan_future_time, book_journey, convert_vehicles_to_ids, convert_vehicle_ids_to_vehicles, convert_locations_to_ids, convert_locations_ids_to_locations, serialize_datetime, deserialize_datetime, get_locations_data


# Create your views here.
def dashboard(request):
    vehicles_data = get_vehicles_of_user(request.session['username'])
    future_booking_data = get_future_bookings_of_user(request.session['username'])
    context = {
        "username": request.session['username'],
        "vehicles_data": vehicles_data,
        "future_booking_data": future_booking_data
    }
    return render(request, '../../drone_system/templates/drone_system/dashboard.html', context)


def information(request):
    drones_data = get_all_drone_data()
    bases_data = get_all_base_data()
    context = {
        "drones_data": drones_data,
        "bases_data": bases_data,
    }
    return render(request, '../../drone_system/templates/drone_system/information.html', context)


def locations(request):
    locations_data = get_locations_data()
    context = {
        "locations_data": locations_data,
    }
    return render(request, '../../drone_system/templates/drone_system/locations.html', context)


def book(request):
    book_status = ""
    vehicles = []
    vehicles_types = []
    route_locations = []
    start_times = []
    end_times = []
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.cleaned_data['origin'] = str(form.cleaned_data['origin'])
            form.cleaned_data['origin'] = (form.cleaned_data['origin'].split(','))[0]
            form.cleaned_data['destination'] = str(form.cleaned_data['destination'])
            form.cleaned_data['destination'] = (form.cleaned_data['destination'].split(','))[0]
            if request.POST.get("Book"):
                if form.cleaned_data['origin'] != form.cleaned_data['destination']:
                    vehicles, vehicles_types, route_locations, book_status = plan_route(form.cleaned_data['origin'], form.cleaned_data['destination'])
                    if None in vehicles:
                        book_status = "None"
                    elif book_status == "":
                        start_times, durations, end_times = plan_time(vehicles, route_locations)
                        book_journey(vehicles, vehicles_types, route_locations, start_times, durations, end_times, request.session['username'])
                        book_status = "Booked"
                    else:
                        start_times, durations, end_times = plan_time(vehicles, route_locations)
                        vehicles_ids = convert_vehicles_to_ids(vehicles)
                        route_locations_ids = convert_locations_to_ids(route_locations)
                        serialized_start_times = serialize_datetime(start_times)
                        serialized_end_times = serialize_datetime(end_times)
                        request.session['vehicles_ids'] = vehicles_ids
                        request.session['vehicles_types'] = vehicles_types
                        request.session['route_locations_ids'] = route_locations_ids
                        request.session['start_times'] = serialized_start_times
                        request.session['durations'] = durations
                        request.session['end_times'] = serialized_end_times
                else:
                    book_status = "Same"
            elif request.POST.get("Yes"):
                vehicles = convert_vehicle_ids_to_vehicles(request.session['vehicles_ids'], request.session['vehicles_types'])
                route_locations = convert_locations_ids_to_locations(request.session['route_locations_ids'])
                start_times = deserialize_datetime(request.session['start_times'])
                end_times = deserialize_datetime(request.session['end_times'])
                book_journey(vehicles, request.session['vehicles_types'], route_locations, start_times, request.session['durations'], end_times, request.session['username'])
                book_status = "Booked"
                form = BookForm()
                del request.session['vehicles_ids']
                del request.session['vehicles_types']
                del request.session['route_locations_ids']
                del request.session['start_times']
                del request.session['durations']
                del request.session['end_times']
            elif request.POST.get("No"):
                del request.session['vehicles_ids']
                del request.session['vehicles_types']
                del request.session['route_locations_ids']
                del request.session['start_times']
                del request.session['durations']
                del request.session['end_times']
                form = BookForm()
    else:
        form = BookForm()
    context = {
        "form": form,
        "book_status": book_status,
        "vehicles": vehicles,
        "vehicles_types": vehicles_types,
        "route_locations": route_locations,
        "start_times": start_times,
        "end_times": end_times,
    }
    return render(request, '../../drone_system/templates/drone_system/book.html', context)


def futurebook(request):
    time_validation = ""
    book_status = ""
    if request.method == "POST":
        form = FutureBook(request.POST)
        if form.is_valid():
            form.cleaned_data['origin'] = str(form.cleaned_data['origin'])
            form.cleaned_data['origin'] = (form.cleaned_data['origin'].split(','))[0]
            form.cleaned_data['destination'] = str(form.cleaned_data['destination'])
            form.cleaned_data['destination'] = (form.cleaned_data['destination'].split(','))[0]
            if form.cleaned_data['origin'] != form.cleaned_data['destination']:
                time = form_time(form.cleaned_data['time'])
                time_validation = True
                vehicles, vehicles_types, route_locations, book_status = plan_route(form.cleaned_data['origin'], form.cleaned_data['destination'])
                if None in vehicles:
                    book_status = "None"
                else:
                    start_times, durations, end_times = plan_future_time(vehicles, route_locations, time)
                    print(start_times)
                    if None in start_times:
                        print("None in start times")
                        book_status = "None"
                    else:
                        book_journey(vehicles, vehicles_types, route_locations, start_times, durations, end_times, request.session['username'], True)
                        book_status = "Booked"
                        form = FutureBook()
            else:
                book_status = "Same"
        else:
            time_validation = False
    else:
        form = FutureBook()
    context = {
        "form": form,
        "time_validation": time_validation,
        "book_status": book_status,
    }
    return render(request, '../../drone_system/templates/drone_system/futurebook.html', context)


def help(request):
    return render(request, '../../drone_system/templates/drone_system/help.html')


def settings(request):
    return render(request, '../../drone_system/templates/drone_system/settings.html')


def changepassword(request):
    form = ChangePassword(request.POST or None)
    status = ""
    if form.is_valid():
        if validate_password(request.session['username'], form.cleaned_data['password']):
            if form.cleaned_data['new_password'] == form.cleaned_data['repeat_password']:
                change_password(request.session['username'], form.cleaned_data['new_password'])
                status = "Changed"
            else:
                status = "Not same"
        else:
            status = "Wrong"
        form = ChangePassword()
    context = {
        "form": form,
        "status": status
    }
    return render(request, '../../drone_system/templates/drone_system/changepassword.html', context)


def deleteaccount(request):
    form = DeleteAccount(request.POST or None)
    status = ""
    if form.is_valid():
        if validate_password(request.session['username'], form.cleaned_data['password']):
            delete_account(request.session['username'])
            return redirect('/dashboard/logout')
        else:
            status = "Wrong"
        form = DeleteAccount()
    context = {
        "form": form,
        "status": status
    }
    return render(request, '../../drone_system/templates/drone_system/deleteaccount.html', context)


def logout(request):
    del request.session['username']
    return redirect('/home/')
