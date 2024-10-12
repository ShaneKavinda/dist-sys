#Ryan doc name: ca.py
import Pyro4

#Set SA1 Connection Details
PORT = 51515
SERVER = "localhost"



def splashScreen():
    print("-------------------------------------")
    print("     == PITRE ==         ")
    print("   Personal Income Tax Return Estimate System")
    print("-------------------------------------")
    print("")


def checkStudent():
    while True:
        selection = input("Are you a current EOU Student? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False

def printAuthentication(auth):
    print()
    print("--------your personal details are as below---------------------------")
    print()
    #print(qual)
    print ("  PID   | PID_NO     | Email   ")
    print ("--------+------------+----------")
    i=1
    for x in auth:
        has_pid =x[0]
        pid_no = x[1]
        email = x[2]
        print ( "   ", has_pid, "  |   ", pid_no, "  |  ", email)
        #print (  i,  unit_title,  unit_mark)
        i +=1

def main():
    uri = "PYRO:server1@"+SERVER+":"+str(PORT)
    server1 = Pyro4.Proxy(uri)

    splashScreen()

    personId = "1V"
    Email = "testuser@email.com"
    
    print("Requesting Data from Server....")
    authentication = server1.getUserDetails(personId, Email)
    
    if not authentication:
        print("No user details found.")
        return

    printAuthentication(authentication)

    
    print("")


main()
