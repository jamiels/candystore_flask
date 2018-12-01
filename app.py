from flask import Flask
from flask import render_template
from flask import request
import mysql.connector as mc
print(mc.__version__)
# export FLASK_DEBUG=1
# $env:FLASK_DEBUG=1

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/orders/<orderid>")
def main(orderid=None):
    return render_template('orders.html',orderid=orderid)

@app.route("/query")
def query():
    name = request.args.get('name')
    color = request.args.get('color')
    print(name)
    print(color)
    return render_template('query.html',name=name,color=color)

@app.route("/form1")
def display_form1():
    return render_template('form_one.html')

# Try without methods
@app.route("/processForm1", methods=['POST'])
def process_form1():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    return render_template('form_one.html')

# http://flask.pocoo.org/docs/1.0/quickstart/

# 1 - use bootstrap startup page
# 2  - change to bootstrap.html
# 3 set FLASK_DEBUG=True
@app.route("/")
def candystore_main():
    product_rows = get_products()
    return render_template('candystore_main_bootstrap.2.html',product_rows=product_rows)

# create table product (product_id int, product_name varchar(50));
# insert into product values(1,'M&M'),(2,'KitKat'),(3,'Jelly Beans')

@app.route("/processOrder",methods=['POST'])
def candystore_processorder():
    qty = request.form['qty']
    itemSelected = request.form['itemOrdered']
    insert_order(qty,itemSelected)
    print('quantity is',qty)
    print('item ordered is',itemSelected)
    return "Order processed!" #render_template('candystore_main.html')

@app.route("/viewOrders")
def candystore_vieworders():
    orders = get_orders()
    return render_template('candystore_orders.1.html',orders=orders)

def get_products():
    connection = mc.connect(user='root', password='jamiel',
                              host='127.0.0.1', database='candystore',
                              auth_plugin='mysql_native_password')
    result = connection.cmd_query("select * from products")
    rows = connection.get_rows()
    connection.close()
    return rows[0]

def insert_order(qty,product_id):
    connection = get_connection()
    sql = "insert into orders (quantity,product_id) values (" + str(qty) + "," + str(product_id) + ");"
    result = connection.cmd_query(sql)
    connection.commit()


def get_orders():
    connection = get_connection()
    sql = "select * from orders, products where orders.product_id = products.product_id"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    connection.close()
    print(rows[0])
    return rows[0]

def get_connection():
    return  mc.connect(user='root', password='jamiel',
                              host='127.0.0.1', database='candystore',
                              auth_plugin='mysql_native_password')

'''
update product
set product_name = 'KitKatt'
where product_id=2
'''

'''
DROP TABLE orders;
CREATE TABLE orders (
     order_id MEDIUMINT NOT NULL AUTO_INCREMENT,
     quantity MEDIUMINT,
     product_id MEDIUMINT, 
     PRIMARY KEY (order_id)
);
'''
