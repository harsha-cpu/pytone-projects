from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', (name, price, image))
        conn.commit()
        conn.close()
        return redirect(url_for('manage_products'))
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        conn.execute('UPDATE products SET name = ?, price = ?, image = ? WHERE id = ?', (name, price, image, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('manage_products'))
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/manage_products')
def manage_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('manage_products.html', products=products)

@app.route('/product_list')
def product_list():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('product_list.html', products=products)

@app.route('/product/<int:product_id>')
def single_product_view(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return render_template('single_product.html', product=product)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    return render_template('cart.html', cart=cart_items)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session.modified = True
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and str(product_id) in session['cart']:
        session['cart'].pop(str(product_id))
        session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
