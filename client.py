#Client.py
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
    print ("  Person ID   | First_Name     | Email   ")
    print ("--------------+----------------+----------")
    i=1
    has_phic = None
    for x in auth:
        has_pid =x[0]
        first_name = x[1]
        email = x[3]
        phic= x[4]
        print ( "   ", has_pid, "  |   ", first_name, "  |  ", email)
        #print (  i,  unit_title,  unit_mark)
        i +=1
        has_phic= phic
    return has_phic

def printTaxCalculation(result):
    print("----------TAX CALCULATIONS----------")
    print(f"Taxable Income: {result["annual_taxable_income"]}")
    print(f"Total Tax Withheld: {result["total_tax_withheld"]}")
    print(f"Total Net Income: {result["total_net_income"]}")
    print(f"Estimated Tax Refund: {result["estimated_tax_refund"]}")
    print(f"Estimated Tax Estimate: {result["tax_estimate"]}")

# Validate the TFN number entered by the user
def validate_TFN(TFN_no):
    if (len(TFN_no) == 8):
        return True
    else:
        return False

def checkDataInput(ID):
    if len(ID) != 6:
        raise Exception("The Entered value should be 6 digit")
    elif not ID.isdigit():
        raise Exception ("THe Entered value is not an integer")


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
            
            tfn = input("Please Enter Your 8 - Digit Tax File Number: ").strip()
            if len(tfn) != 8:
                 raise Exception("The Entered value should be 8 digit")

            user_data["tfn"] = tfn
            user_data["has_tfn"] = True
            return user_data    

        #The user does not have a TFN number
        else:
            #Prompt user to enter personID
            # Prompt the user to enter net_wage, tax withheld as a key-value pair (use a loop which the user can exit anytime, with a max range of 26)
           
            person_ID = input("Please Enter Your 6 - Digit Person ID: ").strip() 
            checkIDerror = checkDataInput(person_ID) # Validate if the length of personId = 6 and is an integer
            
            # Initialize lists for net wages and tax withheld
            net_wages = []
            tax_withheld = []

            print("Please Enter your Bi-Weekly Net Wage and the corresponding Tax Withheld using the format  <net_wage, tax_withheld> .")
            counter = 0
            while (True):
                payroll = input("Enter your payroll data (or '-1' to finish): ").strip()

                if payroll == "-1":
                    break

                try:
                    #Split the payroll input by " , " and change them into map datatype (Tiwari, 2024)
                    netWage, taxWithheld = map(float, payroll.split(","))
                
                    if netWage < 0:
                        print("Net Wage must be more than 0")
                        continue

                    if taxWithheld < 0:
                        print("Tax withheld cannot be less than 0")
                        continue
                    elif taxWithheld > netWage:
                        print ("Tax Withheld cannot be more that Net_wage")
                        continue
                    
                    #Only allow 26 payroll entries
                    counter +=1
                    if counter == 26:
                        print("Payroll can only contain 26 data items!")
                        break

                    net_wages.append(netWage)
                    tax_withheld.append(taxWithheld)
                    
                except ValueError:
                    print("Invalid input format. Please enter the data as '<net_wage>, <tax_withheld>'")
                    continue

            #Ask user whether they have Private Health Insurance Cover (PHIC)
            phic = input("Please state whether you have a Private Health Insurance Cover (PHIC) (y/n/):")
            if (phic == "y" or phic == "Y"):
                hasPHIC = True
            elif (phic == "n" or phic == "N"):
                hasPHIC = False
            else:
                raise Exception()
            
            #Save User Data
            user_data["person_id"] = person_ID
            user_data["net_wages"] = net_wages
            user_data["tax_withheld"] = tax_withheld
            user_data["has_tfn"] = False
            user_data["has_phic"] = hasPHIC
            return user_data

            
    except Exception:
        print("Invalid input, please try again")
        return getUserInput()
        

def main():
    uri = "PYRO:server1@"+SERVER+":"+str(PORT)
    server1 = Pyro4.Proxy(uri)

    splashScreen()

    user_data = getUserInput()
    #print("USER INFORMATION: ")
    #print (user_data)

    # personId = "1V"
    # Email = "testuser@email.com"
    
    # print("Requesting Data from Server....")
    # authentication = server1.getUserDetails(personId, Email)
    
    # if not authentication:
    #     print("No user details found.")
    #     return

    # printAuthentication(authentication)
    
    if user_data["has_tfn"]:
        print("Requesting Data from Server....")
        authentication = server1.getUserDetails(user_data["tfn"])

        if not authentication:
            print("No user details found.")
            return
        
        has_phic= printAuthentication(authentication)

        print("\nRequesting payroll data from the server...")
        payrollData = server1.getUserPayrollData(user_data["tfn"])
        
        if payrollData:
            result = server1.processTaxReturnEstimate(user_data["tfn"], payrollData, has_phic)
            # Display calculation details
            print(f"\nTFN: {user_data["tfn"]}")
            printTaxCalculation(result)
            print("")
        else:
            print("No payroll data found for the given TFN.")
        
    else:
        result = server1.processTaxReturnEstimate(None, user_data, user_data["has_phic"])
        # Display calculation details
        print(f"\nPersonID: {user_data["person_id"]}")
        printTaxCalculation(result)
        print("")
   

main()
