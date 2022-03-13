from flask import Blueprint, render_template
from .models import Appointment, Customer, Employee, Employee_Assignment, Event_Status, Event_Category, Event_Order, Event_Order_Line, Payment, Payment_Type, Product_Service, State, Vendor, Vendor_Service
from . import db


my_view = Blueprint('my_view', __name__)


# Routes to html views with GET requests
@my_view.route("/")
def index():

    CustomerList = Customer.query.join(Event_Order, Customer.Customer_ID == Event_Order.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Event_Order.Event_Time, Customer.Customer_ID)
    
    return render_template('index.html', customers = CustomerList)

@my_view.route('/event/<eventID>')
def event(eventID):

    Event = Event_Order.query.join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Event_Order.Event_Location_Name, 
        Event_Order.Event_Order_Desc, Event_Order.Event_Time, Event_Order.Event_Setup, Event_Order.Event_Delivery, Event_Order.Event_Restriction_Desc)\
            .filter_by(Customer_ID = eventID)
    
    eStatus = Event_Order.query.join(Event_Status, Event_Order.Event_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Event_Status.Event_Status)\
                
    
    return render_template('event.html', event = Event)

@my_view.route('/event')
def viewEvent():
    return render_template('event.html')


@my_view.route('/viewTables')
def viewTables():
    return render_template('viewtables.html')

@my_view.route('/Appointment')
def viewAppointment():
    return render_template('tables/Appointment.html')


@my_view.route('/Customer')
def viewCustomer():
    return render_template('tables/Customer.html', test_table = Test_Table.query.all())


@my_view.route('/Employee')
def viewEmployee():
    return render_template('tables/Employee.html', test_table = Test_Table.query.all())

@my_view.route('/EmployeeAssignment')
def viewEmployeeAssignment():
    return render_template('tables/EmployeeAssignment.html', test_table = Test_Table.query.all())

@my_view.route('/EventCategory')
def viewEventCategory():
    return render_template('tables/EventCategory.html', test_table = Test_Table.query.all())


@my_view.route('/eventOrder')
def viewEventOrder():
    return render_template('tables/eventorder.html', test_table = Test_Table.query.all())
  
@my_view.route('/EventOrderLine')
def vEventOrderLine():
    return render_template('tables/EventOrderLine.html', test_table = Test_Table.query.all())

@my_view.route('/EventStatus')
def viewEventStatus():
    return render_template('tables/EventStatus.html', test_table = Test_Table.query.all())

@my_view.route('/Payment')
def viewPayment():
    return render_template('tables/Payment.html', test_table = Test_Table.query.all())

@my_view.route('/PaymentType')
def viewPaymentType():
    return render_template('tables/PaymentType.html', test_table = Test_Table.query.all())


@my_view.route('/ProductService')
def viewProductService():
    return render_template('tables/ProductService.html', test_table = Test_Table.query.all())


@my_view.route('/State')
def viewState():
    return render_template('tables/State.html', test_table = Test_Table.query.all())

@my_view.route('/Vendor')
def viewVendor():
    return render_template('tables/Vendor.html', test_table = Test_Table.query.all())

@my_view.route('/VendorService')
def viewVendorService():
    return render_template('tables/VendorService.html', test_table = Test_Table.query.all())

@my_view.route('/createDB')
def createdb():
    return render_template('/', db.create_all())