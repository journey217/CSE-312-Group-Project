from app import app,socketio

# initialize the app with the socket instance
# you could include this line right after Migrate(app, db)
socketio.init_app(app)

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0',allow_unsafe_werkzeug=True)


