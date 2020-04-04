# Explaining the code


**Library Import**
from twilio.rest import Client *Adding Twilio library for sending messages*
import time
import pyfirmata *Adding pyFirmata to make it possible for python to communicate serially with Arduino*
import math 


**Initializations**
db_meanings = {} *Dictionary database for storing meaning i.e words associated with each gesture*
db_numbers = {} *Dictionary database for storing phone numbers associated with each gesture*
board = pyfirmata.Arduino("/dev/ttyACM0") *Initiating Arduino board to communicate with Python*
it = pyfirmata.util.Iterator(board) *Initializing Iterator to continously communicate with Arduino*
it.start() *Starting the iterator; iterator is not really needed in this case; more of a convention*


**The following block of code unitl next comment are initializing various pins like a:2:i ==> analog2 pin in input mode**
flex_input_1 = board.get_pin("a:0:i")
flex_input_2 = board.get_pin("a:1:i")
flex_input_3 = board.get_pin("a:2:i")
acc_input_x = board.get_pin("a:3:i")
acc_input_y = board.get_pin("a:4:i")
acc_input_z = board.get_pin("a:5:i")
green_led = board.get_pin("d:4:o")
red_led = board.get_pin("d:5:o")


**Function to send *message* to *rec* number**
def send_message(message,rec):
    client = Client("........", "........")
    client.messages.create(to=rec, from_="+12029526477", body= message)


**Function to blink *led* (either red or green) *n* times**
def blink_led(led,n):
    if led == "red":
        for i in range(0,n):
            red_led.write(1)
            time.sleep(1)
            red_led.write(0)
            time.sleep(1)
    else:
        for i in range(0,n):
            green_led.write(1)
            time.sleep(1)
            green_led.write(0)
            time.sleep(0)


**This function actually sends the message by looking in the dictionary using the input key *nnnnn*/**
**First we get the message by understanding the gesture and then we send it to the number indicated by next gesture**
def send_message_v2():
    *Blink the green light 5 times*
    blink_led("green",5)
    print("Start composing the message")
    time.sleep(1)
    seq = getSequence()
    msg = db_meanings.get(seq,d = -1)
    if msg == -1:
        *Blink red led 5 times*
        blink_led("red",5)
        print("Mesage not found")
        return -1
    *Blink the green light 5 times*
    blink_led("green",5)
    print("Enter the number")
    time.sleep(1)
    seq = getSequence()
    num = db_numbers.get(seq,d =-1)
    if num == -1:
        *Blink red led 5 times*
        blink_led("red",5)
        print("Number not found")
        return -1
    *Blink the green light 3 times*
    blink_led("green",3)
    send_message(msg,num)
    print("Message sent")


**Not needed due to absence of configuration possibility**
def add_to_db(seq,msg):
    db_meanings[seq] = msg


**Initial populating the databases**
def init_pop_db():
    db_meanings["00000"] = "Hello"
    db_meanings["10000"] = "Hai"
    db_meanings["11000"] = "Bye"
    db_meanings["11110"] = "Help Me"
    db_meanings["11111"] = "I am hungry"
    db_meanings["10001"] = "I am lost"
    db_numbers["00000"] = "+917995968475"
    db_numbers["01010"] = "+919640951831"
    db_numbers["11111"] = "+918639872231"

**There will be configuration function here in the real code which is actually commented and not used**


**This *getSequence()* function will get input from the sensors to Arduino in a customized form**
**/*nnnnn* is the customized input where each n = 0/1 represents input data from each of the five sensors; two from accelerometer and three from flex sensors**
def getSequence():
    *The flex_values and roll, pitch are the final inputs from the sensors and depending on their we will add 0 or 1 to seq*
    flex_value_1 = flex_input_1.read()
    flex_value_2 = flex_input_2.read()
    flex_value_3 = flex_input_3.read()
    acc_x = acc_input_x.read()
    acc_y = acc_input_y.read()
    acc_z = acc_input_z.read()
    acc_x_g_val = (acc_x*5/1024-1.65)/0.330
    acc_y_g_val = (acc_y*5/1024-1.65)/0.330
    acc_z_g_val = (acc_z*5/1024-1.80)/0.330 
    roll = math.atan2(acc_y_g_val,acc_z_g_val)*180/3.14+180
    pitch = math.atan2(acc_z_g_val,acc_x_g_val)*180/3.14+180
    seq = ""
    if flex_value_1 >= 200:
        seq += 1
    else:
        seq += 0
    if flex_value_2 >= 200:
        seq += 1
    else:
        seq += 0
    if flex_value_3 >= 200:
        seq += 1
    else:
        seq += 0
    if roll >= 200:
        seq += 1
    else:
        seq += 0
    if pitch >= 200:
        seq += 1
    else:
        seq += 0
    return seq


**Driver Code i.e. the part of the program where the execution starts and ends**
if name == "main":
    *Blink both red and green led's thrice*
    for i in range(0,3):
        red_led.write(1)
        green_led.write(1)
        time.sleep(1)
        red_led.write(0)
        green_led.write(0)
        time.sleep(1)
    print("Entering the programm...")
    *Calling init_pop_db() to  fill the dictionaries with initial entires for corresponding gestures each time Arduino is started*
    init_pop_db()
    *Blink green led twice*
    blink_led("green",2)
    print("Booted up")
    *Continous loop which runs on Arduino waiting for each gesture*
    while True:
        *Getting initial sequence*
        seq = getSequence()
        *If that seq is 10101 then we will take the input, similar to asking user to press 1 before entering any real input*
        while seq != "10101":
            *Taking real input through getSequence function*
            seq = getSequence()
            *Waiting for a second before checking if user entered 10101 as the initial sequence*
            time.sleep(1)
        *If the intial sequence matches 10101 then we are sending message of the real input we took inside while loop*
        send_message_v2()