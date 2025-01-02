from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sqlite3
import time
import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("project.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS auth
    (id VARCHAR PRIMARY KEY,
    pass VARCHAR NOT NULL,
    acc_type VARCHAR NOT NULL)
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS customer
    (id VARCHAR PRIMARY KEY,
    phone INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    FOREIGN KEY(id) REFERENCES auth(id)
    )
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS contractor
    (id VARCHAR PRIMARY KEY,
    phone INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    service VARCHAR NOT NULL,
    FOREIGN KEY(id) REFERENCES auth(id)
    )
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders
    (order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id VARCHAR NOT NULL,
    contractor_id VARCHAR,
    service VARCHAR NOT NULL,
    doa DATE NOT NULL,
    doc DATE,
    amount INTEGER DEFAULT 2000,
    FOREIGN KEY(customer_id) REFERENCES customer(id),
    FOREIGN KEY(contractor_id) REFERENCES contractor(id)
    )
    ''')
    conn.commit()
    conn.close()

logged_in_flag=False
logged_in_id=0
@app.route("/")
def index():
    if logged_in_flag:
        conn = sqlite3.connect("project.db")
        c = conn.cursor()
        if c.execute("select acc_type from auth where id='"+logged_in_id+"'").fetchone()[0] == "contractor":
            return render_template("index.html",left_button_text = "Dashboard", login_page_link = "Dashboard", middle_button_link="Order",middle_button_text="Orders")
        else:
            return render_template("index.html",left_button_text = "Dashboard", login_page_link = "Dashboard", middle_button_link="Booking",middle_button_text="Book Now")
    else:
        return render_template("index.html",left_button_text = "Login", login_page_link = "Login", middle_button_link="Booking",middle_button_text="Book Now")
                                                
@app.route("/Booking", methods = ["GET", "POST"])
def booking():
    conn = sqlite3.connect("project.db")
    c = conn.cursor()
    global logged_in_id
    logged_in_id = str(logged_in_id)
    name=c.execute("select name from customer where id='"+logged_in_id+"'").fetchone() #returning phone no dont know why
    id=logged_in_id
    phone=c.execute("select phone from customer where id='"+logged_in_id+"'").fetchone() #returning name
    address=c.execute("select address from customer where id='"+logged_in_id+"'").fetchone()
    if request.method == "GET":
        if logged_in_flag and name!=None and phone!=None and address!=None:
            return render_template("Booking.html", name = name[0], phone = phone[0], address = address[0])
        elif logged_in_flag:
            return redirect("/Dashboard")
        else:
            return redirect("/Login")
    if request.method == "POST":
        # checking if expected date is after the current date
        x = request.form["date"]
        exp_date = datetime.datetime(int(x[:4]), int(x[5:7]),int(x[-2:]))
        if exp_date > datetime.datetime.now():
            c.execute("insert into orders (customer_id, service, doa) values('"+id+"','"+request.form["service"]+"','"+x+"')")
            conn.commit()
            return redirect("/Dashboard")
        else:
            return render_template("Booking.html", name = name[0], phone = phone[0], address = address[0], error = "Date cannot be before today")


@app.route("/Login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("Login.html")

    elif request.method == "POST":
        #initializing the db instance
        conn = sqlite3.connect("project.db")
        c = conn.cursor()
        #checking if no user exists
        if c.execute("select id from auth where id='"+request.form["user_id"]+"'").fetchone() == None:
            return render_template("Login.html", error="User not found.")
        #checking if password is correct and logging in
        elif request.form["pass"] == c.execute("select pass from auth where id='"+request.form["user_id"]+"'").fetchone()[0]:
            global logged_in_flag
            global logged_in_id
            logged_in_flag=True
            logged_in_id=request.form["user_id"]
            return redirect("/")
            
        else:
            return render_template("Login.html", error="Incorrect Password")
@app.route("/Sign_Up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("Sign_Up.html", password_not_match_error="")
    elif request.method == "POST":
        #initializing the db instance
        conn = sqlite3.connect("project.db")
        c = conn.cursor()
        # checking if both passes are same
        if request.form["pass1"]==request.form["pass2"]:
             # checking if no user exists
            if c.execute("select id from auth where id='"+request.form["user_id"]+"'").fetchone() == None:
                # Checking for customer:
                if request.form.get("s1") == None:
                    c.execute("insert into auth values('"+request.form["user_id"]+"','"+request.form["pass1"]+"', 'customer')")
                else:
                    c.execute("insert into auth values('"+request.form["user_id"]+"','"+request.form["pass1"]+"', 'contractor')")
                conn.commit()
                return render_template("Sign_Up.html", success = "User created succesfully, please login.")
            else:
                return render_template("Sign_Up.html", error="User already exists")
        else:
            return render_template("Sign_Up.html", error = "Passwords do not match, please try again.")
@app.route("/Dashboard", methods = ["GET", "POST"])
def dashboard():
    conn = sqlite3.connect("project.db")
    c = conn.cursor()
    global logged_in_id
    logged_in_id = str(logged_in_id)
    name=c.execute("select name from customer where id='"+logged_in_id+"'").fetchone() #returning phone no dont know why
    id=logged_in_id
    phone=c.execute("select phone from customer where id='"+logged_in_id+"'").fetchone() #returning name
    address=c.execute("select address from customer where id='"+logged_in_id+"'").fetchone()
    if request.method == "GET":
        if name!=None and phone!=None and address!=None:
            prev_orders=c.execute("select order_id, service,doa,doc from orders").fetchall()
            if prev_orders != None:
                return render_template("Dashboard_filled.html", name=name[0], id=id, phone=phone[0],address=address[0], prev_orders=prev_orders)
            else:
                return render_template("Dashboard_filled.html", name=name[0], id=id, phone=phone[0],address=address[0], empty_prev_orders="You haven't made any orders yet.")
        else:
            return render_template("Dashboard_empty.html",id=id)
    elif request.method == "POST":
        name=request.form["name"]
        phone=request.form["phone"]
        address=request.form["address"]
        c.execute("insert into customer values('"+id+"','"+phone+"','"+name+"','"+address+"')")
        conn.commit()
        return render_template("Dashboard_filled.html", name=name, id=id, phone=phone,address=address, success="Values updated successfully")

@app.route("/Order", methods = ["GET", "POST"])
def order():
    return render_template("Order.html")
if __name__ == "__main__":
    init_db()
    app.debug = True
    app.run()

# select order_id, service, doa, doc, 