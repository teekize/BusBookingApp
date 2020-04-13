import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from peewee import *

db = SqliteDatabase('fika.db')


class BaseModel(Model):
    class Meta:
        database =db


class User(UserMixin,BaseModel):
    first_name = CharField()
    last_name =CharField()
    email=CharField(unique=True)
    password= CharField(max_length=110)
    is_admin = BooleanField(default=False)

    

    @classmethod
    def add_user(cls, first_name, last_name, email, password,is_admin=False):
        """
        this classmethod adds the created object and then returns
         the id of the created object
        """
        try:
           user=cls.create(
                first_name= first_name,
                last_name= last_name,
                email= email,
                password= generate_password_hash(password),
                is_admin=is_admin
            )
        #    user = cls.select().where(email == email)
           return user
        except IntegrityError:
            return "e"
    
    @classmethod
    def get_user(cls, id):
        try:
            user=cls.get_by_id(id_)
            return  user
        except DoesNotExist:
            raise ValueError ("User with that id does not exist")

    # @classmethod
    # def login(cls,*args):
    #     user = cls.select(password, email).where(email =mail)

    #     if not user:
    #         return None
        
    #     pass

    @classmethod
    def make_admin(cls, id):
        try:
            user = cls.get_by_id(id_)

            if user:
                cls.is_admin =True
                cls.save(id_)
        except DoesNotExist:
            raise ValueError ("user with that id does not exist")

class Safari(BaseModel):
    bus_number = TextField()
    from_ =CharField()
    Destination =CharField()
    depature_date= CharField()
    created_by =IntegerField()
    # Fare=IntegerField()
    createdon_time= DateTimeField(default = datetime.datetime.now)

    class Meta:
        order_by=('-createdon_time',)

    @classmethod
    def all_safaris(cls):
        safaris = cls.select().dicts()
        return safaris

    @classmethod
    def search_safari(cls,to, from_):
        safari = cls.select().where((cls.Destination== to) & (cls.from_ == from_)).dicts()
        return safari

    @classmethod
    def create_safari(cls,bus_number,from_,Destination,depature_date,user):
        safari =cls.create(
            bus_number =bus_number,
            from_ = from_,
            Destination= Destination,
            depature_date =depature_date,
            created_by = user
        )

        return safari
    
class Booking(BaseModel):
    
    safari_booked_id = ForeignKeyField(Safari, backref="bookings")
    booked_by_id= ForeignKeyField(User, backref="mybookings")
    is_paid = BooleanField(default=False)
    is_cancelled=BooleanField(default=False)
    createdon_time= DateTimeField(default = datetime.datetime.now)

    class Meta:
        order_by=('-createdon_time',)

    # @classmethod
    # def get_all_bookings(cls):
    #     bookings = cls.select(id, safari_booked, booked_by, is_paid, createdon_time)
    #     return bookings

    # @classmethod
    # def search_booking(cls,id):
    #     bookings =cls.select(id, safari_booked, booked_by, is_paid, createdon_time)
    #     if not bookings:
    #         return None
    #     return bookings

    @classmethod
    def create_bk(cls,journey_id, user, is_paid=False, is_cancelled=False):
        
        booking = cls.create(
            safari_booked_id=journey_id,
            booked_by_id=user,
            is_paid=is_paid,
            is_cancelled=is_cancelled
        )

        return booking

    # @classmethod
    # def cancel_booking(id):

    #     booking = cls.select().where(id = id)
    #     if not booking:
    #         return None
        
# class Payment(BaseModel):
#     payment_id= IntegerField(primary_key=True)
#     for_booking=ForeignKeyField(Booking, backref="bookingpay")
#     amount_paid= FloatField()
#     mobile_num = IntegerField()
    

def create_tables():
    with db:
        db.create_tables([User,Safari,Booking,])

# def add_(name_):
#     try:
#         with db.atomic():
#             # Attempt to create the user. If the username is taken, due to the
#             # unique constraint, the database will raise an IntegrityError.
#             user = Booking.create(
#                 booking_id = )1

#         # mark the user as being 'authenticated' by setting the session vars
#         print(user)
#     except IntegrityError:
#         print("same name")
#         # flash('That username is already taken')
# def query(name):
#     user = Booking.select().where(booking_id = 1)
#     print (user)