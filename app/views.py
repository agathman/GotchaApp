from flask import Blueprint, redirect, render_template, request, flash, url_for, redirect
from .models import Appointment, Customer, Employee, Employee_Assignment, Event_Status, Event_Category, Event_Order,\
                    Event_Order_Line, Payment, Payment_Type, Product_Service, State, Vendor, Vendor_Service
from . import db



my_view = Blueprint('my_view', __name__)



# Routes to html views with GET requests
@my_view.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        #Form request to add customer
        #Checks which form to add from
        if request.form['check'] == 'customer':
            customer = Customer(request.form['firstName'], request.form['lastName'], request.form['phone'],
                        request.form['email'], request.form['address'], request.form['city'], request.form['zip'], request.form['date'], request.form['state'])
            db.session.add(customer)
            db.session.commit()
        #Form request to add appointment
        elif request.form['check'] == 'appointment':
            appointment = Appointment(request.form['customerID'], request.form['date'])
            db.session.add(appointment)
            db.session.commit()
        #Form request to add event
        elif request.form['check'] == 'event':
            event = Event_Order(request.form['category'], request.form['customer'], request.form['status'], request.form['eventTime'], request.form['theme'], request.form['eventDesc'],
                        request.form['delivery'], request.form['setup'], request.form['location'], request.form['restrictions'], request.form['address'], request.form['city'],
                        request.form['zip'],2, 1, 'Due after event')
            db.session.add(event)
            db.session.commit()
    
    #Query to find customer names with associated events    
    CustomerList = Customer.query.join(Event_Order, Customer.Customer_ID == Event_Order.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Event_Order.Event_Time, Customer.Customer_ID)
    
    #Query to find customer names with associated appointments
    AppointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Appointment.Date)
    
    return render_template('index.html', customers = CustomerList, newAppointment = Customer.query.all(), appointments = AppointmentList, eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all())

@my_view.route("/", methods=['GET', 'POST'])
def addCustomerModal():

    return(render_template("addCustomerModal.html"))

#View single event info
@my_view.route('/event/<eventID>')
def event(eventID):

    Event = Event_Order.query.join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Event_Order.Event_Time, 
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Location_Name,
        Event_Order.Event_Restriction_Desc, Event_Order.Event_Address, Event_Order.Event_City)\
            .filter_by(Customer_ID = eventID)
                
    
    return render_template('event.html', event = Event)
#View all events
@my_view.route('/events')
def viewEvent():
    
    Events = Event_Order.query.join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Event_Order.Event_Time, 
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Location_Name,
        Event_Order.Event_Restriction_Desc, Event_Order.Event_Address, Event_Order.Event_City)\

    return render_template('tables/events.html', events = Events)


@my_view.route('/viewTables')
def viewTables():
    return render_template('viewtables.html')

#View Appointments
@my_view.route('/Appointments')
def viewAppointment():
    
    Appointments = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Appointment.Appointment_ID, Customer.Customer_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Appointment.Date)

    return render_template('tables/appointment.html', appointments = Appointments, customers = Customer.query.all())


@my_view.route('/Customer')
def viewCustomer():
#State abb
    Customers = Customer.query.join(State, Customer.State_ID == State.State_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Customer.Mailing_Address, Customer.Mailing_City, 
                     Customer.Mailing_Zip_Code, Customer.Contact_Date, State.State_Abbreviation)

    return render_template('tables/customer.html', customers = Customers )


@my_view.route('/Employee')
def viewEmployee():
    Employees = Employee.query.join(State, Employee.State_ID == State.State_ID)\
        .add_columns(Employee.Emp_ID, Employee.Emp_First_Name, Employee.Emp_Last_Name, Employee.Emp_Mailing_Address, Employee.Emp_Mailing_City, 
                     State.State_Abbreviation, Employee.Emp_Zip_Code, Employee.Emp_Phone, Employee.Emp_Email, Employee.Emp_Position)
 
    return render_template('tables/employee.html', employees = Employees )

@my_view.route('/EmployeeAssignment')
def viewEmployeeAssignment():
    Employee_Assignment = Employee_Assignment.query.join(Employee, Employee_Assignment.Emp_ID == Employee.Emp_ID)\
        .add_columns(Employee_Assignment.Employee_Assignment_ID, Employee_Assignment.Assignment_Start_Date,
         Employee.Emp_ID)

    return render_template('tables/employee_assignment.html')

@my_view.route('/EventCategory')
def viewEventCategory():

    Event_Category .add_columns(Event_Category.Event_Category_ID, Event_Category.Event_Category_Name)
    return render_template('tables/event_category.html')


@my_view.route('/EventOrder')
def viewEventOrder():
    Event_Order = Event_Order.query.join(Event_Category, Event_Order.Event_Category_ID == Event_Category.Event_Category_ID),(Customer, Event_Order.Customer_ID == Customer.Customer_ID),
    (Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID),(State, Event_Order.State_ID == State.State_ID),
    (Employee_Assignment, Event_Order.Employee_Assignment_ID == Employee_Assignment.Employee_Assignment_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_ID, Customer.Customer_ID, Event_Status.Event_Status_ID, Event_Order.Event_Time,
         Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Delivery, Event_Order.Event_Location_Name, Event_Order.Event_Restriction_Desc, 
         Event_Order.Event_Address, Event_Order.Event_City, State.State_ID, Event_Order.Event_Zip_Code, Employee_Assignment.Employee_Assignment_ID, Event_Order.Feedback)
    return render_template('tables/event.html')
  
@my_view.route('/EventOrderLine')
def vEventOrderLine():
    return render_template('tables/event_order_line.html')

@my_view.route('/EventStatus')
def viewEventStatus():
    return render_template('tables/event_status.html')

@my_view.route('/Payment')
def viewPayment():
    return render_template('tables/payment.html')

@my_view.route('/PaymentType')
def viewPaymentType():
    return render_template('tables/payment_type.html', payment = Payment.query.all())


@my_view.route('/ProductService')
def viewProductService():
    return render_template('tables/product_service.html')


@my_view.route('/State')
def viewState():
    return render_template('tables/state.html')

@my_view.route('/Vendor', methods = ["GET" ,"POST"])
def viewVendor():

    if request.method == 'POST':
        #Form request to add customer
        #Checks which form to add from
            vendor = Vendor(request.form['vendorName'], request.form['vendorService'], request.form['vendorDesc'])
                       
            db.session.add(vendor)
            db.session.commit()

    vendorlist = Vendor.query.join(Vendor_Service,Vendor_Service.Vendor_Service_ID == Vendor.Vendor_Service_ID)\
        .add_columns(Vendor.Vendor_Name, Vendor.Vendor_Desc, Vendor.First_Name, Vendor.Last_Name, Vendor.Phone, Vendor.Email,
         Vendor_Service.Vendor_Services, Vendor_Service.Vendor_Service_ID)

    return render_template('tables/vendor.html', vendors = vendorlist, vendorServices = Vendor_Service.query.all())


@my_view.route('/VendorService')
def viewVendorService():
    return render_template('tables/vendor_service.html')

@my_view.route('/createDB')
def createdb():
    return render_template('/', db.create_all())