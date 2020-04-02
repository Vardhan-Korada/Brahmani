from twilio.rest import Client
import time
import pyfirmata
import math


#Constants
db_meanings = {}
db_numbers = {}
#Change path to board
board = pyfirmata.Arduino("/dev/ttyACM0")
it = pyfirmata.util.Iterator(board)
it.start()
flex_input_1 = board.get_pin("a:0:i")
flex_input_2 = board.get_pin("a:1:i")
flex_input_3 = board.get_pin("a:2:i")
acc_input_x = board.get_pin("a:3:i")
acc_input_y = board.get_pin("a:4:i")
acc_input_z = board.get_pin("a:5:i")
green_led = board.get_pin("d:4:o")
red_led = board.get_pin("d:5:o")


def send_message(message,rec):
    client = Client("********", "*******")
    client.messages.create(to=rec, from_="+12029526477", body= message)


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


def send_message_v2():
    #Blink the green light 5 times
    blink_led("green",5)
    print("Start composing the message")
    time.sleep(1)
    seq = getSequence()
    msg = db_meanings.get(seq,d = -1)
    if msg == -1:
        #Blink red led 5 times
        blink_led("red",5)
        print("Mesage not found")
        return -1## Code after downloading ard py connection
    #Blink the green light 5 times
    blink_led("green",5)
    print("Enter the number")
    time.sleep(1)
    seq = getSequence()
    num = db_numbers.get(seq,d =-1)
    if num == -1:
        #Blink red led 5 times
        blink_led("red",5)
        print("Number not found")
        return -1
    #Blink the green light 3 times
    blink_led("green",3)
    send_message(msg,num)
    print("Message sent")


## Not needed due to absence of configuration possibility
def add_to_db(seq,msg):
    db_meanings[seq] = msg


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


## Put it on the hold due to input device problems
# def configure_mode():
#     #Blink the green led thrice
#     print("Do the action...")
#     seq = getSequence()
#     #Blink the green led thrice
#     print("Do the action again...")
#     rep_seq = getSequence()
#     if seq == rep_seq:
#         #Blink the 
#         msg = input("Enter its meaning")
#         db_meanings


def getSequence():
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


if __name__ == "__main__":
    # Blink both red and green led's thrice
    for i in range(0,3):
        red_led.write(1)
        green_led.write(1)
        time.sleep(1)
        red_led.write(0)
        green_led.write(0)
        time.sleep(1)
    print("Entering the programm...")
    init_pop_db()
    # Blink green led twice
    blink_led("green",2)
    print("Booted up")
    while True:
        seq = getSequence()
        while seq != "10101":
            seq = getSequence()
            time.sleep(1)
        send_message_v2()

    