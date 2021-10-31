from flask import Flask, render_template
from flask_socketio import SocketIO, send
from threading import Thread
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
socketio = SocketIO(app)

status = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



def print_something(msg):
    count = 0
    print("Hello this is running on thread\n")
    while count<10:
        count+=1
        print(count, "seconds gone!\n")
        sleep(1.5)
    # socketio.send("Done") # broadcasting
    status.update({f"{msg}" : "Done"})



@socketio.on('message')
def socket_bbb(msg):
    str(msg)
    if msg != "User has connected!":
        t0 = Thread(target=print_something, args=(msg,), daemon = True)
        t0.start()
        
        while True:
            print("Status: ", status)
            sleep(1.5)
            if status.get(msg) == "Done":
                send("Done")
                print("Status: ", status)
                break
        del status.get(msg)
        print("Status: ", status)

    if msg == "User has connected!":
        print(msg)




if __name__ == '__main__':
	socketio.run(app, debug=True)