from typing import OrderedDict
from flask import Flask
from flask import request
import json
from transaction import Transaction
app = Flask(__name__)
app.run(debug=True)

transactions = []

spend = OrderedDict()
dict = OrderedDict()
@app.route("/add_transaction",methods = ['GET','POST'])
def add_transaction():
    if request.method == 'POST':
        data = request.get_json()
        for ele in data:

            transactions.append(Transaction(ele['payer'],ele['points'],ele['timestamp']))
        print(transactions)
    return "added transaction"
    
@app.route("/spend_points",methods = ['GET','POST'])
def spend_points():
    if request.method == 'POST':
        data = request.get_json()
        points = data['points']
        spend = OrderedDict()
        dict2 = OrderedDict()
        translist = []
        #for trans in transactions:
            #translist.append([trans.payer,trans.points,trans.timestamp])
        translist = sorted(transactions,key = lambda x:x.timestamp)
        for trans in translist:
            if trans.player in dict1:
                continue
            else:
                spend[trans.player] = 0
                dict2[trans.player] = 0
        for ele in translist:
            if points == 0:
                break
            if ele.points < 0 or dict2[ele.player] + ele.points < 0:
                dict2[ele.player] = dict2[ele.player] + ele.points
            else:
                if points > dict2[ele.player] + ele.points:
                    points = points - (dict2[ele.player] + ele.points)
                    spend[ele.player] = spend[ele.player] - (dict2[ele.player] + ele.points)
                else:
                    spend[ele.player] = spend[ele.player] - points
                    points = 0
            

        for trans in translist:
            if trans.payer in dict:
                dict[trans.payer] = dict[trans.payer] + trans.points
            else:
                dict[trans.payer] = trans.points
        
    return json.dumps(spend)

@app.route("/point_balances",methods = ['GET'])
def point_balances():
    dict = OrderedDict()
    resultdict = OrderedDict()

    for key,value in dict.items():
        resultdict[key] = value + spend[key]
        
    return json.dumps(resultdict)

@app.route("/")
def home():
    return "Hello, Flask!"
