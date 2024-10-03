# Import libraries
from flask import Flask, redirect, request, render_template, url_for
# Instantiate Flask functionality
app = Flask(__name__)

# Sample data

transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        #Crea la nueva transacion
        transaction = {
            'id' : len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Agrega la nueva transaccion
        transactions.append(transaction)
        #Redirigimos
        return redirect(url_for('get_transactions'))
    return render_template('form.html')
    
    
# Update operation
@app.route('/edit/<int:transaction_id>',methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    #Checamos si es POST desde el form
    if request.method == 'POST':
        #Extraemos los valores desde el form
        date = request.form['date']
        amount = float(request.form['amount'])

        #Encontramos la transaccion con el id dado y lo actualizamos
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        
        #Redirigimos a la lista de transacciones despues de la actualizacion
        return redirect(url_for("get_transactions"))
    
    #Si es get encontramos el id de la transaccion y mandamos render al edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:

            #Render el edit form y pasamos a editar
            return render_template("edit.html", transaction=transaction)

    #Si no enonctramos el id mandamos error
    return {"message": "Transaction not found"},404 


# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    return redirect(url_for("get_transactions"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    