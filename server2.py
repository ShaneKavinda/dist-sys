#server2.py
import pyodbc 
import Pyro4

#Configure SQL Server Details
SQL_SERVER_NAME = "KABI"
SQL_SERVER_DB = "PITR"

#Set Server2 Serving Details
SA2_PORT = 51516


@Pyro4.expose
class db(object):
    #Perform Database Lookup
    def __sqlQuery(self, q, arg):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                'Server='+SQL_SERVER_NAME+';'
                                'Database='+SQL_SERVER_DB+';'
                                'Trusted_Connection=yes;')

            cursor = conn.cursor()
            cursor.execute(q, arg)
            return cursor
        except Exception as e:
            print(f"Database connection or query failed: {e}")
            return None

    #----- Exposed Methods that can be invoked

    def getUserDetails(self, tfn):
        try:
            print("in Server2: SA1 -> SA2 : Called getUserDetails")
            user = list()

            print('Tax File Number: '+tfn)
            #print('email: '+Email)
            print("Attempting to Perform MSSQL Database lookup")
            cursor = self.__sqlQuery('SELECT Person_ID, First_Name, Last_Name, Email, phic FROM Users WHERE TFN = ? ', [tfn])
            
            if cursor:
                for i in cursor:
                    user.append([i[0], i[1], i[2], i[3], i[4]])  # Assuming the correct number of columns

            print("Returning user details: ", user)
            return user
        except Exception as e:
            print(f"Error in Server2: {e}")
            return []
        
    def getUserPayrollData(self, tfn):
        try:
            print("In Server2: SA1 -> SA2 : Called getUserPayrollData") 
            payroll = []  # List of dictionaries to store payroll data
            
            print('Tax File Number: '+tfn)
            
            print("Attempting to Perform MSSQL Database lookup")
            cursor = self.__sqlQuery('SELECT Net_Wage, Tax_Withheld FROM PayrollRecords WHERE TFN = ?', [tfn])
            
            if cursor:
            # Loop through the result set and store each record in a dictionary
                for row in cursor:
                    record = {
                        'net_wage': row[0],  # Net_Wage
                        'tax_withheld': row[1]  # Tax_Withheld
                    }
                    payroll.append(record)  # Add the dictionary to the list
            
                print("Returning payroll data: ", payroll)
                return payroll
                
        except Exception as error:
            print(f"Error in Server2: {error}")
            return []

#Accept RMI
PITREDb=db()
daemon=Pyro4.Daemon(port=SA2_PORT)                
uri=daemon.register(PITREDb, "PITREDb")


print("-----------------------------")
print(" Server2 - Interface ")
print("-----------------------------")
print()
print("Ready. Object uri =", uri)
daemon.requestLoop()

