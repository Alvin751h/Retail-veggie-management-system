import csv
from datetime import date
from prettytable import *
import pandas as pd 
import os
import tkinter as tk
from tkinter import filedialog
from keras.api.layers import *
from keras.api.optimizers import *
from tensorflow.python.keras.models import load_model
import cv2
from prettytable import PrettyTable
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  
model = load_model('vegetable-classification.ipynb')  #  trained model

def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    return file_path

def recognize_item(image_path):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (224, 224))  # Resize to model input size
    img_array = np.expand_dims(img_resized, axis=0) / 255.0  # Normalize

    prediction = model.predict(img_array)
    item_index = np.argmax(prediction)
    return labels[item_index]

if not os.path.exists('items.csv'):
     with open("items.csv", mode='w', newline='') as file202:
         wrt=csv.writer(file202)
         wrt.writerow(['Name','Quantity','Price(rs)'])
sname=' '
#to set shop name
def setname():
    ssname=input("enter shop name:")
    print(f"shop name has been set to {sname}")
    with open('sname.txt','w') as namee:
        namee.write(ssname)
    print(f"\nsuccesfully set shop name as {ssname}")

#to input items into the csv file
def inputitem():
    ap = open("items.csv", "a", newline="")
    w = csv.writer(ap)
    n = 0

    while True:
        print("Select an image for the item (or click cancel to stop):")
        image_path = select_image()
        if not image_path:  # If no file is selected
            print("Stopped adding items.")
            break

        # Recognize item name from the image
        item_name = recognize_item(image_path)
        print(f"Recognized item: {item_name}")

        qty = int(input("Enter quantity: "))
        price = int(input("Enter price: "))
        w.writerow([item_name, qty, price])
        n += 1

    print(f"\nSuccessfully added {n} items to items.csv")


#to print the items csv
def show():
    table = PrettyTable()
    with open('items.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        table.field_names = headers
        for row in reader:
            table.add_row(row)
    print(table)
    
#billing function
def bill_with_image():
    global sname
    with open("sname.txt", "r") as reaad:
        sss = reaad.read()
        sname = str(sss)
    billamnt = 0

    user = input("Customer name: ")
    n = int(input("Mobile number: "))

    table = PrettyTable()
    table.field_names = ["Name", "Quantity", "Price"]

    data = pd.read_csv("items.csv")
    while True:
        print("Select an image for the item (or click cancel to stop):")
        image_path = select_image()
        if not image_path:  # If no file is selected
            print("Stopped billing items.")
            break

        # Recognize item name
        item_name = recognize_item(image_path)
        print(f"Recognized item: {item_name}")

        qty = int(input("Enter quantity: "))
        row = data[data["Name"] == item_name]

        if row.empty:
            print(f"{item_name} not found in inventory!")
            continue

        stock_qty = int(row["Quantity"])
        price = int(row["Price(rs)"])

        if stock_qty < qty:
            print(f"Only {stock_qty} {item_name}(s) left!")
        else:
            data.loc[data["Name"] == item_name, "Quantity"] = stock_qty - qty
            data.to_csv("items.csv", index=False)
            table.add_row([item_name, qty, f"{price * qty}\u20B9"])
            billamnt += price * qty

    billp = (
        f"\n\n**************************************************************\n"
        f"                    |{sname}|\n"
        f"  >name:{user}\n  >contact no:{n}\n  >date:{date.today()}\n"
        f"**************************************************************\n\n"
        f"{table}\n                 grand total: {str(billamnt)}₹\n\n"
        "Thank You for purchasing from us\n"
        "**************************************************************"
    )
    print(billp)

    with open(f"bill_{n}.txt", "w", encoding="utf-8") as billt:
        billt.write(billp)
        print(f"Bill is saved in your system as bill_{n}.txt")


#add stock
def addstock():
    a=input("enter item name to add quantity: ").lower().strip()
    n=int(input("enter quantity to be added: "))
    data = pd.read_csv("items.csv")
    with open('items.csv', 'r') as file1:
                reader1 = csv.DictReader(file1)
                for row in reader1:
                    if row['Name'] == a:
                        qty=(int(row['Quantity']))
    data.loc[data["Name"]==a, "Quantity"] = (qty+n)
    data.to_csv("items.csv", index=False)
    print(f"\nsuccesfully added {n} more {a} to the quantity")

#delete item
def delete():
    a=input("enter item name to be deleted: ").lower().strip()
    df=pd.read_csv("items.csv",index_col="Name")
    df=df.drop(a)
    df.to_csv("items.csv",index=True)
    print(f"\nsuccesfully deleted {a} from items.csv")

#user define
ch='Y'
print('Hi This is Python store management system\n')
while ch.upper().strip()=='Y':
    print('>>>we have 6 main commands:')
    print('setname     -     >Allows Shop owner to set their shop \n                    name to be shown in the bill\n')
    print('input       -     >Enables Shop owner to input\n                    item name, quantity, price\n                    in a csv file\n')
    print('add         -     >Enebles Shop owner to add more\n                  quantity to an item\n')
    print('delete      -     >Allows Shop owner to delete a\n                   specific item\n')
    print('show        -     >Displays the csv file of items\n')
    print('bill        -     >Lets the Cashier/owner create\n                    a bill for customer which will\n                    be displayed and saved in the\n                    system as txt file\n')
    print("\n**************************************************************\n**************************************************************\n")
    choice=input("enter command to be done: ")
    if choice.lower().strip()=="setname": setname()
    if choice.lower().strip()=="input": inputitem()
    if choice.lower().strip()=="show": show()
    if choice.lower().strip()=="bill": bill_with_image()
    if choice.lower().strip()=="add": addstock()
    if choice.lower().strip()=="delete": delete()
    print("\n**************************************************************\n**************************************************************\n")
    ch=input("do u want to execute another command?(Y/N): ")
if ch.upper()=="N":
    print(".\n.\n.\n...Thankyou for using our shop management system!!!")
