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
    CustomerList = Customer.query.join(Event_Order, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Event_Status.Event_Status, Event_Order.Event_Time, Customer.Customer_ID)\
        .order_by(Event_Order.Event_Time)
    
    #Query to find customer names with associated appointments
    AppointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Appointment.Date)\
            .order_by(Appointment.Date)
    
    return render_template('index.html', customers = CustomerList, stateList = State.query.all(), newAppointment = Customer.query.all(), appointments = AppointmentList, eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all())

@my_view.route("/", methods=['GET', 'POST'])
def addCustomerModal():

    return(render_template("addCustomerModal.html"))

#View Appointments
@my_view.route('/Appointments', methods=['GET', 'POST'])
def viewAppointment():
    
    appointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Appointment.Appointment_ID, Customer.Customer_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, 
                        Customer.Email, Appointment.Date, Appointment.Event_Order_ID)\
        .order_by(Appointment.Date)

    if request.method == 'POST':
        #date update
        if request.form['check'] == 'dateUpdate':
            appointmentFound = request.form['appointment']
            appointment = Appointment.query.get(appointmentFound)
            appointment.date = request.form['date']
            db.session.commit()
        # new appointment
        elif request.form['check'] == 'newAppointment':
            appointment = Appointment(request.form['customerID'], request.form['date'])
        # Add Event to appointment
        elif request.form['check'] == 'addEvent':
            appointmentFound = request.form['apptID'] 
            appointment = Appointment.query.get(appointmentFound)
            appointment.Event_Order_ID = request.form['event']
            db.session.commit()



    return render_template('tables/appointment.html', appointments = appointmentList, customers = Customer.query.all(), events = Event_Order.query.all())


@my_view.route('/Customer')
def viewCustomer():
#State abb
    Customers = Customer.query.join(State, Customer.State_ID == State.State_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Customer.Mailing_Address, Customer.Mailing_City, 
                     Customer.Mailing_Zip_Code, Customer.Contact_Date, State.State_Abbreviation)

    return render_template('tables/customer.html', customers = Customers )


@my_view.route('/Employee', methods = ['GET', 'POST'])
def viewEmployee():
    Employees = Employee.query.join(State, Employee.State_ID == State.State_ID)\
        .add_columns(Employee.Emp_ID, Employee.Emp_First_Name, Employee.Emp_Last_Name, Employee.Emp_Mailing_Address, Employee.Emp_Mailing_City, 
                     State.State_Abbreviation, Employee.Emp_Zip_Code, Employee.Emp_Phone, Employee.Emp_Email, Employee.Emp_Position)

    if request.method == 'POST':
        employee = Employee(request.form['firstName'], request.form['lastName'], request.form['address'], request.form['city'], request.form['state'], request.form['zip'],
                                request.form['phone'], request.form['email'], request.form['position'])
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('my_view.viewEmployee'))
    
 
    return render_template('tables/employee.html', employees = Employees, stateList = State.query.all() )

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


@my_view.route('/EventOrders', methods = ['GET', 'POST'])
def viewEventOrder():



    eventOrder = Event_Order.query\
        .join(Event_Category, Event_Category.Event_Category_ID == Event_Order.Event_Category_ID)\
        .join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order.Event_Order_Status_ID)\
        .join(State, State.State_ID == Event_Order.State_ID)\
        .join(Employee_Assignment, Employee_Assignment.Employee_Assignment_ID == Event_Order.Employee_Assignment_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_Name, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Event_Status.Event_Status, Event_Order.Event_Time, Event_Order.Event_Theme,
        Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Location_Name, Event_Order.Event_Restriction_Desc, Event_Order.Event_Address, Event_Order.Event_City,
        State.State_Abbreviation, Event_Order.Event_Zip_Code).all()

    if request.method == 'POST':
        #Form request to add Category
        #Checks which form to add from
        if request.form['check'] == 'catCheck':
            category = Event_Category(request.form['category'])
            db.session.add(category)
            db.session.commit()
        # Service Form Handling
        elif request.form['check'] == 'serviceCheck':
            service = Product_Service(request.form['service'])
            db.session.add(service)
            db.session.commit()           
        # Event Form Handling
        elif request.form['check'] == 'event':
            event = Event_Order(request.form['category'], request.form['customer'], request.form['status'], request.form['eventTime'], request.form['theme'], request.form['eventDesc'],
                        request.form['delivery'], request.form['setup'], request.form['location'], request.form['restrictions'], request.form['address'], request.form['city'],
                        request.form['zip'],2, 1, 'Due after event')
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('my_view.viewEventOrder'))
    

    return render_template('tables/events.html', events = eventOrder, eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all(), customers = Customer.query.all(), employees = Employee.query.all())

@my_view.route('/viewEvent/<eventID>', methods=['GET', 'POST'])
def viewEvent(eventID):
    
    eventOrder = Event_Order.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Category, Event_Category.Event_Category_ID == Event_Order.Event_Category_ID)\
        .join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order.Event_Order_Status_ID)\
        .join(State, State.State_ID == Event_Order.State_ID)\
        .join(Employee_Assignment, Employee_Assignment.Employee_Assignment_ID == Event_Order.Employee_Assignment_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_Name, Event_Order.Event_Category_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Event_Status.Event_Status, Event_Order.Event_Time, 
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Restriction_Desc, Event_Order.Event_Location_Name, Event_Order.Event_Address, Event_Order.Event_City,
        State.State_Abbreviation, Event_Order.Event_Zip_Code)
    
    orderLines = Event_Order_Line.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Order, Event_Order.Event_Order_ID == Event_Order_Line.Event_Order_ID)\
        .join(Product_Service, Product_Service.Product_Service_ID == Event_Order_Line.Product_Service_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order_Line.Event_Order_Status_ID)\
        .add_columns(Event_Order_Line.Event_Order_Line_Date, Event_Status.Event_Status, Product_Service.Product_Service)\
        .order_by(Event_Order_Line.Event_Order_Line_Date)
            


    return render_template('tables/viewEvent.html', events = eventOrder, orderLines = orderLines)



# Update an Event record
@my_view.route('/updateevent/<eventID>', methods=['GET', 'POST'])
def updateEvent(eventID):

# Multiple joins statement to provide IDs and descriptions for associated tables
    eventOrder = Event_Order.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Category, Event_Category.Event_Category_ID == Event_Order.Event_Category_ID)\
        .join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order.Event_Order_Status_ID)\
        .join(State, State.State_ID == Event_Order.State_ID)\
        .join(Employee_Assignment, Employee_Assignment.Employee_Assignment_ID == Event_Order.Employee_Assignment_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_Name, Event_Order.Event_Category_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Event_Status.Event_Status, Event_Order.Event_Time, 
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Restriction_Desc, Event_Order.Event_Location_Name, Event_Order.Event_Address, Event_Order.Event_City,
        State.State_Abbreviation, Event_Order.Event_Zip_Code)

    if request.method == 'POST':
        # Fields to be updated (Left side is table field right side is form field)
            event = Event_Order.query.get(eventID)
            event.Event_Category_ID = request.form['category']
            event.Event_Status = request.form['status']
            event.Event_Time = request.form['eventTime']
            event.Event_Theme = request.form['theme']
            event.Event_Order_Desc = request.form['eventDesc']
            event.Event_Delivery = request.form['delivery']
            event.Event_Setup = request.form['setup']
            event.Event_Location_Name = request.form['location']
            event.Event_Restriction_Desc = request.form['restrictions']
            event.Event_Address = request.form['address']
            event.Event_City = request.form['city']
            event.Event_Zip_Code = request.form['zip']
    
            db.session.commit()
            return redirect(url_for('my_view.viewEventOrder'))
           

    return render_template('update/updateEvent.html', eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all(), selected = eventOrder)
  
@my_view.route('/EventOrderLine/<eventID>',  methods=['GET', 'POST'])
def viewEventOrderLine(eventID):

    
    event_order_line = Event_Order_Line.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Status, Event_Order_Line.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .join(Vendor, Event_Order_Line.Vendor_ID == Vendor.Vendor_ID)\
        .join(Event_Order, Event_Order_Line.Event_Order_ID == Event_Order.Event_Order_ID)\
        .join(Product_Service, Event_Order_Line.Product_Service_ID == Product_Service.Product_Service_ID)\
        .add_columns(Event_Order_Line.Event_Order_Line_ID, Event_Order_Line.Event_Order_Status_ID, Event_Status.Event_Status, Event_Order_Line.Event_Order_Line_Date, Vendor.Vendor_ID, 
                            Vendor.Vendor_Name, Event_Order.Event_Order_ID, Event_Order.Event_Time, Event_Order.Customer_ID,Event_Order_Line.Product_Service_ID,Product_Service.Product_Service)\
        
    
    if request.method == 'POST':
        orderLine = Event_Order_Line(request.form['vendor'], request.form['status'], request.form['date'], eventID, request.form['service'])                       
        db.session.add(orderLine)
        db.session.commit()
        
        

    return render_template('tables/eventOrderLine.html', EOL = event_order_line, vendors = Vendor.query.all(), statuses = Event_Status.query.all(), services = Product_Service.query.all())

@my_view.route('/EventStatus')
def viewEventStatus():
    Event_Status = Event_Status()\
        .add_columns(Event_Status.Event_Status_ID, Event_Status.Event_Status)
    return render_template('tables/event_status.html')

@my_view.route('/Payment', methods = ['GET', 'POST'])
def viewPayment():
    payment = Payment.query.join(Payment_Type, Payment.Payment_Type_ID == Payment_Type.Payment_Type_ID)\
        .join(Event_Order, Payment.Event_Order_ID == Event_Order.Event_Order_ID)\
        .join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Payment.Payment_ID, Payment_Type.Payment_Type_ID, Payment_Type.Payment_Type_Name, Customer.First_Name, Customer.Last_Name, Event_Order.Event_Order_ID, Payment.Payment_Date_Init, Payment.Payment_Date_Full)
    
    if request.method == 'POST':
        payment = Payment(request.form['payType'], request.form['eventOrder'], request.form['initDate'], request.form['fullDate'])
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('my_view.viewPayment'))
    
    
    return render_template('tables/payment.html', payments = payment, types = Payment_Type.query.all(), events = Event_Order.query.all())

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