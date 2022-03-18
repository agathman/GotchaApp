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
                        request.form['zip'],2, request.form['state'], 'Due after event')
            db.session.add(event)
            db.session.commit()
    
    #Query to find customer names with associated events    
    CustomerList = Customer.query.join(Event_Order, Customer.Customer_ID == Event_Order.Customer_ID).join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Event_Order.Event_Time, Customer.Customer_ID, Event_Status.Event_Status)
    
    #Query to find customer names with associated appointments
    AppointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Appointment.Date)
    
    return render_template('index.html', customers = CustomerList, stateList = State.query.all(), newAppointment = Customer.query.all(), appointments = AppointmentList, eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all())

    

@my_view.route("/", methods=['GET', 'POST'])
def addCustomerModal():

    return(render_template("addCustomerModal.html"))

#View single event info
@my_view.route('/event/<eventID>')
def event(eventID):

    Event = Event_Order.query.join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Event_Order.Event_Time, Event_Order.Event_Order_Status_ID,
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Location_Name,
        Event_Order.Event_Restriction_Desc, Event_Order.Event_Address, Event_Order.Event_City)\
            .filter_by(Customer_ID = eventID)



    return render_template('event.html', event = Event, Events_Status=Event_Status.query.all())

#View all events
@my_view.route('/events')
def viewEvent():
    
    Events = Event_Order.query.join(Customer, Event_Order.Customer_ID == Customer.Customer_ID).join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Event_Order.Event_Time, Event_Status.Event_Status,
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
    Event_Category = Event_Category()\
        .add_columns(Event_Category.Event_Category_ID, Event_Category.Event_Category_Name)
    return render_template('tables/event_category.html')


@my_view.route('/EventOrder')
def viewEventOrder():
    event_order = Event_Order.query.join(Event_Category, Event_Order.Event_Category_ID == Event_Category.Event_Category_ID).join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Event_Category.Event_Category_ID, Event_Category.Event_Category_Name,Event_Order.Event_Time,
         Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Location_Name, Event_Order.Event_Restriction_Desc, 
         Event_Order.Event_Address, Event_Order.Event_City, Event_Order.Event_Zip_Code, Event_Order.Feedback, Customer.Customer_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone)

    return render_template('tables/eventorder.html', EO =event_order, states = State.query.all(), customerlists= Customer.query.all())
  
@my_view.route('/EventOrderLine')
def viewEventOrderLine():
    event_order_line = Event_Order_Line.query.join(Event_Status, Event_Order_Line.Event_Order_Status_ID == Event_Status.Event_Status_ID).join(Vendor,Event_Order_Line.Vendor_ID==Vendor.Vendor_ID).join(Event_Order, Event_Order_Line.Event_Order_ID==Event_Order.Event_Order_ID).join(Product_Service,Event_Order_Line.Product_Service_ID==Product_Service.Product_Service_ID)\
        .add_columns(Event_Order_Line.Event_Order_Line_ID, Event_Order_Line.Event_Order_Status_ID, Event_Status.Event_Status, Event_Order_Line.Event_Order_Line_Date, Vendor.Vendor_ID, Vendor.First_Name, Vendor.Last_Name, Event_Order.Event_Order_ID,Event_Order.Customer_ID,Event_Order_Line.Product_Service_ID,Product_Service.Product_Service)\

    return render_template('tables/event_order_line.html',EOL = event_order_line)

@my_view.route('/EventStatus')
def viewEventStatus():
    Event_Status = Event_Status()\
        .add_columns(Event_Status.Event_Status_ID, Event_Status.Event_Status)
    return render_template('tables/event_status.html')

@my_view.route('/Payment')
def viewPayment():
    Payment = Payment.query.join(Payment_Type, Payment.Payment_Type_ID == Payment_Type.Payment_Type_ID), (Event_Order, Payment.Event_Order_ID == Event_Order.Event_Order_ID)\
        .add_columns(Payment.Payment_ID, Payment_Type.Payment_Type_ID, Event_Order.Event_Order_ID, Payment.Payment_Date_Init, Payment.Payment_Date_Full)
    return render_template('tables/payment.html')

@my_view.route('/PaymentType')
def viewPaymentType():
    Payment_Type = Payment_Type()\
        .add_columns(Payment_Type.Payment_ID, Payment_Type.Payment_Type_ID)
    return render_template('tables/payment_type.html', payment = Payment.query.all())


@my_view.route('/ProductService')
def viewProductService():
    Product_Service = Product_Service()\
        .add_columns(Product_Service.Product_Service_ID, Product_Service.Product_Service)
    return render_template('tables/product_service.html')


@my_view.route('/State')
def viewState():
    State = State()\
        .add_columns(State.State_ID, State.State_Name, State.State_Abbreviation)
    return render_template('tables/state.html')

@my_view.route('/Vendor', methods = ["GET" ,"POST"])
def viewVendor():
    # Vendor = Vendor.query.join(Vendor_Service, Vendor.Vendor_Services_ID == Vendor_Service.Vendor_Services_ID)\
    #     .add_columns(Vendor.Vendor_ID, Vendor.Vendor_Name, Vendor_Service.Vendor_Services_ID, Vendor.Vendor_Desc, 
    #     Vendor.First_Name, Vendor.Last_Name, Vendor.Phone, Vendor.Email )
    #^^^^This view route causes vendor page to not open when running application

    if request.method == 'POST':

        #Form request to add customer
        #Checks which form to add from
            vendor = Vendor(request.form['vendorName'], request.form['vendorService'], request.form['vendorDesc'],request.form['firstName'],
                request.form['lastName'],request.form['phone'],request.form['email'])
                       
            db.session.add(vendor)
            db.session.commit()

    vendorlist = Vendor.query.join(Vendor_Service,Vendor_Service.Vendor_Service_ID == Vendor.Vendor_Service_ID)\
        .add_columns(Vendor.Vendor_Name, Vendor.Vendor_Desc, Vendor.First_Name, Vendor.Last_Name, Vendor.Phone, Vendor.Email,
         Vendor_Service.Vendor_Services, Vendor_Service.Vendor_Service_ID)

    return render_template('tables/vendor.html', vendors = vendorlist, vendorServices = Vendor_Service.query.all())








@my_view.route('/VendorService')
def viewVendorService():
    Vendor_Service = Vendor_Service()\
        .add_columns(Vendor_Service.Vendor_Service_ID, Vendor_Service.Vendor_Services)
    return render_template('tables/vendor_service.html')



@my_view.route('/createDB')
def createdb():
    return render_template('/', db.create_all())