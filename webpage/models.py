from django.db import models
from django.db import connection
from decimal import Decimal


# Create your models here.

class User(models.Model):
    """User details are stored in user table"""
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=30)
    phone_no = models.IntegerField()
    gender = models.CharField(max_length=1)

    @staticmethod
    def authenticate(username, password):
        """Used to validate a user"""
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user:
            if user.password == password:
                return user
        return None

    def __str__(self):
        """To represent the data in txt format"""
        return f"<username : {self.username}, gender : {self.gender}>"
    
class Hotel(models.Model):
    """Hotel details"""
    name = models.CharField(max_length=25)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    location = models.CharField(max_length=25)
    room_2b_available = models.IntegerField()
    room_2b_price = models.DecimalField(max_digits=8, decimal_places=2)
    room_3b_available = models.IntegerField()
    room_3b_price = models.DecimalField(max_digits=8, decimal_places=2)
    food_price = models.DecimalField(max_digits=8, decimal_places=2)

    @staticmethod
    def filter_hotels(rating=0, location='chennai', 
                  room_type='2_br', rooms='1', food='off', days=1):

        with connection.cursor() as cursor:
            if room_type == "2_br":
                query = (
                    "SELECT id, name, location, rating, room_2b_available, room_2b_price, food_price "
                    "FROM webpage_hotel "
                    "WHERE location=%s AND rating>=%s AND room_2b_available>=%s;"
                )
                room_price = "2 BedRoom price"
                room_name = "2 BedRoom available"
            else:
                query = (
                    "SELECT id, name, location, rating, room_3b_available, room_3b_price, food_price "
                    "FROM webpage_hotel "
                    "WHERE location=%s AND rating>=%s AND room_3b_available>=%s;"
                )
                room_price = "3 BedRoom price"
                room_name = "3 BedRoom available"
            cursor.execute(query, [location, rating, rooms])
            data = cursor.fetchall()
            for i, tup in enumerate(data):
                total_room_price = tup[5]*Decimal(rooms)*Decimal(days)
                total_food_price = 0
                if food == 'on':
                    total_food_price = tup[6]*Decimal(days)
                txt = (f"{'Name':<25} : {tup[1]}\n" +
                       f"{'Location':<25} : {tup[2]}\n" +
                       f"{'Rating':<25} : {tup[3]}\n" +
                       f"{'No. of days':<25} : {days}\n" +
                       f"{'No. of rooms':<25} : {rooms}\n" +
                       f"{'Total Room price':<25} : ₹ {total_room_price}\n" +
                       f"{'Total Food price':<25} : ₹ {total_food_price}\n" +
                       f"{'Total amount':<25} :₹ {total_room_price +total_food_price}\n")
                tup2 = (txt,) + tup
                data[i] = tup2 
            final_data = [("Name", "Location", "Rating", room_name, room_price, 
                     "Food price", "Action")] + data
        return final_data

    
class Hotel_Bookings(models.Model):
    """hotel Booking details"""
    # id is already automatically created django 
    hotel_id = models.IntegerField()
    user_id = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    food = models.CharField(max_length=5)
    room_count_2b = models.IntegerField(null=True)
    room_count_3b = models.IntegerField(null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @staticmethod
    def get_bookings(user_id):
        with connection.cursor() as cursor:
            query = """
                SELECT
                    h.name as "Hotel Name",
                    h.location as "Location",
                    hb.food as "Food",
                    hb.room_count_2b + hb.room_count_3b as "No. of Rooms",
                    hb.price as "Total Price",
                    hb.booking_date as "Booking Date",
                    hb.from_date as "Check-in Date",
                    hb.to_date as "Check-out Date",
                    hb.id as "Id"
                FROM
                    webpage_Hotel h
                INNER JOIN
                    webpage_Hotel_bookings hb ON h.id = hb.hotel_id
                WHERE
                    hb.user_id = %s
                """
            cursor.execute(query, [user_id])
            result = cursor.fetchall()

        return result


