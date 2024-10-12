#import pyodbc 
import Pyro4

#Set SA2 Connection Details
SA2_PORT = 51516
SA2_SERVER = "localhost"

#Set SA1 Serving Details
SA1_PORT = 51515


@Pyro4.expose
class server1(object):
    #Perform Database Lookup
    def __getUserDetails(self, Email, personId=None):
        print("from Server1: SA1 -> SA2 : Performing Database Request")
        #connect to SA2 with RMI
        sa2Uri = "PYRO:PITREDb@"+ SA2_SERVER + ":" + str(SA2_PORT)
        database=Pyro4.Proxy(sa2Uri)      
        
        #request user details
        return database.getUserDetails(personId, Email)
    
    def getUserDetails(self, personId, Email):
        print("from server1: Client -> SA1 : Called userAuthentication")
        userDetails = self.__getUserDetails(personId, Email)
        
        if not userDetails or len(userDetails) == 0:
            print("No user details found.")
            return []

        # Assuming each entry has at least 3 items
        try:
            print('User details:', userDetails[0][0], userDetails[0][1], userDetails[0][2])
        except IndexError:
            print("Error: Missing user details in response.")
            return []

        print("in Server1: SA1 -> Client : Sending data back to client")
        return userDetails

    

#Accept RMI
server1=server1()
daemon=Pyro4.Daemon(port = SA1_PORT)                
uri=daemon.register(server1, "server1")   

print("--------------------")
print(" Server 1: Interface")
print("--------------------")
print()
print("Ready. Object uri =", uri)
daemon.requestLoop()

