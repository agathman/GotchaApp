from . import db

class Appointment(db.Model):
    __tablename__ = 'Appointment'
    Appointment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Event_Order_ID = db.Column(db.Integer, db.ForeignKey('Event_Order.Event_Order_ID'), nullable=False)

    def __repr__(self, Appointment_ID, Customer_ID, Event_Order_ID):
        self.Appointment_ID = Appointment_ID
        self.Customer_ID = Customer_ID
        self.Event_Order_ID = Event_Order_ID

class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Contact_Date = db.Column(db.Date)
    First_Name = db.Column(db.String)
    Last_Name = db.Column(db.String)
    Phone = db.Column(db.String)
    Email = db.Column(db.String)
    Mailing_Address = db.Column(db.String)
    Mailing_City = db.Column(db.String)
    State_ID = db.Column(db.Integer, db.ForeignKey('State.State_ID'))
    Mailing_Zip_Code = db.Column(db.String)


class Employee(db.Model):
    __tablename__ = 'Employee'
    Emp_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Emp_First_Name = db.Column(db.String)
    Emp_Last_Name = db.Column(db.String)
    Emp_Mailing_City = db.Column(db.String)
    State_ID = db.Column(db.Integer, db.ForeignKey('State.State_ID'))
    Emp_Zip_Code = db.Column(db.String)
    Emp_Phone = db.Column(db.String)
    Emp_Email = db.Column(db.String)
    Emp_Position = db.Column(db.String)

class Employee_Assignment(db.Model):
    __tablename__ = 'Employee_Assignment'
    Employee_Assignment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Assignment_Start_Date = db.Column(db.Date)
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employee.Emp_ID'))

class Event_Category(db.Model):
    __tablename__ = 'Event_Category'
    Event_Category_ID = db.Column('Event_Category_ID', db.Integer, primary_key=True, autoincrement=True)
            

class Event_Order(db.Model):
    __tablename__ = 'Event_Order'
    Event_Order_ID = db.Column(db.Integer, primary_key=True, autoincrement= True)
    Event_Category_ID = db.Column(db.Integer, db.ForeignKey('Event_Category.Event_Category_ID'), nullable=False)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Event_Status_ID = db.Column(db.Integer, db.ForeignKey('Event_Status.Event_Status_ID'), nullable=False)
    Event_Time = db.Column(db.Date, nullable=False)
    Event_Theme = db.Column(db.String, nullable=False)
    Event_Order_Desc = db.Column(db.String, nullable=False)
    Event_Delivery = db.Column(db.String, nullable=False)
    Event_Setup = db.Column(db.String, nullable=False)
    Event_Location_Name = db.Column(db.String, nullable=False)
    Event_Delivery = db.Column(db.String, nullable=False)
    Event_Setup = db.Column(db.String, nullable=False)
    Event_Restriction_Desc = db.Column(db.String, nullable=False)
    Event_Order_Desc = db.Column(db.String, nullable=False)
    Event_Address = db.Column(db.String, nullable=False)
    Event_City = db.Column(db.String, nullable=False)
    State_ID = db.Column(db.Integer, db.ForeignKey('State.State_ID'), nullable=False)
    Event_Zip_Code = db.Column(db.Integer, nullable=False)
    Employee_Assignment_ID = db.Column(db.Integer, db.ForeignKey('Employee_Assignment.Employee_Assignment_ID'))
    Feedback = db.Column(db.Integer)


# Class method to GET from DB

    def __repr__(self, Event_Order_ID, Event_Category_ID, Customer_ID, Event_Order_Status_ID, Event_Time, Event_Theme, Event_Order_Desc, Event_Delivery, Event_Setup, 
                                Event_Location_Name, Event_Restriction_Desc, Event_Address, Event_City, State_ID, Event_Zip_Code, Employee_Assignment_ID, Feedback):
        # Defines representation for object
            self.Event_Order_ID = Event_Order_ID
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
            self.State_ID = State_ID
            self.Event_Zip_Code = Event_Zip_Code
            self.Employee_Assignment_ID = Employee_Assignment_ID
            self.Feedback = Feedback
            

class Event_Order_Line(db.Model):
    __tablename__ = 'Event_Order_Line'
    Event_Order_Line_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Event_Status(db.Model):
    __tablename__ = 'Event_Status'
    Event_Status_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Payment(db.Model):
    __tablename__ = 'Payment'
    Payment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Payment_Type(db.Model):
    __tablename__ = 'Payment_Type'
    Payment_Type_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Product_Service(db.Model):
    __tablename__ = 'Product_Service'
    Product_Service_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class State(db.Model):
    __tablename__ = 'State'
    State_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Vendor(db.Model):
    __tablename__ = 'Vendor'
    Vender_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Vendor_Service(db.Model):
    __tablename__ = 'Vendor_Service'
    Vendor_Service_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)






db.session


#Object Modeling for tables
#Object Modeling for tables



class Test_Table(db.Model):
    __tablename__ = 'Test_Table'
    Test_Data = db.Column(db.Integer, primary_key=True, autoincrement= True)
    Test_Data2 = db.Column(db.String)

    def __repr__(self, Test_Data, Test_Data2):
            self.Test_Data = Test_Data 
            self.Test_Data2 = Test_Data2
            