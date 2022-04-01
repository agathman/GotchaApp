from . import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'Appointment'
    Appointment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Event_Order_ID = db.Column(db.Integer, db.ForeignKey('Event_Order.Event_Order_ID'), nullable=True)
    Datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, Customer_ID, Datetime):
        self.Customer_ID = Customer_ID
        self.Datetime = Datetime

class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    First_Name = db.Column(db.String(250))
    Last_Name = db.Column(db.String (250))
    Phone = db.Column(db.String(12))
    Email = db.Column(db.String(250))
    Mailing_Address = db.Column(db.String (250))
    Mailing_City = db.Column(db.String(250))
    State_ID = db.Column(db.Integer, db.ForeignKey('State.State_ID'))
    Mailing_Zip_Code = db.Column(db.String(10))

    Event_Order = relationship("Event_Order", backref="Customer")

    def __init__(self, First_Name, Last_Name, Phone, Email, Mailing_Address, Mailing_City, Mailing_Zip_Code, State_ID):
       
        self.First_Name = First_Name
        self.Last_Name = Last_Name
        self.Phone = Phone
        self.Email = Email
        self.Mailing_Address = Mailing_Address
        self.Mailing_City = Mailing_City
        self.Mailing_Zip_Code = Mailing_Zip_Code
        self.State_ID = State_ID


#form created
class Employee(db.Model):
    __tablename__ = 'Employee'
    Emp_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Emp_First_Name = db.Column(db.String(50))
    Emp_Last_Name = db.Column(db.String(50))
    Emp_Mailing_Address = db.Column(db.String(250))
    Emp_Mailing_City = db.Column(db.String(100))
    State_ID = db.Column(db.Integer, db.ForeignKey('State.State_ID'))
    Emp_Zip_Code = db.Column(db.String(10))
    Emp_Phone = db.Column(db.String(12))
    Emp_Email = db.Column(db.String(100) )
    Emp_Position = db.Column(db.String(50))

    def __init__(self,Emp_First_Name, Emp_Last_Name, Emp_Mailing_Address, Emp_Mailing_City, State_ID,Emp_Zip_Code, Emp_Phone, Emp_Email, Emp_Position):
        self.Emp_First_Name = Emp_First_Name
        self.Emp_Last_Name = Emp_Last_Name
        self.Emp_Mailing_Address = Emp_Mailing_Address
        self.Emp_Mailing_City =Emp_Mailing_City
        self.State_ID = State_ID
        # Tanya- I added this
        self.Emp_Zip_Code= Emp_Zip_Code
        self.Emp_Phone = Emp_Phone
        self.Emp_Email =Emp_Email
        self.Emp_Position =Emp_Position

#form created

class Employee_Assignment(db.Model):
    __tablename__ = 'Employee_Assignment'
    Employee_Assignment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Assignment_Start_Date = db.Column(db.Date)
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employee.Emp_ID'))

    def __init__(self, Assignment_Start_Date, Employee_ID):
        self.Assignment_Start_Date = Assignment_Start_Date
        self.Employee_ID = Employee_ID


#form created
class Event_Category(db.Model):
    __tablename__ = 'Event_Category'
    Event_Category_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_Category_Name = db.Column(db.String(150), nullable=False)

    def __init__(self, Event_Category_Name):
        self.Event_Category_Name = Event_Category_Name       
#form created
class Event_Order(db.Model):
    __tablename__ = 'Event_Order'
    Event_Order_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_Category_ID = db.Column(db.Integer, db.ForeignKey('Event_Category.Event_Category_ID'), nullable=False)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Event_Order_Status_ID = db.Column(db.Integer, db.ForeignKey('Event_Status.Event_Status_ID'), nullable=False)
    Event_Time = db.Column(db.Date, nullable=False)
    Event_Theme = db.Column(db.String(250), nullable=False)
    Event_Order_Desc = db.Column(db.String (250), nullable=False)
    Event_Delivery = db.Column(db.String (100), nullable=False)
    Event_Setup = db.Column(db.String (250), nullable=False)
    Event_Location_Name = db.Column(db.String(250), nullable=False)
    Event_Restriction_Desc = db.Column(db.String(250), nullable=False)
    Event_Address = db.Column(db.String(250), nullable=False)
    Event_City = db.Column(db.String(100), nullable=False)
    State_ID = db.Column(db.Integer, db.ForeignKey('State.State_ID'), nullable=False)
    Event_Zip_Code = db.Column(db.Integer, nullable=False)
    Employee_Assignment_ID = db.Column(db.Integer, db.ForeignKey('Employee_Assignment.Employee_Assignment_ID'))
    Feedback = db.Column(db.Integer)

    

    def __init__(self, Event_Category_ID, Customer_ID, Event_Order_Status_ID, Event_Time, Event_Theme, Event_Order_Desc, Event_Delivery, Event_Setup, 
                                Event_Location_Name, Event_Restriction_Desc, Event_Address, Event_City, Event_Zip_Code, Employee_Assignment_ID, State, Feedback):
        # Defines representation for object
            
            self.Event_Category_ID = Event_Category_ID
            self.Customer_ID = Customer_ID
            self.Event_Order_Status_ID = Event_Order_Status_ID
            self.Event_Time = Event_Time
            self.Event_Theme = Event_Theme
            self.Event_Order_Desc = Event_Order_Desc
            self.Event_Delivery = Event_Delivery
            self.Event_Setup = Event_Setup
            self.Event_Location_Name = Event_Location_Name
            self.Event_Restriction_Desc = Event_Restriction_Desc
            self.Event_Address = Event_Address
            self.Event_City = Event_City
            self.State_ID = State
            self.Event_Zip_Code = Event_Zip_Code
            self.Employee_Assignment_ID = Employee_Assignment_ID
            self.Feedback = Feedback
            
#form created
class Event_Order_Line(db.Model):
    __tablename__ = 'Event_Order_Line'
    Event_Order_Line_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vendor_ID = db.Column(db.Integer, db.ForeignKey('Vendor.Vendor_ID'), nullable=True)
    Event_Order_Status_ID = db.Column(db.Integer,db.ForeignKey('Event_Category.Event_Category_ID'), nullable=False)
    Event_Order_Line_Date = db.Column(db.Date, nullable=False)
    Event_Order_ID = db.Column(db.Integer, db.ForeignKey('Event_Order.Event_Order_ID'), nullable=True)
    Product_Service_ID = db.Column(db.Integer, db.ForeignKey('Product_Service.Product_Service_ID'), nullable=False)

# Class method to GET from DB

    def __init__(self, Vendor_ID, Event_Order_Status_ID,
                Event_Order_Line_Date, Event_Order_ID, Product_Service_ID):
# Defines representation for object

            self.Vendor_ID = Vendor_ID
            self.Event_Order_Status_ID = Event_Order_Status_ID
            self.Event_Order_Line_Date = Event_Order_Line_Date
            self.Event_Order_ID = Event_Order_ID
            self.Product_Service_ID = Product_Service_ID

#form created
class Event_Status(db.Model):
    __tablename__ = 'Event_Status'
    Event_Status_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Event_Status = db.Column(db.String(50), nullable=False)

    Event_Order = relationship('Event_Order', backref='Event_Status') 

    def __init__(self, Event_Status):
        self.Event_Status = Event_Status
#form created
class Payment(db.Model):
    __tablename__ = 'Payment'
    Payment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Payment_Type_ID = db.Column(db.Integer, db.ForeignKey('Payment_Type.Payment_Type_ID'), nullable=False)
    Event_Order_ID = db.Column(db.Integer, db.ForeignKey('Event_Order.Event_Order_ID'), nullable=False)
    Payment_Date_Init = db.Column(db.Date, nullable=False)
    Payment_Date_Full = db.Column(db.Date, nullable=False)

    def __init__(self, Payment_Type_ID, Event_Order_ID, Payment_Date_Init, Payment_Date_Full):
        self.Payment_Type_ID = Payment_Type_ID
        self.Event_Order_ID = Event_Order_ID
        self.Payment_Date_Init = Payment_Date_Init
        self.Payment_Date_Full = Payment_Date_Full
#form created
class Payment_Type(db.Model):
    __tablename__ = 'Payment_Type'
    Payment_Type_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Payment_Type_Name = db.Column(db.String(50), nullable=False)

    def __init__(self, Payment_Type_Name):
        self.Payment_Type_Name = Payment_Type_Name
#form created
class Product_Service(db.Model):
    __tablename__ = 'Product_Service'
    Product_Service_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Product_Service = db.Column(db.String(50), nullable=False)

    def __init__(self, Product_Service):
        self.Product_Service = Product_Service
#form created
class State(db.Model):
    __tablename__ = 'State'
    State_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    State_Name = db.Column(db.String(20), nullable=False)
    State_Abbreviation = db.Column(db.String(2), nullable=False)

    def __init__(self, State_ID, State_Name, State_Abbreviation):
        self.State_ID = State_ID
        self.State_Name = State_Name
        self.State_Abbreviation = State_Abbreviation
#form created
class Vendor(db.Model):
    __tablename__ = 'Vendor'
    Vendor_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vendor_Name = db.Column(db.String(50), nullable=False)
    Vendor_Service_ID = db.Column(db.Integer, db.ForeignKey('Vendor_Service.Vendor_Service_ID'), nullable=False)
    Vendor_Desc = db.Column(db.String(250), nullable=False)
    First_Name = db.Column(db.String(250), nullable=False)
    Last_Name = db.Column(db.String(250), nullable=False)
    Phone = db.Column(db.String, nullable=False)
    Email = db.Column(db.String(250), nullable=False)

    def __init__(self, Vendor_Name, Vendor_Service_ID, Vendor_Desc, First_Name, Last_Name, Phone, Email):
        self.Vendor_Name = Vendor_Name
        self.Vendor_Service_ID = Vendor_Service_ID
        self.Vendor_Desc = Vendor_Desc
        self.First_Name = First_Name
        self.Last_Name = Last_Name
        self.Phone = Phone
        self.Email = Email

#form creation
class Vendor_Service(db.Model):
    __tablename__ = 'Vendor_Service'
    Vendor_Service_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vendor_Services = db.Column(db.String(50), nullable=False)

    def __init__(self, Vendor_Services):
            self.Vendor_Services = Vendor_Services








            