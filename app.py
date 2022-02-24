from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/add_transaction",methods = ['GET'])
def add_transaction():
    return "addtransaction"

@app.route("/spend_points",methods = ['GET','POST'])
def spend_points():
    return "spendpoints"

@app.route("/point_balances",methods = ['GET'])
def point_balances():
    return "pointbalances"

@app.route("/")
def home():
    return "Hello, Flask!"
