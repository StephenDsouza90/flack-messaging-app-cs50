from collections import deque

from flask import Flask, session, request, render_template, redirect
from flask_socketio import SocketIO, emit

from decorator import handle_login


channels = {}
messages = dict()
users = []
emoji = ["\U0001f600", "\U0001F606", "\U0001F923", "\U0001F61B", "\U0001F61C"]


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
socketio = SocketIO(app)


@app.route("/")
@handle_login
def index():
    """ Home page """

    return render_template("index.html", channels=channels)


@app.route("/display-name", methods=["GET", "POST"])
def display_name():
    """ User is asked to display a name """

    session.clear()
    username = request.form.get("username")

    if request.method == "POST":
        if not username:
            return render_template("error.html", 
                message="Please provide username!")
        elif username in users:
            return render_template("error.html", 
                message="Username already exist!")
        else:
            users.append(username)
            session["username"] = username
            session.permanent = True
            return redirect("/")
    else:
        return render_template("display_name.html")


@app.route("/logout", methods=["GET"])
def logout():
    """ User logout """

    users.remove(session['username'])
    session.clear()
    return redirect("/")


@app.route("/create-channel", methods=["GET", "POST"])
@handle_login
def create_channel():
    """ Create channel """

    new_channel = request.form.get("channel")
    user = session.get('username')

    if request.method == "POST":
        if new_channel in channels:
            return render_template("error.html", 
                message="Channel already exists!")
        elif not new_channel:
            return render_template("error.html", 
                message="Please provide a channel name!")
        else:
            channels[new_channel] = user
            messages[new_channel] = deque()
            return redirect("/channel/" + new_channel)
    else:
        return render_template("display_name.html")


@app.route("/channel/<channel>", methods=["GET"])
@handle_login
def channel(channel):
    """ Channel page - Send and receive messages """

    session['current_channel'] = channel
    return render_template("channel.html", name=channels.get(channel), messages=messages[channel], emoji=emoji)


@socketio.on("message")
def handle_message(msg, timestamp):
    """ Broadcaste message """

    room = session.get('current_channel')

    if len(messages[room]) > 100:
        messages[room].popleft()
    else:
        messages[room].append([timestamp, session.get('username'), msg])
    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg}, 
        broadcast=True)


if __name__=='__main__':
    socketio.run(app, debug=True)