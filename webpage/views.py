from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from urllib.parse import urlencode
from .models import *
from datetime import datetime, timedelta
from decimal import Decimal


def Main(request):
    request.user = None
    return render(request, 'Main.html')


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = User.authenticate(username, password)
        if user is None:
            context = {"error" : "true"}
            return render(request, 'Login.html', context)
        request.session['user_id'] = user.id
        return redirect('Home')

    if request.method == "GET":
        error = request.GET.get('error', "false")
        context = {"error" : error}
        return render(request, 'Login.html', context)


def Home(request):
    if request.method == "POST":
        icon = request.POST.get("icon")
        hotel_id = request.POST.get("hotelId")
        context = {}

        # Payment processing
        if hotel_id is not None:
            user_id = request.session['user_id']
            filter_dict = request.session['filter_dict']

            if filter_dict['room_type'] == '2_br':
                room_count_2b = filter_dict['rooms']
                room_count_3b = None
            else:
                room_count_2b = None
                room_count_3b = filter_dict['rooms']
            price = calc_price(hotel_id, filter_dict)
            
            # creating a booking object
            booking = Hotel_Bookings(hotel_id=hotel_id, 
                user_id=user_id, booking_date=current_date(),
                food = filter_dict['food'],
                room_count_2b=room_count_2b,
                room_count_3b=room_count_3b,
                from_date=filter_dict['from_date'],
                to_date=filter_dict['to_date'],
                price=price)
            booking.save()
            context = {"payment" : True}
            return render(request, 'Home.html', context)


        # Applying Filters
        elif icon == "hotel":
            # Filters with default values 
            rating = request.POST.get('hotel_rating')
            location = request.POST.get('hotel_location')
            food = request.POST.get('food')
            if food is None:
                food = "off"
            room_type = request.POST.get('room_type')
            rooms = request.POST.get('room_count')
            if rooms == '':
                rooms = '1'
            checkin_date = request.POST.get('checkin_date')
            if not checkin_date:
                checkin_date = current_date()
            checkout_date = request.POST.get('checkout_date')
            if not checkout_date:
                checkout_date = current_date(1)
            if checkin_date == '' or checkout_date == '':
                tot_days = 1
            else:
                tot_days = calc_date_diff(checkin_date, checkout_date)

            # filter dictionary
            filter_dict = {'rating' : rating, 
                           'location' : location, 
                           'room_type' : room_type, 
                          'rooms' : rooms, 
                          'food' : food,
                          'tot_days' : tot_days,
                          'from_date' : checkin_date,
                          'to_date' : checkout_date}

            request.session['filter_dict'] = filter_dict
            table = Hotel.filter_hotels(rating, location, room_type,
                                        rooms, food, tot_days)
            context = {"table_header":table[0], "table_data" : table[1:]}

        return render(request, 'Home.html', context)

            
    if request.method == "GET":
        return render(request, 'Home.html')


def MyBookings(request):
    context = {}
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        hotel_booking = Hotel_Bookings.objects.get(id=booking_id)
        hotel_booking.delete()
        context.update({'cancelation' : 'True'})
    
    user_id = request.session['user_id']
    booking_data = Hotel_Bookings.get_bookings(user_id)
    context.update({'booking_data': booking_data})
    return render(request, 'MyBookings.html', context)


def Help(request):
    return render(request, 'Help.html')


# Functionalaities
def calc_date_diff(date_str1, date_str2):
    # Convert strings to datetime objects
    date_object1 = datetime.strptime(date_str1, "%Y-%m-%d")
    date_object2 = datetime.strptime(date_str2, "%Y-%m-%d")

    # Calculate the date difference
    date_difference = date_object2 - date_object1

    # Access the days from the timedelta object
    days_difference = date_difference.days

    return days_difference


def current_date(days=0):
    date = datetime.now().date()
    date += timedelta(days=days)
    date_str = date.strftime("%Y-%m-%d")
    return date_str


def calc_price(hotel_id, filters):
    hotel = Hotel.objects.get(id=hotel_id)
    food_price = 0

    if filters['room_type'] == '2_br':
        room_price = Decimal(hotel.room_2b_price)
    else:
        room_price = Decimal(hotel.room_3b_price)

    room_price *= Decimal(filters['rooms'])
    if filters['food'] == 'on':
        food_price = Decimal(hotel.food_price)

    total_price = ((room_price + food_price)
        *Decimal(filters['tot_days']))
    return total_price

    