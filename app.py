from flask import Flask,render_template,request,redirect
import json
import os

app = Flask(__name__)

# Load data
def load_expenses():
    try :
        with open("expenses.json","r") as f:
            return json.load(f)
    except :
        return []

def save_expenses(data):
    with open("expenses.json",'w') as f:
        json.dump(data,f)  

@app.route("/")
def home():
    expenses = load_expenses()
    return render_template('index.html',expenses=expenses)

@app.route("/add",methods=["GET","POST"])
def add_expense():
    if request.method == "POST":
        name = request.form.get('name')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        date = request.form.get('date')

        expenses = load_expenses()

        expenses.append({
            "name" : name,
            "amount" : amount,
            "category" : category,
            "date" : date
        })

        save_expenses(expenses)

        return redirect("/")
    
    return render_template('add.html')

@app.route('/summary')
def summary():
    expenses = load_expenses()
    summary = {}

    for exp in expenses:

        category = exp['category']
        amount = float(exp['amount'])

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount
    
    return render_template('summary.html',summary=summary)


@app.route('/delete/<int:index>')
def delete(index):
    expenses = load_expenses()

    if 0 <= index < len(expenses):
        expenses.pop(index)
    
    save_expenses(expenses)
    return redirect('/')




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)