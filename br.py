from twilio.rest import Client
import time

db_meanings = {}
db_numbers = {}


def send_message(message,rec):
    client = Client("AC74b994c82cd3828c4ad9257fff440b1c", "e56dae188746693801abe43889432742")
    client.messages.create(to=rec, from_="+12029526477", body= message)


def send_message_v2():
    #Blink the green light 5 times
    print("Start composing the message")
    time.sleep(1)
    seq = getSequence()
    msg = db_meanings.get(seq,d = -1)
    if msg == -1:
        #Blink red led 5 times
        print("Mesage not found")
        return -1
    #Blink the green light 5 times
    print("Enter the number")
    time.sleep(1)
    seq = getSequence()
    num = db_numbers.get(seq,d =-1)
    if num == -1:
        #Blink red led 5 times
        print("Number not found")
        return -1
    #Blink the green light 3 times
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


## Code after downloading ard py connection
def getSequence():
    return "11111"