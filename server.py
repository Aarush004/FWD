from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/home")
def index():
    return render_template("index.html",login_page_link = "Login", booking_page_link = "Booking")
                                                
@app.route("/Booking")
def booking():
    return render_template("Booking.html")

@app.route("/Login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("Login.html")
    elif request.method == "POST":
        return render_template("demo.html", userid = request.form["user_id"])
@app.route("/Sign_Up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("Sign_Up.html")
    elif request.method == "POST":
        return render_template("demo.html", userid = request.form["user_id"])
if __name__ == "__main__":
    app.debug = True
    app.run()
