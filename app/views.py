from sqlite3 import IntegrityError
from urllib.error import HTTPError
from flask import Blueprint, redirect, render_template, request, flash, url_for, redirect
from .models import Appointment, Customer, Employee, Employee_Assignment, Event_Status, Event_Category, Event_Order,\
                    Event_Order_Line, Payment, Payment_Type, Product_Service, State, Vendor, Vendor_Service
from . import db
from datetime import date, timedelta, datetime
from sqlalchemy import exc



my_view = Blueprint('my_view', __name__)





# INDEX PAGE - Quick view for events and appointments - CREATES: Customer, Event, Appointment

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
            timeStr = request.form['time']
            dateFound = request.form['date']
            dateandtime = dateFound + ' ' + timeStr
            dateObject = datetime.strptime(dateandtime, '%Y-%m-%d %H:%M')
            print(f'PRINTING TIME OBJECT STR************{dateandtime} {dateObject}')
            appointment = Appointment(request.form['customerID'], dateandtime)
            db.session.add(appointment)
            db.session.commit()
        #Form request to add event
        elif request.form['check'] == 'event':
            event = Event_Order(request.form['category'], request.form['customer'], request.form['status'], request.form['eventTime'], request.form['theme'], request.form['eventDesc'],
                        request.form['delivery'], request.form['setup'], request.form['location'], request.form['restrictions'], request.form['address'], request.form['city'],
                        request.form['zip'], request.form['employeeAssignment'], request.form['state'], 'Due after event')
            db.session.add(event)
            db.session.commit()
    
    
    #Query to find customer names with associated events    
    CustomerList = Customer.query.join(Event_Order, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Event_Order.Event_Order_ID, Event_Status.Event_Status, Event_Order.Event_Time, Customer.Customer_ID)\
        .order_by(Event_Order.Event_Time)\
        .filter(Event_Order.Event_Time >= date.today(),Event_Order.Event_Time <= (date.today() + timedelta(days=30)))
    
    #Query to find customer names with associated appointments
    AppointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Appointment.Datetime)\
            .order_by(Appointment.Datetime)\
            .filter(Appointment.Datetime >= date.today(), Appointment.Datetime <= (date.today() + timedelta(days=30)))
    
    return render_template('index.html', employees = Employee.query.all(), customers = CustomerList, stateList = State.query.all(), newAppointment = Customer.query.all(), appointments = AppointmentList, eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all())

# APPOINTMENTS Create/View/Update

@my_view.route('/Appointments', methods=['GET', 'POST'])
def viewAppointment():
    
    appointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Appointment.Appointment_ID, Customer.Customer_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, 
                        Customer.Email, Appointment.Datetime, Appointment.Event_Order_ID)\
        .order_by(Appointment.Datetime)

    if request.method == 'POST':
        #date update
        if request.form['check'] == 'dateUpdate':
            appointmentFound = request.form['appointment']
            appointment = Appointment.query.get(appointmentFound)
            appointment.date = request.form['date']
            db.session.commit()
        
        # new appointment
        elif request.form['check'] == 'newAppointment':
           # dateObject = datetime.strptime(request.form['date'], '%Y-%m-%d')
            timeStr = request.form['time']
            date = request.form['date']
            dateandtime = date + ' ' + timeStr
            dateObject = datetime.strptime(dateandtime, '%Y-%m-%d %H:%M')
            print(f'PRINTING TIME OBJECT STR************{dateandtime} {dateObject}')
            appointment = Appointment(request.form['customerID'], dateandtime)
            db.session.add(appointment)
            db.session.commit()
        
        # Add Event to appointment
        elif request.form['check'] == 'addEvent':
            appointmentFound = request.form['apptID'] 
            appointment = Appointment.query.get(appointmentFound)
            appointment.Event_Order_ID = request.form['event']
            db.session.commit()

        # Delete Appoinment
        elif request.form['check'] == 'deleteAppointment':
            delAppointmentID = request.form['delAppointmentID']
            appointmentFound = Appointment.query.get(delAppointmentID)
            try:
                db.session.delete(appointmentFound)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
                flash('Delete is not possible for this record')
                return redirect(url_for('my_view.viewAppointment'))
            else:
                db.session.commit()

        
        




    return render_template('tables/appointment.html', appointments = appointmentList, customers = Customer.query.all(), events = Event_Order.query.all())

# CUSTOMER Create/View/Update

@my_view.route('/Customer', methods = ['GET', 'POST'])
def viewCustomer():

#State abb
    Customers = Customer.query.join(State, Customer.State_ID == State.State_ID)\
        .add_columns(Customer.Customer_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Customer.Mailing_Address, Customer.Mailing_City, 
                     Customer.Mailing_Zip_Code, Customer.State_ID, State.State_Abbreviation)\
                         .order_by(Customer.Last_Name)
    if request.method == 'POST':
    #Form request to add customer
        if request.form['check'] == 'addCustomer':
            customer = Customer(request.form['firstName'], request.form['lastName'], request.form['phone'],
                        request.form['email'], request.form['address'], request.form['city'], request.form['zip'], request.form['state'])
            db.session.add(customer)
            db.session.commit()
        
        if request.form['check'] == 'updateCustomer':
            customerID = request.form['customerID']
            customerFound = Customer.query.get(customerID)
            customerFound.First_Name = request.form['firstName']
            customerFound.Last_Name = request.form['lastName']
            customerFound.Phone = request.form['phone']
            customerFound.Email = request.form['email']
            customerFound.Mailing_Address = request.form['address']
            customerFound.Mailing_City = request.form['city']
            customerFound.Mailing_Zip = request.form['zip']
            customerFound.State_ID = request.form['state']
            db.session.commit()
        
        if request.form['check'] == 'deleteCustomer': 
            delCustomerID = request.form['deleteCustomerID']
            customerFound = Customer.query.get(delCustomerID)
            try:
                db.session.delete(customerFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Error: Cannot delete customer with an associated event')
                    return redirect(url_for('my_view.viewCustomer'))
            else:
                db.session.commit()          
    return render_template('tables/customer.html', customers = Customers, stateList = State.query.all() )

# EMPLOYEES - Create/View/Update

@my_view.route('/Employee', methods = ['GET', 'POST'])
def viewEmployee():
    Employees = Employee.query.join(State, Employee.State_ID == State.State_ID)\
        .add_columns(Employee.Emp_ID, Employee.Emp_First_Name, Employee.Emp_Last_Name, Employee.Emp_Mailing_Address, Employee.Emp_Mailing_City, 
                     State.State_Abbreviation, Employee.State_ID, State.State_Name, Employee.Emp_Zip_Code, Employee.Emp_Phone, Employee.Emp_Email, Employee.Emp_Position)

    if request.method == 'POST':
        if request.form['check'] == 'addEmployee':
            employee = Employee(request.form['firstName'], request.form['lastName'], request.form['address'], request.form['city'], request.form['state'], request.form['zip'],
                                    request.form['phone'], request.form['email'], request.form['position'])
            db.session.add(employee)
            db.session.commit()

        elif request.form['check'] == 'updateEmployee':
            empID = request.form['employeeID']
            employeeFound = Employee.query.get(empID)
            employeeFound.Emp_First_Name = request.form['firstName']
            employeeFound.Emp_Last_Name = request.form['lastName']
            employeeFound.Emp_Mailing_Address = request.form['address']
            employeeFound.Emp_Mailing_City = request.form['city']
            employeeFound.Emp_State_ID = request.form['state']
            employeeFound.Emp_Zip_Code = request.form['zip']
            employeeFound.Emp_Phone = request.form['phone']
            employeeFound.Emp_Email = request.form['email']
            employeeFound.Emp_Position = request.form['position']
            db.session.commit()
        
        # Delete employee
        elif request.form['check'] == 'deleteEmployee':
            delEmployeeID = request.form['deleteEmployeeID']
            employeeFound = Employee.query.get(delEmployeeID)
            try:
                db.session.delete(employeeFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewEmployee'))
            else:
                db.session.commit()



        return redirect(url_for('my_view.viewEmployee'))
    
 
    return render_template('tables/employee.html', employees = Employees, stateList = State.query.all() )

# Employee assignment - Will be removed later 

@my_view.route('/EmployeeAssignment')
def viewEmployeeAssignment():
    Employee_Assignment = Employee_Assignment.query.join(Employee, Employee_Assignment.Emp_ID == Employee.Emp_ID)\
        .add_columns(Employee_Assignment.Employee_Assignment_ID, Employee_Assignment.Assignment_Start_Date,
         Employee.Emp_ID)

    return render_template('tables/employee_assignment.html')


# EVENT ORDER - Create/View/Update

@my_view.route('/EventOrders', methods = ['GET', 'POST'])
def viewEventOrder():

    eventOrder = Event_Order.query\
        .join(Event_Category, Event_Category.Event_Category_ID == Event_Order.Event_Category_ID)\
        .join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order.Event_Order_Status_ID)\
        .join(State, State.State_ID == Event_Order.State_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_Name, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Event_Status.Event_Status, Event_Order.Event_Time, Event_Order.Event_Theme,
        Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Location_Name, Event_Order.Event_Restriction_Desc, Event_Order.Event_Address, Event_Order.Event_City,
        State.State_Abbreviation, Event_Order.Event_Zip_Code).order_by(Event_Order.Event_Time)

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
                        request.form['zip'], None , request.form['state'], 'Due after event')
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('my_view.viewEventOrder'))
        # Delete event
        elif request.form['check'] == 'deleteEventOrder':
            delEventID = request.form['deleteEventOrderID']
            eventFound = Event_Order.query.get(delEventID)
            try:
                db.session.delete(eventFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewEventOrder'))
            else:
                db.session.commit()
    

    return render_template('tables/events.html', events = eventOrder, eventCategory = Event_Category.query.all(), statuses = Event_Status.query.all(), customers = Customer.query.all(), employees = Employee.query.all(), stateList = State.query.all() )

# SINGLE EVENT DETAIL W/ ORDER LINES - View - NEEDS UPDATE FUNCTIONALITY

@my_view.route('/viewEvent/<eventID>', methods=['GET', 'POST'])
def viewEvent(eventID):
    
    eventOrder = Event_Order.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Category, Event_Category.Event_Category_ID == Event_Order.Event_Category_ID)\
        .join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order.Event_Order_Status_ID)\
        .join(State, State.State_ID == Event_Order.State_ID)\
        .join(Employee_Assignment, Employee_Assignment.Employee_Assignment_ID == Event_Order.Employee_Assignment_ID)\
        .join(Employee, Employee_Assignment.Employee_ID == Employee.Emp_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_Name, Event_Order.Event_Category_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Event_Order.Event_Order_Status_ID, Event_Status.Event_Status, Event_Order.Event_Time, 
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Restriction_Desc, Event_Order.Event_Location_Name, Event_Order.Event_Address, Event_Order.Event_City,
        State.State_Abbreviation, Event_Order.Event_Zip_Code, Employee.Emp_First_Name, Employee.Emp_Last_Name)
    
    orderLines = Event_Order_Line.query.filter_by(Event_Order_ID = eventID)\
        .join(Vendor, Vendor.Vendor_ID == Event_Order_Line.Vendor_ID)\
        .join(Event_Order, Event_Order.Event_Order_ID == Event_Order_Line.Event_Order_ID)\
        .join(Product_Service, Product_Service.Product_Service_ID == Event_Order_Line.Product_Service_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order_Line.Event_Order_Status_ID)\
        .add_columns(Event_Order_Line.Vendor_ID, Vendor.Vendor_Name, Event_Order_Line.Event_Order_Line_Date, Event_Status.Event_Status, Product_Service.Product_Service)\
        .order_by(Event_Order_Line.Event_Order_Line_Date)

    if request.method == 'POST':
        if request.form['check'] == 'orderLine':
            orderLine = Event_Order_Line(request.form['vendor'], request.form['status'], request.form['date'], eventID, request.form['service'])                       
            db.session.add(orderLine)
            db.session.commit()

        elif request.form['check'] == 'updateEvent':

            eventFound = Event_Order.query.get(eventID)
            eventFound.Event_Category_ID = request.form['category']
            eventFound.Event_Order_Status_ID = request.form['status']
            eventFound.Event_Time = request.form['eventTime']
            eventFound.Event_Theme = request.form['theme']
            eventFound.Event_Order_Desc = request.form['eventDesc']
            eventFound.Event_Delivery = request.form['delivery']
            eventFound.Event_Setup = request.form['setup']
            eventFound.Event_Location_Name = request.form['location']
            eventFound.Event_Restriction_Desc = request.form['restrictions']
            eventFound.Event_Address = request.form['address']
            eventFound.Event_City = request.form['city']
            eventFound.Event_Zip_Code = request.form['zip']
            db.session.commit()
            


    return render_template('tables/viewEvent.html', categories = Event_Category.query.all(), events = eventOrder, orderLines = orderLines, vendors = Vendor.query.all(), statuses = Event_Status.query.all(), services = Product_Service.query.all(), employees = Employee.query.all())



# EVENT UPDATE FUNCTIONS - Move to event detail route

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
  
 # Temporary - ORDER LINE now viewable in EVENT DETAIL route
 #  
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

# Will be removed and viewed within events page

@my_view.route('/Misc', methods=['GET', 'POST'])
def viewMisc():

    if request.method == 'POST':
        
        if request.form['check'] == 'catCheck':
            categoryID = request.form['catID']
            category = Event_Category.query.get(categoryID)
            category.Event_Category_Name = request.form['category']
            db.session.commit()
        
        if request.form['check'] == 'statCheck':
            statusID = request.form['statID']
            status = Event_Status.query.get(statusID)
            status.Event_Status = request.form['status']
            db.session.commit()
        
        if request.form['check'] == 'productCheck':
            productServiceID = request.form['productID']
            productService = Product_Service.query.get(productServiceID)
            productService.Product_Service = request.form['productService']
            db.session.commit()
        
        if request.form['check'] == 'vendorCheck':
            vendorServiceID = request.form['vendorID']
            vendorService = Vendor_Service.query.get(vendorServiceID)
            vendorService.Vendor_Services = request.form['vendorService']
            db.session.commit()

        if request.form['check'] == 'paymentCheck':
            paymentTypeID = request.form['paymentID']
            paymentType = Payment_Type.query.get(paymentTypeID)
            paymentType.Payment_Type_Name = request.form['paymentType']
            db.session.commit()
    
    return render_template( 'tables/misc.html', categories = Event_Category.query.all(), statuses = Event_Status.query.all(), productServices = Product_Service.query.all(), 
                            vendorServices = Vendor_Service.query.all(), payments = Payment_Type.query.all())




# PAYMENT - View/Create/Update needs delete

@my_view.route('/Payment', methods = ['GET', 'POST'])
def viewPayment():
    payment = Payment.query.join(Payment_Type, Payment.Payment_Type_ID == Payment_Type.Payment_Type_ID)\
        .join(Event_Order, Payment.Event_Order_ID == Event_Order.Event_Order_ID)\
        .join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Payment.Payment_ID, Payment_Type.Payment_Type_ID, Payment_Type.Payment_Type_Name, Customer.First_Name, Customer.Last_Name, Event_Order.Event_Order_ID, Event_Order.Event_Time, Payment.Payment_Date_Init, Payment.Payment_Date_Full)
    
    eventWithCustomer = Event_Order.query.join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .add_columns(Event_Order.Event_Order_ID, Customer.First_Name, Customer.Last_Name)
    if request.method == 'POST':

        if request.form['check'] == 'addPayment':
            addPayment = Payment(request.form['payType'], request.form['eventOrder'], request.form['initDate'], request.form['fullDate'])
            db.session.add(addPayment)
            db.session.commit()
        
        elif request.form['check'] == 'updatePayment':
            paymentID = request.form['paymentID']
            paymentFound = Payment.query.get(paymentID)
            paymentFound.Payment_Type_ID = request.form['payType']
            paymentFound.Event_Order_ID = request.form['eventOrder']
            paymentFound.Payment_Date_Init = request.form['initDate']
            paymentFound.Payment_Date_Full = request.form['fullDate']
            db.session.commit()
        
        # Delete payment
        elif request.form['check'] == 'deletePayment':
            delPaymentID = request.form['deletePaymentID']
            paymentFound = Payment.query.get(delPaymentID)
            try:
                db.session.delete(paymentFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewPayment'))
            else:
                db.session.commit()
        




 
            return redirect(url_for('my_view.viewPayment'))
    
    
    return render_template('tables/payment.html', payments = payment, types = Payment_Type.query.all(), events = eventWithCustomer)

# Payment type functions will be included in PAYMENT 

@my_view.route('/PaymentType')
def viewPaymentType():
    Payment_Type = Payment_Type()\
        .add_columns(Payment_Type.Payment_ID, Payment_Type.Payment_Type_ID)
    return render_template('tables/payment_type.html', payment = Payment.query.all())

# CREATE product services in misc page

@my_view.route('/ProductService')
def viewProductService():
    Product_Service = Product_Service()\
        .add_columns(Product_Service.Product_Service_ID, Product_Service.Product_Service)
    return render_template('tables/product_service.html')

# VENDOR Create/View - NEEDS UPDATE FUNCTIONALITY
@my_view.route('/Vendor', methods = ["GET" ,"POST"])
def viewVendor():
   

    
         
    vendorlist = Vendor.query.join(Vendor_Service,Vendor_Service.Vendor_Service_ID == Vendor.Vendor_Service_ID)\
    .add_columns(Vendor.Vendor_ID, Vendor.Vendor_Name, Vendor.Vendor_Desc, Vendor.First_Name, Vendor.Last_Name, Vendor.Phone, Vendor.Email,
    Vendor_Service.Vendor_Services, Vendor_Service.Vendor_Service_ID)

        #Form request to add customer
    if request.method == 'POST':
        #Checks which form to add from
        if request.form['check'] == 'addVendor':
            vendor = Vendor(request.form['vendorName'], request.form['vendorService'], request.form['vendorDesc'],request.form['firstName'],
                request.form['lastName'],request.form['phone'],request.form['email'])
                       
            db.session.add(vendor)
            db.session.commit()

        elif request.form['check'] == 'updateVendor':
            vendorID = request.form['vendorID']
            vendorFound = Vendor.query.get(vendorID)
            vendorFound.Vendor_Name = request.form['vendorName']
            vendorFound.Vendor_Services = request.form['vendorService']
            vendorFound.Vendor_Desc = request.form['vendorDesc']
            vendorFound.First_Name = request.form['firstName']
            vendorFound.Last_Name = request.form['lastName']
            vendorFound.Phone = request.form['phone']
            vendorFound.Email = request.form['email']
            db.session.commit()
        
        # Delete vendor
        elif request.form['check'] == 'deleteVendor':
            delVendorID = request.form['deleteVendorID']
            vendorFound = Vendor.query.get(delVendorID)
            try:
                db.session.delete(vendorFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewVendor'))
            else:
                db.session.commit()
        
    return render_template('tables/vendor.html', vendors = vendorlist, vendorServices = Vendor_Service.query.all())


@my_view.route('/VendorService')
def viewVendorService():
    Vendor_Service = Vendor_Service()\
        .add_columns(Vendor_Service.Vendor_Service_ID, Vendor_Service.Vendor_Services)
    return render_template('tables/vendor_service.html')

