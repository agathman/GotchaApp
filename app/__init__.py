from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

  
app = Flask(__name__, template_folder="templates", static_folder='assets', instance_relative_config=False)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pymssql://gotchadata:Got1234!@COT-CIS4375-08.cougarnet.uh.edu:1433/GotchaData'
app.config['SECRET_KEY'] = 'secretkey'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db = SQLAlchemy(session_options={"autoflush": False})
db.init_app(app)
    #app.config.from_object('config.config')



with app.app_context():
    from .views import my_view  # Import routess
    app.register_blueprint(my_view)
    from .models import Appointment, Customer, Employee, Employee_Assignment, Event_Status, Event_Category, Event_Order, Event_Order_Line, Payment, Payment_Type, Product_Service, State, Vendor, Vendor_Service
    #db.create_all()
    #db.session.commit()
     
    if __name__ == '__main__':
         app.run(debug = True)




