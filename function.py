from project import *

def getAllStores():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT store_id, store_name, store_branch, store_address FROM stores")

    print("StoreId Storename StoreBranch StoreAddress")
    for row in cursor:
        print(row[0], row[1], row[2], row[3])

def getAllVendors():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT vendor_id, vendor_name, vendor_location, vendor_address FROM vendors")

    print("VendorId VendorName VendorBranch VendorAddress")
    for row in cursor:
        print(row[0], row[1], row[2], row[3])

def getReviewOfStoreLocation():
    location = input("Enter the branch name")
    if location.count == 0:
        print("You didn't provide a valid location")
        return

    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, store_name, store_review FROM stores WHERE store_branch='{location}';")
    print("StoreId Storename StoreReview")
    for row in cursor:
        print(row[0], row[1], row[2])
    print()
def getListOfDelayedOrders():
    cancellableOrders = []
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, orgin, destination, actual_delivery_time, delivery_time FROM orders WHERE actual_delivery_time > delivery_time;")
    print("OrderId Orgin Destination ActualDeliveryTime NormalDeliveryTime")
    for row in cursor:
        id = row[0]
        cancellableOrders.append(id)
        print(id, row[1], row[2], row[3], row[4])
    
    conn.close()

    yNChoice = input("Do you want to cancel any above mentioned order? (Y/N)")
    yNChoice = yNChoice.capitalize()
    if yNChoice != 'Y':
        return
    
    try:
        print("Enter an id from above?")
        idToCancel = int(input())
        if idToCancel not in cancellableOrders:
            print("This order isn't delayed! Can't be cancelled!")
            return

        conn = getConnection()
        query = f"UPDATE orders SET order_status='C' WHERE order_id={idToCancel};"
        cursor = conn.cursor()        
        cursor.execute(query)
        cursor.commit()
        conn.close()
        print("You sucessfully cancelled the order!")
    except:
        print("You entered an invalid id!")
        return
    
def cancelReturn(vendorId):
    try:
        print("Enter an id from above?")
        idToCancel = int(input())

        conn = getConnection()

        getQuery = f"SELECT order_status FROM orders WHERE order_id={idToCancel} AND vendor_id={vendorId};"
        cursor = conn.cursor()
        cursor.execute(getQuery)
        result=cursor.fetchone()
        if result == None:
            return
                    
        if(len(result) == 0):
            print("No order with this id exists!")
            return

        status = result[0]        
        charToChange = ""
        if status == 'C':
            charToChange = 'A'
        else:
            charToChange = 'C'
        conn.close()
        conn = getConnection()
        query = f"UPDATE orders SET order_status='{charToChange}' WHERE order_id={idToCancel};"
        cursor = conn.cursor()        
        cursor.execute(query)
        cursor.commit()
        conn.close()
        if status == 'C':
            print("You have accepted the order back!")
        else:
            print("You have cancelled the order!")
    except:
        print("You entered an invalid id!")
        return        

def deleteDrug(vendorId):
    try:
        medId = int(input("Enter the medicine id?"))
        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM vendor_med WHERE vendor_id={vendorId} AND medicine_id={medId};")
        conn.commit()
        conn.close()
        print("Succesfully removed the drug from your inventory!")
    except:
        print("Failed to update with the said id!")

def deleteDrugStore(storeId):

    try:
        medId = int(input("Enter the medicine id?"))
        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM med_store WHERE store_id={storeId} AND medicine_id={medId};")
        conn.commit()
        conn.close()
        print("Succesfully removed the drug from your inventory!")
    except:
        print("Failed to update with the said id!")        

def updateMinThreshold():
    try:
        medId = int(input("Enter the medicine id"))
        newThre = int(input("Enter the new threshold"))

        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"UPDATE vendor_med SET min_threshold={newThre} WHERE medicine_id={medId}")
        conn.commit()
        conn.close()
        print("Succesfully updated the minimum threshold!")
    except:
        print("Failed to update the threshold")

def updateMaxThreshold():
    try:
        medId = int(input("Enter the medicine id"))
        newThre = int(input("Enter the new threshold"))

        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"UPDATE vendor_med SET max_threshold={newThre} WHERE medicine_id={medId}")
        conn.commit()
        conn.close()
        print("Succesfully updated the max threshold!")
    except:
        print("Failed to update the threshold")

def changeRate(id):
    try:
        medId = int(input("Enter the medicine id"))
        newPrice = int(input("Enter the new order price"))

        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"UPDATE vendor_med SET med_unit_price={newPrice} WHERE medicine_id={medId}")
        conn.commit()
        conn.close()
        print("Succesfully updated the total order price")
    except:
        print("Failed to update the order price")

def changeTime():
    try:
        orderId = int(input("Enter the order id"))
        timeForDeliver = int(input("Enter the new time possible time for the order"))
        if timeForDeliver == 0:
            print("The date you entered is not valid!")
            return
        conn = getConnection()
        cur = conn.cursor()
        cur.execute(f"UPDATE orders SET actual_delivery_time={timeForDeliver} WHERE order_id={orderId}")
        conn.commit()
        conn.close()
        print("Succesfully updated the order time")
    except:
        print("Failed to update the order time")