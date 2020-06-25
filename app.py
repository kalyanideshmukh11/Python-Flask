from flask import Flask, render_template, request
from datetime import datetime
import yfinance as yf
from requests.exceptions import ConnectionError
from requests.exceptions import InvalidURL
import lxml
import json
app = Flask(__name__)


@app.route('/')
def display_index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def calculate():
    sym = request.form['sym']
    stock = yf.Ticker(sym)
    x=0
    while x<1:
        try:
            json_response = stock.info
            break
        except (ImportError,IndexError,UnboundLocalError,NameError,InvalidURL):
            submit = request.form['submit']
            error = "Invalid Symbol"
            return render_template('index.html', submit=submit, error=error)
        except ConnectionError:
            submit = request.form['submit']
            error = "Connection Issue"
            return render_template('index.html', submit=submit, error=error)
            #print("Invalid Stock Symbol")
            x=1

    #json_response = stock.info
    if json_response is not None:
            date1 = datetime.now()
            symb=sym
            name = json_response['longName']
            name=(str(name) + ' (' +str(symb)+') ')
            previousClose=json_response['previousClose']
            current_value=json_response['bid']
            value_change=round((current_value-previousClose), 2)
            percentage_change= round(float((value_change/previousClose)*100), 2)
            value_change = ('+ ' + str(value_change)) if value_change >= 0 else str(value_change)
            percentage_change = ('+ ' + str(percentage_change) + '%') if percentage_change >= 0 else str(percentage_change) +'%'
            submit = request.form['submit']
        #print json_response
            return render_template('index.html', date1=date1, sym=sym, name=name,current_value=current_value, stock=stock, symb=symb, value_change=value_change, percentage_change=percentage_change, submit=submit)
    else:
            submit = request.form['submit']
            error = "Ticker not Available"
            return render_template('index.html', submit=submit, error=error)

if __name__ == '__main__':
    app.run()
