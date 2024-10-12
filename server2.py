import pyodbc 
import Pyro4

#Configure SQL Server Details
SQL_SERVER_NAME = "SHANE_K_99\\SQLEXPRESS"
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
        except:
            return None

    #----- Exposed Methods that can be invoked

    def getUserDetails(self, Email, personId):
        try:
            print("in Server2: SA1 -> SA2 : Called getUserDetails")
            user = list()

            print('person ID: '+personId)
            print('email: '+Email)
            print("Attempting to Perform MSSQL Database lookup")
            cursor = self.__sqlQuery('SELECT has_pid, first_name, last_name FROM Users WHERE personId = ? AND email = ?', [personId, Email])
            
            if cursor:
                for i in cursor:
                    user.append([i[0], i[1], i[2]])  # Assuming the correct number of columns

            print("Returning user details: ", user)
            return user
        except Exception as e:
            print(f"Error in Server2: {e}")
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

