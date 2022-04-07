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
                        request.form['email'], request.form['address'], request.form['city'], request.form['zip'], request.form['state'])
            db.session.add(customer)
            db.session.commit()
            flash('Success! Customer Added')
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
            flash('Success! Appointment Added.')
        #Form request to add event
        elif request.form['check'] == 'event':
            event = Event_Order(request.form['category'], request.form['customer'], request.form['status'], request.form['eventTime'], request.form['theme'], request.form['eventDesc'],
                        request.form['delivery'], request.form['setup'], request.form['location'], request.form['restrictions'], request.form['address'], request.form['city'],
                        request.form['zip'] , request.form['state'], 'Due after event')
            db.session.add(event)
            db.session.commit()
            flash('Success! Event Added.')
    
    
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
    eventList = Event_Order.query.join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Event_Order.Event_Order_ID, Customer.First_Name, Customer.Last_Name)

    if request.method == 'POST':
        #date update
        if request.form['check'] == 'dateUpdate':
            appointmentFound = request.form['appointment']
            appointment = Appointment.query.get(appointmentFound)
            appointment.date = request.form['date']
            db.session.commit()
            flash('Success! Appointment updated.')
        
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
            flash('Success! Appointment Added.')
        
        # Add Event to appointment
        elif request.form['check'] == 'updateAppointment':
            appointmentFound = request.form['apptID'] 
            appointment = Appointment.query.get(appointmentFound)
            updateDate = request.form['updateDate']
            updateTime = request.form['updateTime']
            updatedDateTime = updateDate + ' ' + updateTime
            updateDateObj = datetime.strptime(updatedDateTime, '%Y-%m-%d %H:%M')
            appointment.Datetime = updateDateObj
            appointment.Event_Order_ID = request.form['event']
            db.session.commit()
            flash('Success! Appointment updated.')

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
                flash('Success! Appointment deleted.')

        
        




    return render_template('tables/appointment.html', appointments = appointmentList, customers = Customer.query.all(), events = eventList)

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
            flash('Success! Customer added')
        
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
            flash('Success! Customer updated.')
        
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
            flash('Success! Employee added')

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
            flash('Success! Employee updated.')
        
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
                flash('Success! Employee deleted.')



        return redirect(url_for('my_view.viewEmployee'))
    
 
    return render_template('tables/employee.html', employees = Employees, stateList = State.query.all() )

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
                
        # Event Form Handling
        if request.form['check'] == 'event':
            event = Event_Order(request.form['category'], request.form['customer'], request.form['status'], request.form['eventTime'], request.form['theme'], request.form['eventDesc'],
                        request.form['delivery'], request.form['setup'], request.form['location'], request.form['restrictions'], request.form['address'], request.form['city'],
                        request.form['zip'], request.form['state'], 'Due after event')
            db.session.add(event)
            db.session.commit()
            flash('Success! Event added.')
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

    foundEventID = eventID
    
    eventOrder = Event_Order.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Category, Event_Category.Event_Category_ID == Event_Order.Event_Category_ID)\
        .join(Customer, Customer.Customer_ID == Event_Order.Customer_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order.Event_Order_Status_ID)\
        .join(State, State.State_ID == Event_Order.State_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Category.Event_Category_Name, Event_Order.Event_Category_ID, Customer.First_Name, Customer.Last_Name, Customer.Phone, Customer.Email, Event_Order.Event_Order_Status_ID, Event_Status.Event_Status, Event_Order.Event_Time, 
        Event_Order.Event_Theme, Event_Order.Event_Order_Desc, Event_Order.Event_Delivery, Event_Order.Event_Setup, Event_Order.Event_Restriction_Desc, Event_Order.Event_Location_Name, Event_Order.Event_Address, Event_Order.Event_City,
        State.State_Abbreviation, Event_Order.Event_Zip_Code)
    
    orderLines = Event_Order_Line.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Order, Event_Order.Event_Order_ID == Event_Order_Line.Event_Order_ID)\
        .join(Product_Service, Product_Service.Product_Service_ID == Event_Order_Line.Product_Service_ID)\
        .join(Event_Status, Event_Status.Event_Status_ID == Event_Order_Line.Event_Order_Status_ID)\
        .add_columns(Event_Order_Line.Event_Order_Line_ID, Event_Order_Line.Event_Order_Status_ID, Event_Order_Line.Event_Order_Line_Date, Event_Status.Event_Status, Product_Service.Product_Service)\
        .order_by(Event_Order_Line.Event_Order_Line_Date)
    
    vendorServiceList = Vendor_Service.query.filter_by(Event_Order_ID = eventID)\
        .join(Vendor, Vendor_Service.Vendor_ID == Vendor.Vendor_ID)\
        .join(Event_Status, Vendor_Service.Vendor_Service_Status_ID == Event_Status.Event_Status_ID)\
        .join(Event_Order, Vendor_Service.Event_Order_ID == Event_Order.Event_Order_ID)\
        .add_columns(Vendor_Service.Vendor_Service_ID, Vendor_Service.Vendor_Services, Vendor.Vendor_ID, Vendor.Vendor_Name,
        Vendor_Service.Date, Event_Order.Event_Order_ID, Vendor_Service.Vendor_Service_Status_ID, Event_Status.Event_Status_ID, Event_Status.Event_Status)
    
    empAssignmentList = Employee_Assignment.query.filter_by(Event_Order_ID = eventID)\
        .join(Employee, Employee_Assignment.Employee_ID == Employee.Emp_ID)\
        .add_columns(Employee_Assignment.Employee_Assignment_ID, Employee.Emp_First_Name, Employee.Emp_Last_Name, Employee_Assignment.Assignment_Start_Date)
        



    if request.method == 'POST':
        if request.form['check'] == 'orderLine':
                orderLine = Event_Order_Line(request.form['status'], request.form['date'], eventID, request.form['service'])                       
                db.session.add(orderLine)
                db.session.commit()
                flash('Success! Order Line added.')
        
        if request.form['check'] == 'addVendorService':
            vendorService = Vendor_Service(request.form['service'], request.form['vendor'], request.form['event'], request.form['status'], request.form['date'])
            db.session.add(vendorService)
            db.session.commit()
            flash('Sucess! Vendor Service added.')


        if request.form['check'] == 'updateEvent':

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
            flash('Success! Event updated.')
        
        if request.form['check'] == 'addEmployeeAssign':
            employee = Employee_Assignment(date.today(), request.form['employeeID'], foundEventID)
            db.session.add(employee)
            db.session.commit()
        
        if request.form['check'] == 'updateOrderLine':
            orderLineID = request.form['orderLineID']
            orderLineFoundforUpdate = Event_Order_Line.query.get(orderLineID)
            currStatus = request.form['currStatus']
            updateStatus = request.form['statusUpdate']
            dateFound = request.form['date']
            print(f'********** {dateFound} ***********{currStatus} ****{updateStatus}')
            if updateStatus == '0':
                orderLineFoundforUpdate.Event_Order_Status_ID = currStatus
                orderLineFoundforUpdate.Event_Order_Line_Date = dateFound
                db.session.commit()
                flash('Success! Order Line updated.')
            else:
                orderLineFoundforUpdate.Event_Order_Status_ID = updateStatus
                orderLineFoundforUpdate.Event_Order_Line_Date = dateFound
                db.session.commit()
                flash('Success! Order Line updated.')
            
            return redirect(url_for('my_view.viewEvent', eventID = foundEventID))
        
        if request.form['check'] == 'updateVendorService':
            vendorServiceID = request.form['venServiceID']
            vendorServiceforUpdate = Vendor_Service.query.get(vendorServiceID)
            currStatus = request.form['currStatus']
            updateStatus = request.form['statusUpdate']
            dateFound = request.form['date']
            if updateStatus == '0':
                vendorServiceforUpdate.Vendor_Service_Status_ID = currStatus
                vendorServiceforUpdate.Vendor_Service_Line_Date = dateFound
                db.session.commit()
                flash('Success! Vendor Service updated.')
            else:
                vendorServiceforUpdate.Vendor_Service_Status_ID = updateStatus
                vendorServiceforUpdate.Vendor_Service_Line_Date = dateFound
                db.session.commit()
                flash('Success! Vendor Service updated.')
            
            return redirect(url_for('my_view.viewEvent', eventID = foundEventID))
           

        
        if request.form['check'] == 'delEventCheck':
            delEventID = request.form['delEventID']
            eventToBeDeleted = Event_Order.query.get(delEventID)
            try:
                db.session.delete(eventToBeDeleted)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewEventOrder'))
            else:
                db.session.commit()
                flash('Delete Succesful')
                return redirect(url_for('my_view.viewEventOrder'))

        
        if request.form['check'] == 'delOrderLineCheck':
            delOrderLineID = request.form['delOrderLineID']
            orderLineTobeDeleted = Event_Order_Line.query.get(delOrderLineID)
            try:
                db.session.delete(orderLineTobeDeleted)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewEventOrder'))
            else:
                flash('Success! Order line deleted')
                db.session.commit()
                return redirect(url_for('my_view.viewEvent', eventID = foundEventID))
        
        if request.form['check'] == 'delVendorService':
            delVendorService = request.form['delVenServiceID']
            vendorServiceFound = Vendor_Service.query.get(delVendorService)
            try:
                db.session.delete(vendorServiceFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewEvent', eventID = foundEventID))
            else:
                flash('Success! Service deleted.')
                db.session.commit()
                return redirect(url_for('my_view.viewEvent', eventID = foundEventID))
        
        if request.form['check'] == 'delEmployeeAssign':
            delEmployeeID = request.form['delEmployeeID']
            employeeRemoved = Employee_Assignment.query.get(delEmployeeID)
            try:
                db.session.delete(employeeRemoved)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
                flash('Delete is not possible for this record')
                return redirect(url_for('my_view.viewEvent', eventID = foundEventID))
            else:
                flash('Success! Employee removed.')
                db.session.commit()
                return redirect(url_for('my_view.viewEvent', eventID = foundEventID))


            


    return render_template('tables/viewEvent.html', employeeAssignments = empAssignmentList, vendorServices = vendorServiceList, categories = Event_Category.query.all(), events = eventOrder, orderLines = orderLines, vendors = Vendor.query.all(), statuses = Event_Status.query.all(), services = Product_Service.query.all(), employees = Employee.query.all())


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
#UPDATE HANDLERS

        if request.form['check'] == 'updateCatCheck':
            categoryID = request.form['catID']
            category = Event_Category.query.get(categoryID)
            category.Event_Category_Name = request.form['category']
            db.session.commit()
            flash('Success! Category updated.')
            
        
        if request.form['check'] == 'statCheck':
            statusID = request.form['statID']
            status = Event_Status.query.get(statusID)
            status.Event_Status = request.form['status']
            db.session.commit()
            flash('Success! Status updated')
        
        if request.form['check'] == 'productCheck':
            productServiceID = request.form['productID']
            productService = Product_Service.query.get(productServiceID)
            productService.Product_Service = request.form['productService']
            db.session.commit()
            flash('Success! Product Service updated.')
        
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
            flash('Success! Payment Type updated.')

# ADDING/CREATION HANDLERS

        if request.form['check'] == 'catCheck':
            category = Event_Category(request.form['category'])
            db.session.add(category)
            db.session.commit()
            flash('Success! Category added.')
        # Service Form Handling
        
        if request.form['check'] == 'serviceCheck':
            service = Product_Service(request.form['service'])
            db.session.add(service)
            db.session.commit() 
            flash('Success! Product Service added.')
        
        if request.form['check'] == 'statusCheck':
            status = Event_Status(request.form['status'])
            db.session.add(status)
            db.session.commit()
            flash('Success! Status added.')
        
        if request.form['check'] == 'vServiceCheck':
            vService = Vendor_Service(request.form['service'])
            db.session.add(vService)
            db.session.commit()

            
        if request.form['check'] == 'payTypeCheck':
            payType = Payment_Type(request.form['payType'])
            db.session.add(payType)
            db.session.commit()
            flash('Success! Payment Type added.')

#DELETE HANDLERS

        if request.form['check'] == 'delVenService':
            delVenID = request.form['delVenServiceID']
            venFound = Vendor_Service.query.get(delVenID)
            try: 
                db.session.delete(venFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewMisc'))
            else:
                db.session.commit()
                flash('Delete Succesful')
                return redirect(url_for('my_view.viewMisc'))
            
        if request.form['check'] == 'delCategory':
            delCatID = request.form['delCategoryID']
            catFound = Event_Category.query.get(delCatID)
            try:
                db.session.delete(catFound)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()  
                flash('Delete is not possible for this record')
                return redirect(url_for('my_view.viewMisc'))
            else:
                flash('Delete Succesful')
                db.session.commit()
        
        if request.form['check'] == 'delStatus':
            delStatusID = request.form['delStatusID']
            statusFound = Event_Status.query.get(delStatusID)
            try:
                db.session.delete(statusFound)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()  
                flash('Delete is not possible for this record')
                return redirect(url_for('my_view.viewMisc'))
            else:
                flash('Delete Succesful')
                db.session.commit()
        
        if request.form['check'] == 'delProService':
            delProServiceID = request.form['delProServiceID']
            ProServiceFound = Product_Service.query.get(delProServiceID)
            try:
                db.session.delete(ProServiceFound)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()  
                flash('Delete is not possible for this record')
                return redirect(url_for('my_view.viewMisc'))
            else:
                flash('Delete Succesful')
                db.session.commit()
        
        if request.form['check'] == 'delPayType':
            delPayTypeID = request.form['delPayTypeID']
            payTypeFound = Payment_Type.query.get(delPayTypeID)
            try:
                db.session.delete(payTypeFound)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()  
                flash('Delete is not possible for this record')
                return redirect(url_for('my_view.viewMisc'))
            else:
                flash('Delete Succesful')
                db.session.commit()
    
    return render_template( 'tables/misc.html', categories = Event_Category.query.all(), statuses = Event_Status.query.all(), productServices = Product_Service.query.all(), 
                            vendorServices = Vendor_Service.query.all(), payments = Payment_Type.query.all())




# PAYMENT - View/Create/Update

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
            flash('Success! Payment added.')
        
        elif request.form['check'] == 'updatePayment':
            paymentID = request.form['paymentID']
            paymentFound = Payment.query.get(paymentID)
            paymentFound.Payment_Type_ID = request.form['payType']
            paymentFound.Event_Order_ID = request.form['eventOrder']
            paymentFound.Payment_Date_Init = request.form['initDate']
            paymentFound.Payment_Date_Full = request.form['fullDate']
            db.session.commit()
            flash('Success! Payment updated.')
        
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
                flash('Success! Payment deleted.')
        
            return redirect(url_for('my_view.viewPayment'))
      
    return render_template('tables/payment.html', payments = payment, types = Payment_Type.query.all(), events = eventWithCustomer)

# Payment type functions will be included in PAYMENT 


# CREATE product services in misc page


# VENDOR Create/View 
@my_view.route('/Vendor', methods = ["GET" ,"POST"])
def viewVendor():
   
  
    vendorlist = Vendor.query.all()

        #Form request to add customer
    if request.method == 'POST':
        #Checks which form to add from
        if request.form['check'] == 'addVendor':
            vendor = Vendor(request.form['vendorName'], request.form['vendorDesc'],request.form['firstName'],
                request.form['lastName'],request.form['phone'],request.form['email'])
            db.session.add(vendor)
            db.session.commit()
            flash('Success! Vendor added.')
            return redirect(url_for('my_view.viewVendor'))


        elif request.form['check'] == 'updateVendor':
            vendorID = request.form['vendorID']
            vendorFound = Vendor.query.get(vendorID)
            vendorFound.Vendor_Name = request.form['vendorName']
            vendorFound.Vendor_Desc = request.form['vendorDesc']
            vendorFound.First_Name = request.form['firstName']
            vendorFound.Last_Name = request.form['lastName']
            vendorFound.Phone = request.form['phone']
            vendorFound.Email = request.form['email']
            db.session.commit()
            flash('Success! Vendor updated')
        
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
                flash('Success! Vendor deleted.')
        
    return render_template('tables/vendor.html', vendors = vendorlist)


@my_view.route('/vendorService/<vendorID>', methods=['GET', 'POST'])
def viewVendorService(vendorID):

    foundVendorID = vendorID

    vendorServiceList = Vendor_Service.query.filter_by(Vendor_ID = vendorID)\
        .join(Vendor, Vendor_Service.Vendor_ID == Vendor.Vendor_ID)\
        .join(Event_Status, Vendor_Service.Vendor_Service_Status_ID == Event_Status.Event_Status_ID)\
        .join(Event_Order, Vendor_Service.Event_Order_ID == Event_Order.Event_Order_ID)\
        .add_columns(Vendor_Service.Vendor_Service_ID, Vendor_Service.Vendor_Services, Vendor.Vendor_ID, Vendor.Vendor_Name,
        Vendor_Service.Date, Event_Order.Event_Order_ID, Vendor_Service.Vendor_Service_Status_ID, Event_Status.Event_Status_ID, Event_Status.Event_Status)

    vendorName = Vendor.query.filter_by(Vendor_ID = vendorID)\
        .add_columns(Vendor.Vendor_ID, Vendor.Vendor_Name)

    eventJoin = Event_Order.query\
        .join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Event_Order.Event_Order_ID, Customer.Customer_ID, Customer.First_Name, Customer.Last_Name)

    if request.method == 'POST':
        # Add
        if request.form['check'] == 'addVendorService':
            vendorService = Vendor_Service(request.form['service'], request.form['vendor'], request.form['event'], request.form['status'], request.form['date'])
            db.session.add(vendorService)
            db.session.commit()
            flash('Success! Vendor Service added.')
        # Update
        if request.form['check'] == 'updateVendorService':
            
            vendorServiceID = request.form['venServiceID']
            vendorServiceforUpdate = Vendor_Service.query.get(vendorServiceID)
            vendorServiceforUpdate.Vendor_Service_Status_ID = request.form['statusUpdate']
            vendorServiceforUpdate.Date = request.form['date']
            db.session.commit()
            flash('Success! Vendor Service updated.')
            
            return redirect(url_for('my_view.viewVendorService', vendorID = foundVendorID)) 
            #Delete
        if request.form['check'] == 'delVendorService':
            delVendorService = request.form['delVenServiceID']
            vendorServiceFound = Vendor_Service.query.get(delVendorService)
            try:
                db.session.delete(vendorServiceFound)
                db.session.flush()
            except exc.IntegrityError:
                    db.session.rollback()  
                    flash('Delete is not possible for this record')
                    return redirect(url_for('my_view.viewVendorService', vendorID = foundVendorID))
            else:
                db.session.commit()  
                flash('Success! Vendor Service deleted.') 
    

        
    return render_template('tables/vendorService.html', vendorName = vendorName, vendors = Vendor.query.all(), vendorServices = vendorServiceList, statuses = Event_Status.query.all(), events = eventJoin)

@my_view.route('/Reports', methods = ['GET', 'POST'])
def viewReports():

    events = Event_Order.query\
        .join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .add_columns(Event_Order.Event_Order_ID, Customer.First_Name, Customer.Last_Name)
    
    
    
    if request.method == 'POST':
        if request.form['check'] == 'event':
            eventSelected = request.form['event']
            return redirect(url_for('my_view.eventReport', eventID = eventSelected))
        
        if request.form['check'] == 'vendor':
            vendorSelected = request.form['vendorSelected']
            return redirect(url_for('my_view.viewVendorService', vendorID = vendorSelected))
        
        if request.form['check'] == 'employeeCheck':
            employeeSelected = request.form['employee']
            return redirect(url_for('my_view.viewEmployeeAssignment', employeeID = employeeSelected))



    return render_template('tables/reports.html', events = events, vendors = Vendor.query.all(), employees = Employee.query.all())

@my_view.route('/eventReport/<eventID>')
def eventReport(eventID):
    event = Event_Order.query.filter_by(Event_Order_ID = eventID)\
        .join(Customer, Event_Order.Customer_ID == Customer.Customer_ID)\
        .join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .join(Event_Category, Event_Order.Event_Category_ID == Event_Category.Event_Category_ID)\
        .join(State, Event_Order.State_ID == State.State_ID)\
        .add_columns(Event_Order.Event_Order_ID, Event_Order.Event_Address, Event_Order.Event_City,
        Event_Order.Event_Delivery, Event_Order.Event_Location_Name, Event_Order.Event_Order_Desc,
        Event_Order.Event_Restriction_Desc, Event_Order.Event_Setup, Event_Order.Event_Theme, Event_Order.Event_Time,
        Customer.First_Name, Customer.Last_Name, Customer.Phone, Event_Status.Event_Status, Event_Category.Event_Category_Name, State.State_Abbreviation)

    orderLines = Event_Order_Line.query.filter_by(Event_Order_ID = eventID)\
        .join(Product_Service, Event_Order_Line.Product_Service_ID == Product_Service.Product_Service_ID)\
        .join(Event_Status, Event_Order_Line.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Product_Service.Product_Service, Event_Status.Event_Status, Event_Order_Line.Event_Order_Line_Date)
    
    vendorServices = Vendor_Service.query.filter_by(Event_Order_ID = eventID)\
        .join(Event_Status, Vendor_Service.Vendor_Service_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Vendor_Service.Vendor_Services, Vendor_Service.Date, Event_Status.Event_Status)

    return render_template('reports/eventReport.html', events = event, orderLines = orderLines, vendorServices = vendorServices,)

@my_view.route('/appointmentReport')
def appointmentReport():

    AppointmentList = Appointment.query.join(Customer, Appointment.Customer_ID == Customer.Customer_ID)\
        .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Appointment.Datetime)\
            .order_by(Appointment.Datetime)\
            .filter(Appointment.Datetime >= date.today(), Appointment.Datetime <= (date.today() + timedelta(days=30)))
    
    return render_template('reports/appointmentReport.html', appointments = AppointmentList)

@my_view.route('/eventListReport')
def eventListReport():
    CustomerList = Customer.query.join(Event_Order, Customer.Customer_ID == Event_Order.Customer_ID)\
    .join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
    .add_columns(Customer.First_Name, Customer.Last_Name, Customer.Email, Customer.Phone, Event_Order.Event_Order_ID, Event_Status.Event_Status, Event_Order.Event_Time, Customer.Customer_ID)\
    .order_by(Event_Order.Event_Time)\
    .filter(Event_Order.Event_Time >= date.today(),Event_Order.Event_Time <= (date.today() + timedelta(days=30)))
   
    return render_template('reports/eventListReport.html', customers = CustomerList)

@my_view.route('/employeeAssignments/<employeeID>', methods = ['GET', 'POST'])
def viewEmployeeAssignment(employeeID):

    assignments = Employee_Assignment.query.filter_by(Employee_ID = employeeID)\
        .join(Employee, Employee_Assignment.Employee_ID == Employee.Emp_ID)\
        .join(Event_Order, Employee_Assignment.Event_Order_ID == Event_Order.Event_Order_ID)\
        .join(Event_Status, Event_Order.Event_Order_Status_ID == Event_Status.Event_Status_ID)\
        .add_columns(Employee.Emp_First_Name, Employee.Emp_Last_Name, Employee_Assignment.Event_Order_ID, Event_Order.Event_Time, 
        Event_Order.Event_Order_Status_ID, Event_Status.Event_Status)\
    
    employeeName = Employee.query.get(employeeID)
    

    return render_template('reports/employeeAssignmentReport.html', employees = assignments, names = employeeName)