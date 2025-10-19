import pyodbc
from function import *;

def getConnection():
    return pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-KUEGS2UO\TSQL;'
                      'Database=pyth;'
                      'Trusted_Connection=yes;')


def getInitialState():
    initStateChoices = [1, 2, 3, 4]
    choice = 0
    print("Enter your authentication option")
    print("1. Sign up")
    print("2. log in")
    print("3. Exit")
    try:
        choice = int(input())
    except:
        print("Incorrect choice entered! Retry Again")
        return True

    if choice not in initStateChoices:
        print("Incorrect choice entered! Retry Again")
        return True

    if(choice == 3):
        global cont
        cont = False
        print("Exiting...")
        return False

    roleId = getRole()
    while roleId == -1:
        print("You entered wrong role id")
        roleId = getRole()

    if(choice == 1):
        signup(roleId)

    if(choice == 2):
        isLoggedIn = signin(roleId)
        if isLoggedIn == -1:
            print("Incorrect login")
            return True

        if roleId == 1:
            getStoreMenu(isLoggedIn)
            return True
        else:
            getVendorMenu(isLoggedIn)
            return True

def getStoreMenu(storeId):
    doMenu = True
    possibleChoices = [1, 2, 3, 4, 5, 6, 7]
    storeChoice = 0
    while(doMenu):
        print("1. List all stores")
        print("2. Get Review of a Store Branch")
        print("3. Delete Drug")
        print("4. Update Minimum Threshold")
        print("5. Update Maximum Threshold")
        print("6. Change Time For Delivery")     
        print("7. Change Rate For Drug")     
        print("8. Exit")
        try:
            storeChoice = int(input())
        except:
            print("Please enter a valid integer!")
            return
        
        if storeChoice not in possibleChoices:
            print("Please enter a valid choice!")

        if storeChoice == 8:
            doMenu = False
            return

        if storeChoice == 1:
            getAllStores()
        elif storeChoice == 2:
            getReviewOfStoreLocation()
        elif storeChoice == 3:
            deleteDrugStore(storeId)
        elif storeChoice == 4:
            updateMinThreshold()
        elif storeChoice == 5:
            updateMaxThreshold()
        elif storeChoice == 6:
            changeTime()
        elif storeChoice == 7:
            changeRate(storeId)


def getVendorMenu(vendorId):
    doMenu = True
    possibleChoices = [1, 2, 3, 4, 5]
    vendorChoice = 0
    while(doMenu):
        print("1. List all suppliers")
        print("2. List of order taking more time")
        print("3. Cancel Return")
        print("4. Delete Drug")     
        print("5. Exit")
        try:
            vendorChoice = int(input())
        except:
            print("Please enter a valid integer!")
            return
        
        if vendorChoice not in possibleChoices:
            print("Please enter a valid choice!")

        if vendorChoice == 5:
            doMenu = False
            return

        if vendorChoice == 1:
            getAllVendors()
        elif vendorChoice == 2:
            getListOfDelayedOrders()
        elif vendorChoice == 3:
            cancelReturn(vendorId)
        elif vendorChoice == 4:
            deleteDrug(vendorId)
    
def signup(roleId):
    if(roleId == 2):
        fetch = True
        username = ""
        password = ""
        storename = ""
        address = ""
        contact = ""
        email = ""
        while(fetch):
            username = input("Enter username: ")
            password = input("Enter password: ")            
            storename = input("Enter Storename: ")
            address = input("Enter address: ")
            contact = input("Enter contact: ")
            email = input("Enter email: ")
            branch = input("Enter branch: ")

            if username.count == 0 or password.count == 0 or storename.count == 0 or address.count == 0 or contact.count == 0:
                fetch = True
                print("Please enter the information again, Some fields are missing!")
            else:
                fetch = False
            

        storeSignUpQuery = f'''
        INSERT INTO stores
           ([store_password]
           ,[store_username]
           ,[store_name]
           ,[store_branch]
           ,[store_address]
           ,[store_contact]
           ,[store_email]
           ,[role_id])
     VALUES
           (
            '{password}'
           ,'{username}'
           ,'{storename}'
           ,'{branch}'
           ,'{address}'
           ,'{contact}'
           ,'{email}'
           ,1
           );
        '''

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(storeSignUpQuery)
        cursor.commit()
        conn.close
        print(f'Succesfully signed up as {storename}!')
        return True
    else:
        fetch = True
        username = ""
        password = ""
        name = ""
        loc = ""
        address = ""
        email = ""
        contact = ""
        while(fetch):
            username = input("Enter username: ")
            password = input("Enter password: ")            
            storeName = input("Enter Vendor name: ")
            address = input("Enter address: ")
            contact = input("Enter contact: ")
            email = input("Enter email: ")
            loc = input("Enter loc: ")      

            if username.count == 0 or password.count == 0 or storeName.count == 0 or address.count == 0 or contact.count == 0 or loc.count == 0:
                fetch = True
                print("Please enter the information again, Some fields are missing!")
            else:               
                fetch = False

        signupVendorQuery = f'''
            INSERT INTO vendors
            ([vendor_password]
            ,[vendor_username]
            ,[vendor_name]
            ,[vendor_location]
            ,[vendor_address]
            ,[vendor_email]
            ,[vendor_contact]
            ,[role_id])
        VALUES
            (
            '{password}'
            ,'{username}'
            ,'{storeName}'
            ,'{loc}'
            ,'{address}'
            ,'{email}'
            ,'{contact}'
            ,2
            );            
        '''

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(signupVendorQuery)
        cursor.commit()
        conn.close
        print(f'Succesfully signed up as {storeName}!')
        return True


def signin(roleId):
    fetch = True
    username = ""
    password = ""
    
    while(fetch):
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username.count == 0 or password.count == 0:
            fetch = True
            print("Please provide a username and password")
        else:
            fetch = False
    
    query = ""
    if(roleId == 2):
        query = f'''
            SELECT store_id FROM stores WHERE store_username='{username}' AND store_password='{password}';
        '''
    else:
        query = f'''
            SELECT vendor_id FROM vendors WHERE vendor_username='{username}' AND vendor_password='{password}';
        ''' 
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query)
    result=cursor.fetchone()
    conn.close()       
    if result == None:
        return -1
        
    if len(result) == 0:
        return -1
    
    return result[0]

def getRole():
    roleChoice = [1, 2]
    print("Specify your role")
    print("1. Supplier")
    print("2. Store")
    try:
        choice = int(input())
    except:
        print("Incorrect choice entered! Retry Again")
        return -1

    if choice not in roleChoice:
        return -1

    return choice


def main():
    cont = True
    while(cont):
        x = getInitialState()
        if x == False:
            cont = False
            break

if __name__ == "__main__":
    main()    
    