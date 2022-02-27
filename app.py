from typing import OrderedDict
from flask import Flask
from flask import request
import json
from transaction import Transaction
app = Flask(__name__)
app.run(debug=True)


## global declarations
transactions = []
spend = OrderedDict()
dict1 = OrderedDict()


## API to add in new transactions
## return a statement telling that transactions have been added

@app.route("/add_transaction",methods = ['GET','POST'])
def add_transaction():
    if request.method == 'POST':
        data = request.get_json()
        if isinstance(data,list):
            for ele in data:
                transactions.append(Transaction(ele['payer'],ele['points'],ele['timestamp']))
            
        elif isinstance(data, dict):
            transactions.append(Transaction(data['payer'],data['points'],data['timestamp']))
        print(transactions)

    return "added transaction"

## API endpoint to calculate the points spent by each payer according to the rules defined in the transactions
## returns a JSON response with each payer and the points spent by them
    
@app.route("/spend_points",methods = ['GET','POST'])
def spend_points():
    if request.method == 'POST':
        data = request.get_json()
        points = data['points']
        dict2 = OrderedDict()
        translist = []
        output = []
        

        translist = sorted(transactions,key = lambda x:x.timestamp)


        for trans in translist:
            if trans.payer in dict2:
                continue
            else:
                spend[trans.payer] = 0
                dict2[trans.payer] = 0
        
        for ele in translist:
            if points == 0:
                break
            if ele.points < 0 or dict2[ele.payer] + ele.points < 0:
                dict2[ele.payer] = dict2[ele.payer] + ele.points
            else:
                if points > dict2[ele.payer] + ele.points:
                    points = points - (dict2[ele.payer] + ele.points)
                    spend[ele.payer] = spend[ele.payer] - (dict2[ele.payer] + ele.points)
                else:
                    spend[ele.payer] = spend[ele.payer] - points
                    points = 0
            

        for trans in translist:
            if trans.payer in dict1:
                dict1[trans.payer] = dict1[trans.payer] + trans.points
            else:
                dict1[trans.payer] = trans.points
        
        for key,value in spend.items():
            output.append({
                'payer' : key,
                'points' : value
            })
        
    return json.dumps(output)

## API endpoint to calculate the balance of each payer
## returns a JSON response which contains the balance of each payer 

@app.route("/point_balances",methods = ['GET'])
def point_balances():
    resultdict = OrderedDict()
    print(transactions)
    for trans in transactions:
        if trans.payer in resultdict:
            continue
        else:
            resultdict[trans.payer] = trans.points
 
    for key,value in dict1.items():
        resultdict[key] = value + spend[key]
    return json.dumps(resultdict)

## Default route
@app.route("/")
def home():
    return "Hello, Flask!"
