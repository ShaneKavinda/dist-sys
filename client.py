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

# Get user input from the user
def getUserInput():
    try:
        TFN_input = input("Please enter if you have a TFN number (y/n/):")
        if (TFN_input == "y" or TFN_input == "Y"):
            get_TFN = True
        elif (TFN_input == "n" or TFN_input == "N"):
            get_TFN = False
        else:
            raise Exception()
        
        #Get the personId if the user has a TFN number
        if (get_TFN):
            #Get the personId as user input
            # Validate if the length of personId = 6 and is an integer

            #Get email address of the user (for authentication)

        #The user does not have a TFN number
        else:
            # Prompt user to enter personID
            # Prompt the user to enter net_wage, tax withheld as a key-value pair (use a loop which the user can exit anytime, with a max range of 26)
            
    except Exception:
        print("Invalid input, please try again")
        getUserInput()
        

def main():
    uri = "PYRO:server1@"+SERVER+":"+str(PORT)
    server1 = Pyro4.Proxy(uri)

    splashScreen()

    getUserInput()
    # personId = "1V"
    # Email = "testuser@email.com"
    
    # print("Requesting Data from Server....")
    # authentication = server1.getUserDetails(personId, Email)
    
    # if not authentication:
    #     print("No user details found.")
    #     return

    # printAuthentication(authentication)

    
    print("")


main()
