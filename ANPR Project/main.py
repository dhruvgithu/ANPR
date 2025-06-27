# toaster = win10toast.ToastNotifier()
# toaster.show_toast("ALARM", f"{real}", duration=5)

import win10toast #for notification
import datetime
from tkinter import *  # FOR GUI
from twilio.rest import Client # FOR MESSAGE SENDING
import easyocr # FOR EXTRACTING TEXT FROM THE IMAGE
import cv2     # FOR COMPUTER VISION
from PIL import ImageTk, Image # Image compressor


sid="ACf026f2aef2b48ac3ad977e517d826ea4"  #CREDENTIAL OF TWILIO
auttoken="76f27b562a5a1d835ffcb9bd4b620665" ##REDENTIAL OF TWILIO



def window(name,no,state,num):  #  GUI 
    root = Tk()
    root.config(bg="lightblue")
    root.geometry('1500x650')
    root.title("Team Immortals ANPR")

    label_0 = Label(root, text="Team Immortals ANPR", width=20, font=("bold", 35), bg="yellow", fg="red")
    label_0.place(x=620, y=5)

    label_1 = Label(root, text="Name", width=20, font=("bold", 25), bg="orange")
    label_1.place(x=570, y=150)

    entry_1 = Label(root, text=name, font="bold 25")
    entry_1.place(x=1000, y=150)

    label_2 = Label(root, text="Vehicle No.", width=20, font=("bold", 25), bg="white", fg="dark blue")
    label_2.place(x=570, y=220)

    entry_2 = Label(root, text=no, font="bold 25")
    entry_2.place(x=1000, y=220)

    label_3 = Label(root, text="Area", width=20, font=("bold", 25), bg="green")
    label_3.place(x=570, y=280)

    entry_3 = Label(root, text=state, font="bold 25")
    entry_3.place(x=1000, y=280)

    label_4 = Label(root, text="Phone No.", width=20, font=("bold", 25), bg="orange")
    label_4.place(x=570, y=350)

    entry_4 = Label(root, text=num, font="bold 25")
    entry_4.place(x=1000, y=350)

    button1 = Button(root, text="Send E-Challan", font="bold 25")
    button1.place(x=800, y=550)

    img = Image.open("96a683e9-2e35-4102-bd4d-f9495cc146d9.png")
    img_new = img.resize((450, 350))
    image = ImageTk.PhotoImage(img_new)

    label = Label(root, image=image)
    label.place(x=20, y=90)

    root.mainloop()


# SENDING THE MESSAGE

def msg(Owner,vehicle_no):
    date_today=datetime.date.today()
    time_today=datetime.time()
    message=f"Dear {Owner},This is to inform you your vehicle {vehicle_no},has been found parked in wrong parking " \
            f"The offense occurred on {date_today} and {time_today} at the following location: XXdelXX" \
            f"According to the regulations stated in the Motor Vehicles Act, 1988, Section 48, Clause 8C, you are liable to pay a fine for this offense." \
            f"Offense: Wrong Parking Fine Amount: INR 1000 Due Date: 27-05-2023 Payment Method: Online/Offline ,Failure to pay the imposed fine on or " \
            f"before the due date will result in further legal consequences, including additional fines, vehicle impoundment." \
            f"If you believe this chalan has been issued in error, you may appeal against it within 25-05-2023. " \
            f"For the appeal process and further assistance, please contact the RTO OFFICE at +18006478965 or mhtrrto@gov.in." \
            f"We appreciate your cooperation in this matter and urge you to comply with the regulations to ensure the smooth functioning and safety of all road users." \
            f"Ministry of Tranport"
    return message

# For Checking the STATE

dict={"AP":"Andhra Pradesh","AR": "Arunachal Pradesh","AS":"ASSAM","BR":"BIHAR","CG":"Chhattisgarh","GA":"GOA",
      "GJ":"GUJRAT","HR":"HARYANA","HP":"Himanchal Prdaesh","JH":"Jharkhand","KA":"Karnataka","KL":"Kerela","DL":"Delhi",
"AN":"Andaman and Nicobar Islands", "CH":"Chandigarh", "DN":"Dadra and Nagar Haveli" ,"DD":"Daman and Diu","JK":"Jammu and Kashmir" ,"LA":"Ladakh" ,
      "LD":"Lakshadweep", "PY":"Puducherry","UA":"Uttarakhand",
"MP":"Madhya Pradesh" ,"MH":"Maharashtra" ,"MN":"Manipur", "ML":"Meghalaya" ,"MZ":"Mizoram", "NL":"Nagaland" ,"OD":"Odisha" ,"PB":"Punjab", "RJ":"Rajasthan" ,
      "SK":"Sikkim", "TN":"Tamil Nadu" ,"TS":"Telangana", "TR":"Tripura", "UP":"Uttar Pradesh" ,"UK":"Uttarakhand", "WB":"West Bengal"

      }

harcascade = "model/haarcascade_russian_plate_number.xml" # Harcascade

cap = cv2.VideoCapture(0) # For Capturing from Video Camera

cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500  # For Number Plate
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(
    r'C:\Users\dhruv\OneDrive\Desktop\Mini Project\ANPR-main\ANPR-main\model\haarcascade_russian_plate_number.xml'
)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
            img_roi = img[y: y + h, x:x + w]
            cv2.imshow("Number Plate", img_roi)

    cv2.imshow("INPUT FEED", img)


    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scanned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("INPUT FEED", img)
        cv2.waitKey(500)

        reder=easyocr.Reader(['en'])
        result=reder.readtext("plates/scanned_img_" + str(count) + ".jpg")   
        number_plate = result[0][1]
        state = number_plate[:2]


        try:
            print(f"Vehicle Number {number_plate}")
            print(f"Vehicle Registration area is {dict[state]}")
            name="MR. XXDXJX"
            print(f"Owner Name {name}")
            number=' +917xxxx5xxxx'
            print(f"Phone Number {number}")
            count += 1
            window(name,number_plate,state,number)
            message=msg(name,number_plate)
            cl = Client(sid, auttoken)
            cl.messages.create(body=message, from_='+12525126957', to='+917017482038')
        except Exception as e:
            print("NOT ABLE TO READ IT PROPERLY ... TRY AGAIN （*゜ー゜*）")


