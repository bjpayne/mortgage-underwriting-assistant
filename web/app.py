from flask import Flask, render_template
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
