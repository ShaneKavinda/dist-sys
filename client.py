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
        
        user_data = {}

        #Get the personId if the user has a TFN number
        if (get_TFN):
            #Get the personId as user input
            # Validate if the length of personId = 6 and is an integer
            person_ID = input("Please Enter Your 6 - Digit Person ID: ").strip()
            if len(person_ID) != 6:
                raise Exception("The Entered value should be 6 digit")
            elif not person_ID.isdigit():
                raise Exception ("THe Entered value is not an integer")
            
            #Get email address of the user (for authentication)
            email = input("Enter your email address: ").strip()
            if "@" not in email or "." not in email:
                raise Exception("Invalid email address. Please enter a valid email.")    
            
            user_data ["person_ID"] = person_ID
            user_data ["email"] = email
            user_data ["has_TFN"] = True

            return user_data    

        #The user does not have a TFN number
        else:
            #Prompt user to enter personID
            # Prompt the user to enter net_wage, tax withheld as a key-value pair (use a loop which the user can exit anytime, with a max range of 26)
            person_ID = input("Please Enter Your 6 - Digit Person ID: ").strip()
            if len(person_ID) != 6:
                raise Exception("The Entered value should be 6 digit")
            elif not person_ID.isdigit():
                raise Exception ("THe Entered value is not an integer")
            
               # Initialize lists for net wages and tax withheld
            net_wages = []
            tax_withheld = []

            print("Please Enter your Bi-Weekly Net Wage and the corresponding Tax Withheld.")
            for i in range(26):
                netWage = float(input("Please Enter Your Bi Weekly Net Wage, ENTER -1 to finish entering: "))
                if netWage == -1:
                    break
                elif netWage < 0:
                    print("Net Wage must be more than 0")
                    continue

                taxWithheld = float (input ("Please Enter the corresponding Tax Withheld: "))
                if taxWithheld < 0:
                    print("Tax withheld cannot be less than 0")
                    continue
                elif taxWithheld > netWage:
                    print ("Tax Withheld cannot be more that Net_wage")
                    continue
                
                net_wages.append(netWage)
                tax_withheld.append(taxWithheld)

            #Save User Data
            user_data["person_id"] = person_ID
            user_data["net_wages"] = net_wages
            user_data["tax_withheld"] = tax_withheld
            user_data["has_tfn"] = False

            return user_data

            
    except Exception:
        print("Invalid input, please try again")
        return getUserInput()
        

def main():
    #uri = "PYRO:server1@"+SERVER+":"+str(PORT)
    #server1 = Pyro4.Proxy(uri)

    splashScreen()

    user_data = getUserInput()
    print("USER INFORMATION: ")
    print (user_data)

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
