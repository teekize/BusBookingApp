from flask import Flask,g, request, render_template, url_for,redirect,flash,jsonify,send_file
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from io import BytesIO
from werkzeug.security import check_password_hash
from peewee import *
from models import User, create_tables, Safari,Booking
from api2pdf import Api2Pdf
# from pay import mpesa

from pprint import pprint as pp

fika =Flask(__name__)
fika.secret_key ="1222564"

a2p_client = Api2Pdf('2e70670c-add5-40e4-8fdc-8d6be87596ce')

login_manager= LoginManager()
login_manager.init_app(fika)
login_manager.login_view='user_login'

@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(int(userid))
    except DoesNotExist:
        return None

@fika.before_request
def before_request():
    g.user=current_user

def email_exist(email):
    """
    this method checks if simmillar email exists
    """
    mail = User.select().where(email == email)
    return mail

@fika.route('/', methods=["GET"])
def homepage():
   return render_template("index.html")

@fika.route('/.webhook/mpesa', methods=["POST"])
def webhook():
    
    print('\n\n--- Received M-Pesa webhook ---\n\n')
    content = request.json
    pp(content)

    
    print('\n\n--- End ---\n\n')
    return jsonify({"statusCode": 200, "status": "success"})

@fika.route('/search', methods=["GET"])
def search():
    """
    for any data thta is sent in a form but the method is get
    the data isn the request is found in the args
    ie: request.args["name]
    """
    # data = [request.args["from"],request.args["destination"], request.args['date']]  
    safaris =Safari.search_safari(request.args["destination"], request.args["from"])

    for safari in safaris:
        print (safari.get('id'))
    if not safaris:
        return "none journey as such"

    return render_template("buses.html", buses = safaris)
    

@fika.route('/register', methods=["POST","GET"])
def register():
    """
    with this view one can be able to register to the application
    """
    if request.method == 'POST': 
       
        data = [
                request.form['First_Name'],
                 request.form['Last_Name'], 
                 request.form['Email'], 
                 request.form['Password']
                ]

        for name in data:
            print(name)

        response =User.add_user(data[0], data[1], data[2], data[3])

        if response != "e":
            flash (f"welcome {request.form['Last_Name']}")
            return redirect(url_for('homepage'))
    return render_template('register.html')

@fika.route("/user-login", methods=["GET","POST"])
def user_login():
    if request.method == "POST":
        form_data = [request.form['email'],request.form['password']]
        
        try:
            user=User.get(User.email==form_data[0])
        except DoesNotExist:
            return "user does not exists"
        else:
            if check_password_hash(user.password, form_data[1]):

                login_user(user)
                flash("You've been logged in ")
                return redirect(url_for("homepage"))
            else:
                flash(" Your email or password does not match !", "error")
    return render_template("login.html")
       



@fika.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you have been looged out! come back soon")
    return redirect(url_for("homepage"))

    
@fika.route('/resp',methods=["GET"])
def resp():
    return render_template("resp.html")

@fika.route('/make_booking/<int:journey_id>', methods=["POST","GET"])
@login_required
def bookings(journey_id):
    if request.method=="POST":
        user =g.user._get_current_object()
        safari_id = journey_id

        add_booking= Booking.create_bk(safari_id, user)
        if add_booking:

            print (add_booking)
            return redirect(url_for("my_bookings"))
    return render_template("index.html")

# @fika.route('/cancel_booking', methods=["PUT"])
# def bookings():
#     if request.method!="PUT":
#         return render_template("error.html")
    
#     form_data =request.form["booking_id"]
#     user =request.token["token"]

#     add_booking= Bookings.cancel_booking(form_data, user)

#     bookings = Bookings.select(id, jounery_id).where(booked_by=user)
#     return render_template("bookings_made.html")


# @fika.route('/pay/<int:booking_id>', methods=["GET", "POST"])
# def pay(booking_id):
#     if request.method=="POST":
#         form_data = [request.form["phone_number"], request.form["amount"]]
        

#         booking = Booking.get(id=booking_id)
#         if not booking:
#             return "No booking with that id"
        
#         mpesa_response = mpesa.make_stk_push(form_data[0], form_data[1])
#         return mpesa_response["ResponseCode"]

#     return redirect(url_for('my_bookings'))

@fika.route('/add_safari', methods=["GET", "POST"])
@login_required
def add_safari():
    if request.method== "POST":
        # print(g.user.id)
        # user =User.get().where(id=g.user.id)
        # if user == False:
        #     return "Wewe you are not admin pole"
        
        # print(g.user.id)
        form_data = [
                    request.form['bus_number'],
                    request.form['from'],
                    request.form['Destination'],
                    request.form['depature_date']
                    ]
        user =current_user.id
        
        add_safari = Safari.create_safari(form_data[0],form_data[1],form_data[2],form_data[3],user)
        return redirect("all_safaris")

    return render_template("add_bus.html")

@fika.route('/all_safaris', methods=["GET"])
@login_required
def all_safaris():
    all_safaris =Safari.select().dicts()
    if not all_safaris:
        return "None found"
    return render_template("all_safaris.html", buses =all_safaris )

# @fika.route('/all_payments', methods=["GET"])
# def all_payments():
#     all_payments =Payments.select(id, mpesa_ref, amount, paid_by)
#     if not all_payments:
#         return render_template("not_found.html")
#     return render_template("all_payments.html", data =all_safaris )

@fika.route('/all_bookings', methods=["GET"])
@login_required
def all_bookings():
    all_bookings =Booking.select().dicts()
    if not all_bookings:
        return "None"
    return render_template("all_bookings.html", data =all_bookings )

@fika.route('/my_bookings', methods=["GET"])
@login_required
def my_bookings():
    all_bookings =Booking.select().where(Booking.booked_by_id==current_user.id).dicts()
    if not all_bookings:
        return "None"
    return render_template("all_bookings.html", data =all_bookings )

# @fika.route('/load', methods=['GET'])
# def load():
#     url =url_for("download",id_=1)

#     api_response = a2p_client.HeadlessChrome.convert_from_html(url, inline_pdf=True, file_name='test.pdf')

#     print(api_response)
#     return "api_response['pdf']"
    

@fika.route("/download/<int:id_>", methods=["GET"])
def download(id_):
    id_=id_
    ticket =Booking.select().where(Booking.id== id_).dicts()
    # safari =Safari.select().where(Safari.id == ticket.safari_booked_id).dicts()
    rendered= render_template('ticket.html', data=ticket) 
    api_response = a2p_client.HeadlessChrome.convert_from_html(rendered, inline_pdf=True, file_name='test.pdf')
    link =api_response.result['pdf']

    return link

if __name__ == "__main__":
    create_tables()
    admin= User.add_user("admin", "admin", "admin@gmail.com","admin", is_admin=True)
    fika.run(debug= True)