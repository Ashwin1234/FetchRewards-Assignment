from typing import OrderedDict
from flask import Flask
from flask import request
from flask import Response
import json
from transaction import Transaction
app = Flask(__name__)
app.run(debug=True)


## global declarations
transactions = []
spend = OrderedDict()
dict1 = OrderedDict()
dict2 = OrderedDict()
resultdict = OrderedDict()



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
    
    for trans in transactions:
        if trans.payer in resultdict:
            continue
        else:
            resultdict[trans.payer] = trans.points

    return "added transaction"

## API endpoint to calculate the points spent by each payer according to the rules defined in the transactions
## returns a JSON response with each payer and the points spent by them
    
@app.route("/spend_points",methods = ['GET','POST'])
def spend_points():
    if request.method == 'POST':
        data = request.get_json()
        points = data['points']
        
        translist = []
        output = []
        
        total_points = 0

        translist = sorted(transactions,key = lambda x:x.timestamp)

        for key,value in resultdict.items():
            total_points = total_points + value
        
        if total_points < points:
            return Response(
                "Insufficient balance", status = 400, mimetype = 'application/json'
            )

        if isinstance(points,int) == False and isinstance(points,float) == False:
            return Response(
                "Points should be a number", status = 400, mimetype = 'application/json'
            )

        if points < 0:
            return Response(
                "Points cannot be negative", status = 400, mimetype = 'application/json'
            )
        
        for trans in translist:
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
                    dict2[ele.payer] = 0
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
        for key,value in resultdict.items():
            resultdict[key] = value + spend[key]
        
    return json.dumps(output)

## API endpoint to calculate the balance of each payer
## returns a JSON response which contains the balance of each payer 

@app.route("/point_balances",methods = ['GET'])
def point_balances():
    
    print(transactions)

    return json.dumps(resultdict)

## Default route
@app.route("/")
def home():
    return "Hello, Flask!"
