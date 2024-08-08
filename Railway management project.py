import mysql.connector as mysql
from prettytable import PrettyTable
import random 


host = "localhost"
user = "root"
password = "GummyBear"

def login() :

# Specify the correct username and password
    correct_username = "admin"
    correct_password = "blackbag"

    print("""==============================================================================
                                LOGIN PAGE
==============================================================================""")

# Taking input from user
    username = input("Enter Username :- ")
    password = input("Enter Password :- ")

# Checking if the input data matches the specified data
    if username == correct_username and password == correct_password :
        print("Login Successful. Welcome ", username + "!")
        return True
    else :
        print()
        print("Login failed. Incorrect username or password.")
        return False
    
# If login is successful then further actions are performed
if login() :
        try :
# Connecttion declaration for database and user
                connection = mysql.connect(
                        host=host,
                        user = user,
                        passwd = password
                )

# Checking for successful connection

                if connection.is_connected() :
                        print("Database connected successfully.")
                        print()
# Main Cursor

# Create a database where all the data is stored
                cursor = connection.cursor()
                cursor.execute("use sample")
                query = """create database if not exists sample"""
                cursor.execute(query)

# Function for menu display to get input(choice) from user
                def Display():
                        print('''====================================================================================================
                                What would you like to do ?
                                        1. Add trains to schedule 
                                        2. See available Trains and their prices
                                        3. Remove a train 
                                        4. Book a ticket
                                        5. Display bill
                                        6. Update Tickets available
                                        7. Worker Menu
                                        8. Exit
====================================================================================================
                        ''')
# Taking choice as input from user
                        choice = int(input("Enter your choice (number) :- "))
                        if choice == 1:
                                AddTrains()
                                Display()
                        elif choice == 2:
                                SeeTrains()
                                Display()
                        elif choice == 3:
                                RemoveTrains()
                                Display()
                        elif choice == 4:
                                book_ticket()
                                Display()
                        elif choice == 5 :
                                display_bill()
                                Display()
                        elif choice == 6 :
                                update_tickets_available()
                                Display()
                        elif choice == 7 :
                                worker_menu()
                                Display()
                        else :    
                                print("Database Disconnected successfully.")
                                connection.close()
                

# Function to add trains 
                def AddTrains():

# Writing a sql query to get the desired result 
                        table_creation_sql = '''
                                CREATE TABLE IF NOT EXISTS TrainSchedule (
                                TrainName VARCHAR(255),
                                TrainNumber INT,
                                FromDestination VARCHAR(255),
                                ToDestination VARCHAR(255),
                                DateOfDeparture DATE,
                                TimeOfDeparture TIME,
                                Tickets_available INT,
                                Cost INT
                                )
                                '''
# Execute the table creation SQL statement
                        cursor.execute(table_creation_sql)

#Making of dictionary to insert data into the table
                        train_data = {
                        'TrainName': input("Trainname : "),
                        'TrainNumber': int(input("Train number : ")),
                        'FromDestination': input("From : "),
                        'ToDestination': input("To : "),
                        'DateOfDeparture': input("Date (yyyy-mm-dd) : "),
                        'TimeOfDeparture': input("Time (hh:mm:ss) : "),
                        'Tickets_available' : input("Enter no of tickets available : "),
                        'Cost': int(input("Cost : "))
                        }

# Inserting data into the table
                        insert_data_trainschedule_query = """
                        INSERT INTO TrainSchedule  
                        (TrainName, TrainNumber, FromDestination, ToDestination, DateOfDeparture, TimeOfDeparture, Tickets_available, Cost)
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                        """
                        data = (
                        train_data['TrainName'],
                        train_data['TrainNumber'],
                        train_data['FromDestination'],
                        train_data['ToDestination'],
                        train_data['DateOfDeparture'],
                        train_data['TimeOfDeparture'],
                        train_data['Tickets_available'],
                        train_data['Cost'])

# Execute the data insertion query
                        cursor.execute(insert_data_trainschedule_query,data)  

# Commit the changes
                        connection.commit()

# Booking a train ticket
                def book_ticket() :
                        ticket_table_query = """
                        CREATE TABLE IF NOT EXISTS ticket (
                                Customer_name VARCHAR(255),
                                TrainNumber INT,
                                FromDestination VARCHAR(255),
                                ToDestination VARCHAR(255),
                                DateofDeparture DATE,
                                Phone_number BIGINT,
                                Cost INT,
                                Bill_number INT
                        )"""
        
# execute the table creation query
                        cursor.execute(ticket_table_query)

# Generating a bill number using random module
                        Bill_no = (random.randint(100,300))

# Making of dictionary to insert data into thr table
                        ticket_data = {
                        'Customer_name': input("Name : "),
                        'TrainNumber': int(input("Train number : ")),
                        'FromDestination': input("From : "),
                        'ToDestination': input("To : "),
                        'DateOfDeparture': input("Date (yyyy-mm-dd) : "),
                        'Phone_number' : int(input("Mobile number : ")) ,
                        'Cost': int(input("Price : ")),
                        'Bill_number' : Bill_no
                        }

# Inserting data into the table 
                        insert_data_ticket_query = """
                        INSERT INTO ticket 
                        (Customer_name, TrainNumber, FromDestination, ToDestination, DateOfDeparture, Phone_number, Cost, Bill_number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                        """ 
                        data = (
                        ticket_data['Customer_name'],
                        ticket_data['TrainNumber'],
                        ticket_data['FromDestination'],
                        ticket_data['ToDestination'],
                        ticket_data['DateOfDeparture'],
                        ticket_data['Phone_number'],
                        ticket_data['Cost'],
                        ticket_data['Bill_number']
                        )

# Execute the data insertion query
                        cursor.execute(insert_data_ticket_query,data)

# Commit the changes
                        connection.commit()

                        print()
# Displaying additional information and bill number
                        print("Ticket booking successful")
                        print("Bill number :",Bill_no)



# Seeing available trains and their prices
                def SeeTrains() :
# Execute a query to fetch data from the table
                        cursor.execute('SELECT * FROM TrainSchedule')
                        column_names = [description[0] for description in cursor.description]

# Create a PrettyTable object with column names
                        table = PrettyTable(column_names)

# Fetch and add rows from the query result
                        rows = cursor.fetchall()
                        for row in rows:
                                table.add_row(row)

# Print the table
                        print(table)

# Displaying bill to user 
                def display_bill() :

#taking bill no from the user
                        Bno = int(input("Enter Bill number : "))
                        print()
                        print("Your Bill is :")
                        print()
    
# Writing a sql query to get the desired result 
                        search_query = f"SELECT * FROM ticket WHERE Bill_number = {Bno} ;"

#execute the search query
                        cursor.execute(search_query)

                        column_names = [description[0] for description in cursor.description]

# Create a PrettyTable object with column names
                        table = PrettyTable(column_names)

# Fetch and add rows from the query result
                        rows = cursor.fetchall()
                        for row in rows:
                                table.add_row(row)

# Print the table
                        print(table)

#Updating Tables
                def update_tickets_available() :
                        SeeTrains()

# get the train name and no of available tickets from user
                        Tno = input("Enter Train Number : ")
                        t_a_no = int(input("Enter number of available tickets : "))

# Writing a sql query to get the desired result 
                        update_query = f"UPDATE TrainSchedule SET Tickets_available ={t_a_no} WHERE TrainNumber = {Tno} ;"

# execute the update query
                        cursor.execute(update_query)

# Commit the changes
                        connection.commit()
                        print("Number of tickets updated successfully.")
                        SeeTrains()

# Removing a row from the table trainschedule
                def RemoveTrains():
        
# Assuming you have a table named 'your_table' and a condition for the row you want to delete
# For example, deleting a row where 'employee_id' is 123
                        SeeTrains()
                        TNo = int(input("Enter TrainNumber: "))

# Writing a sql query to get the desired result 
                        delete_query = f"DELETE FROM TrainSchedule WHERE TrainNumber = {TNo} ;"

# Execute the delete query
                        cursor.execute(delete_query)

# Commit the changes and close the connection
                        connection.commit()

# Creating a worker menu 
                def worker_menu() :
                                print("""============================================================================================
                                WORKER MENU
============================================================================================
                                (a) View Workers
                                (b) Add Worker 
                                (c) Update Worker Information
                                (d) Exit""")

                                choice_w = input("Enter your choice (a-d) :- ")
                                if choice_w == "a" :
                                        display_worker()
                                        worker_menu()
                                elif choice_w == "b" :
                                        add_worker()
                                        worker_menu()
                                elif choice_w == "c" :
                                        update_worker()
                                        worker_menu()
                                elif choice_w == "d" :
                                        print("Worker menu exited successfully.")
                                        Display()
                                else :
                                        print("Invalid choice. Please enter from (a-d).")

# To display worker table
                def display_worker() :

# Execute a query to fetch data from table
                        cursor.execute("SELECT * FROM Worker")
                        worker_column = [description[0] for description in cursor.description]

# Create a PrettyTable object with column names
                        table = PrettyTable(worker_column)

# Fetch and add rows from the query result
                        workers = cursor.fetchall()
                        for worker in workers:
                                table.add_row(worker)

# Print the table
                        print(table)

# To add worker data to table
                def add_worker() :
                        print()

# Writing a query to create worker table
                        worker_table_query = """
                        CREATE TABLE IF NOT EXISTS Worker (
                                WorkerID INT AUTO_INCREMENT PRIMARY KEY,
                                FirstName Varchar(255),
                                LastName VARCHAR(255),
                                Position VARCHAR(255),
                                Salary DECIMAL(10,2),
                                HireDate DATE
                        )"""
# Execute the table creation query
                        cursor.execute(worker_table_query)

# Making a dictionary to insert data into table
                        worker_data = {
                        'WorkerID': int(input("Worker ID : ")),
                        'FirstName': input("First Name : "),
                        'LastName': input("Last Name : "),
                        'Position': input("Position : "),
                        'Salary': int(input("Salary : ")),
                        'HireDate': input("HireDate (yyyy-mm-dd) : ")
                        }
# Inserting data into the table 
                        insert_data_worker_query = """
                        INSERT INTO Worker
                        (WorkerID , FirstName , LastName , Position , Salary , HireDate)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """ 
                        work_data = (
                        worker_data['WorkerID'],
                        worker_data['FirstName'],
                        worker_data['LastName'],
                        worker_data['Position'],
                        worker_data['Salary'],
                        worker_data['HireDate']
                        )
                        print()

# Execute the data insertion query
                        cursor.execute(insert_data_worker_query,work_data)

# Commit the changes
                        connection.commit()

# To update worker data
                def update_worker() :
                        print()
# Get worker id from user to update
                        worker_id = int(input("Enter Worker ID to update : "))
                        new_salary = float(input("Enter new Salary : "))

# Writing a query to update data of specified worker
                        worker_update_query = f"UPDATE Worker SET Salary = {new_salary} WHERE WorkerID = {worker_id}"

# Execute the update query
                        cursor.execute(worker_update_query)
                        print("Worker information updated successfully.")
# Commit the changes
                        connection.commit()


# Displays the menu
                Display()
                connection.close()
    

        except mysql.errors as err :
                print(f"Eroor : {err}")

else :
    print()