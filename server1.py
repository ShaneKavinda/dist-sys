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
    
    def processTaxReturnEstimate(self, personId, net_wages, tax_withheld, has_phic):
        print(f"Processing tax return estimate for Person ID: {personId}")
        
        # Display the tax-related data (biweekly wages and tax withheld)
    
        print("\nBiweekly wages and tax withheld:")
        for i in range(1, len(net_wages) + 1):
            print(f"Period {i}: <{net_wages[i - 1]}, {tax_withheld[i - 1]}>")

        # Calculate total wages and tax withheld
        net_income=sum(net_wages)
        total_tax_withheld = sum(tax_withheld)

        taxable_income = net_income  #not too sure about where is taxable_income is from

        # Simplified tax return logic
        if taxable_income <= 18200:
            tax_due = 0
        elif taxable_income >=18201 and taxable_income <= 45000:
            tax_due = 0.19 * (taxable_income - 18200)
        elif taxable_income >= 45001 and  taxable_income <= 120000:
            tax_due = 5092 + 0.325 * (taxable_income - 45000)
        else:
            tax_due = 29467 + 0.37 * (taxable_income - 120000)

        # Medicare Levy (ML) at 2% of taxable income
        medicare_levy = taxable_income * 0.02

        if not has_phic and taxable_income > 90000:
            if taxable_income <= 105000:
                mls = taxable_income * 0.01
            elif taxable_income <= 140000:
                mls = taxable_income * 0.0125
            else:
                mls = taxable_income * 0.015
        else:
            mls = 0

        # Total tax payable
        total_tax_payable = tax_due + medicare_levy + mls

        # Calculate tax refund (or additional tax owed)
        tax_refund = total_tax_withheld - total_tax_payable

        #Calculate Tax estimate
        tax_estimate = taxable_income - net_income - tax_due - medicare_levy - mls 

         # Display calculation details
        print(f"\nTaxable Income: {taxable_income}")
        print(f"Tax Calculated: {tax_due}")
        print(f"Medicare Levy: {medicare_levy}")
        print(f"Medicare Levy Surcharge (MLS): {mls}")
        print(f"Total Tax Payable: {total_tax_payable}")
        print(f"Estimated Tax Refund: {tax_refund}")
        print(f"Estimated Tax Estimate: {tax_estimate}")
        
        # Send the results back to the client
        result = {
            "person_id": personId,
            "annual_taxable_income": taxable_income,
            "total_tax_withheld": total_tax_withheld,
            "total_net_income": net_income,
            "estimated_tax_refund": tax_refund,
            "tax_estimate" : tax_estimate,
            "has_tfn": False
        }

        return result


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

