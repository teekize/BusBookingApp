from flask import Flask, request, render_template, url_for

fika =Flask(__name__)


@fika.route('/', methods=["GET"])
def homepage():
   return render_template("index.html")

@fika.route('/user-register', methods=["GET"])
def user_register():
    return render_template("register.html")


@fika.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@fika.route('/safari', methods=["GET"])
def add_safari():
    return render_template("buses.html")

@fika.route('/booking_info', methods=["GET"])
def bookings():
    return render_template("contacts.html")



if __name__ == "__main__":
    fika.run()