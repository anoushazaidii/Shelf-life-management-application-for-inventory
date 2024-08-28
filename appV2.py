from flask import Flask, jsonify, render_template, request, redirect, send_file, url_for, flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Product, MaterialDescription, Issuance, User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import barcode
from barcode.writer import ImageWriter
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a secret key for session management

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  # Should be False since you're using TLS

app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
mail = Mail(app)

def send_shelf_life_alert(product, user_email):
    if product.shelf_life_remaining < 15:
        msg = Message('Shelf Life Alert!',
                      recipients=[user_email])
        msg.body = f"Dear User,\\n\\nThe product {product.material_description} (Code: {product.code}) has a shelf life of {product.shelf_life_remaining} days remaining. Please take necessary action."
        mail.send(msg)
        print(f"Alert email sent to {user_email} for product {product.code}.")

@app.route('/send-test-email')
def send_test_email():
    print("MAIL_USERNAME:", os.getenv('MAIL_USERNAME'))  # Debugging line
    print("MAIL_PASSWORD:", os.getenv('MAIL_PASSWORD'))  # Debugging line
    msg = Message('Test Email', 
              recipients=['anoushazaidi432@gmail.com'],  # Specify the recipient's email address
              sender=os.getenv('MAIL_USERNAME'))
    msg.body = 'This is a test email sent from Flask.'
    mail.send(msg)
    return 'Email sent to anoushazaidi432@gmail.com!'

# Admin setup
admin = Admin(app, name='Inventory Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(MaterialDescription, db.session))
admin.add_view(ModelView(Issuance, db.session))
admin.add_view(ModelView(User, db.session))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('signin.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
        else:
            # Use pbkdf2:sha256 for password hashing
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, username=username, password=hashed_password, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful, please login', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/get_material_details/<material_name>')
@login_required
def get_material_details(material_name):
    material = db.session.query(MaterialDescription).filter_by(name=material_name).first()
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    products = db.session.query(Product).filter_by(material_description=material.name).all()
    lots = db.session.query(Product.lot_number).filter_by(material_description=material.name).distinct().all()
    
    material_details = {
        'products': len(products),
        'lots': len(lots),
        'details': [{
            'lot_number': product.lot_number,
            'receiving_date': product.receiving_date.strftime('%Y-%m-%d'),
            'quantity': product.receiving_stock
        } for product in products]
    }

    return jsonify(material_details)
@app.route('/material/<string:code>', methods=['GET'])
@login_required
def material_details(code):
    material = MaterialDescription.query.filter_by(code=code).first()
    if material:
        products = Product.query.filter_by(code=code).all()
        lots = set([product.lot_number for product in products])
        total_qty = sum([product.receiving_stock for product in products])
        remaining_qty = sum([product.remaining_stock for product in products])
        
        data = {
            'material_code': material.code,
            'description': material.material_description,
            'lots': len(lots),
            'total_qty': total_qty,
            'remaining_qty': remaining_qty,
            'products': products
        }
        return render_template('material_details.html', data=data)
    else:
        return "Material not found", 404



@app.route('/', methods=['GET'])
@login_required
def dashboard():
    search_query = request.args.get('search_query', '').strip()
    sort_order = request.args.get('sort_order', 'oldest_to_newest')

    query = db.session.query(Product)

    if search_query:
        query = query.filter(
            (Product.po_number.ilike(f'%{search_query}%')) |
            (Product.code.ilike(f'%{search_query}%')) |
            (Product.md_number.ilike(f'%{search_query}%'))
        )

    if sort_order == 'newest_to_oldest':
        query = query.order_by(Product.receiving_date.desc())
    else:
        query = query.order_by(Product.receiving_date.asc())

    products = query.filter(Product.remaining_stock > 0).all()
    materials = MaterialDescription.query.all()

    critical_products = [p for p in products if p.shelf_life_remaining < 15]
    other_products = [p for p in products if p.shelf_life_remaining >= 15]

    sorted_products = critical_products + other_products
    return render_template('dashboard.html', products=sorted_products, materials=materials, search_query=search_query)


@app.route('/get_material/<code>', methods=['GET'])
@login_required
def get_material(code):
    material = MaterialDescription.query.filter_by(code=code).first()
    if material:
        return jsonify({
            'material_description': material.material_description,
            'shelf_life': material.shelf_life,
            'u_o_m': material.u_o_m
        })
    return jsonify({})


@app.route('/add-receiving', methods=['POST'])
@login_required
def add_receiving():
    code = request.form['code']
    material_description = request.form['material_description']
    po_number = request.form['po_number']
    md_number = request.form['md_number']
    store_name = request.form['store_name']
    vendor_name = request.form['vendor_name']
    receiving_date_str = request.form['receiving_date']
    receiving_stock = int(request.form['receiving_stock'])
    shelf_life = int(request.form['shelf_life'])

    # Convert string to datetime
    receiving_date = datetime.strptime(receiving_date_str, '%Y-%m-%d')

    # Fetch the highest lot number for the given code
    last_product = Product.query.filter_by(code=code).order_by(Product.lot_number.desc()).first()
    lot_number = last_product.lot_number + 1 if last_product else 1

    # Calculate expiry date, aging days, and shelf life remaining
    expiry_date = receiving_date + timedelta(days=shelf_life)
    today = datetime.today()
    aging_days = max(0, (today - receiving_date).days)
    shelf_life_remaining = max(0, (expiry_date - today).days)
   
    # Create a new Product record
    new_product = Product(
        material_description=material_description,
        code=code,
        po_number=po_number,
        md_number=md_number,
        store_name=store_name,
        vendor_name=vendor_name,
        receiving_date=receiving_date,
        receiving_stock=receiving_stock,
        shelf_life=shelf_life,
        lot_number=lot_number,
        expiry_date=expiry_date,
        aging_days=aging_days,
        shelf_life_remaining=shelf_life_remaining,
        remaining_stock=receiving_stock  # Initialize remaining stock
    )
    barcode_path = generate_barcode_for_product(po_number=new_product.po_number, code=new_product.code, md_number=new_product.md_number)
    new_product.barcode_path = barcode_path

    db.session.add(new_product)
    
    db.session.commit()
    
    send_shelf_life_alert(new_product, current_user.email)

    
    flash('Product added successfully!')
    return redirect(url_for('dashboard'))




@app.route('/po_history')
@login_required
def po_history():
    po_groups = db.session.query(
        Product.po_number,
        db.func.count(Product.id).label('product_count'),
        db.func.group_concat(Product.material_description).label('materials'),
        db.func.group_concat(Product.receiving_date).label('receiving_dates'),
        db.func.group_concat(Product.receiving_stock).label('quantities'),
        db.func.sum(Product.receiving_stock).label('total_quantity')
    ).group_by(Product.po_number).all()

    return render_template('po_history.html', po_groups=po_groups)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        # Update product details
        product.material_description = request.form['material_description']
        product.receiving_stock = int(request.form['receiving_stock'])
        product.remaining_stock = product.receiving_stock  # Reset remaining stock
        product.shelf_life = int(request.form['shelf_life'])
        product.po_number = request.form['po_number']
        product.md_number = request.form['md_number']
        product.store_name = request.form['store_name']
        product.vendor_name = request.form['vendor_name']
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    
    return redirect(url_for('dashboard'))

@app.route('/issue_product', methods=['POST'])
def issue_product():
    product_id = request.form.get('product_id')
    issue_qty = float(request.form.get('issue_qty'))
    
    if not product_id:
        return jsonify({"error": "Product ID is required."}), 400
    
    # Fetch the product using the ID
    product = Product.query.get_or_404(product_id)
    
    if product.remaining_stock is None:
        product.remaining_stock = product.receiving_stock  # Initialize if None
    
    if issue_qty > product.remaining_stock:
        return jsonify({"error": "Issue quantity exceeds remaining stock."}), 400

    # Create issuance record
    issuance = Issuance(
        material_id=product.id,
        code=product.code,
        issue_quantity=issue_qty,
        issue_date=datetime.utcnow()
    )
    db.session.add(issuance)

    # Update product stock
    product.remaining_stock -= issue_qty
    product.total_issuances += issue_qty
    product.last_issuance_date = datetime.utcnow()
    
    if product.remaining_stock <= 0:
        db.session.delete(product)

    db.session.commit()
    flash('Product issued successfully!')
    return redirect(url_for('dashboard'))


@app.route('/all-products')
@login_required
def all_products():
    products = Product.query.all()
    return render_template('all_products.html', products=products)

@app.route('/bulk-issuance', methods=['GET', 'POST'])
def bulk_issuance():
    if request.method == 'POST':
        # Logic for bulk issuance
        return redirect(url_for('dashboard'))
    return render_template('bulk_issuance.html')

@app.route('/issuance_history')
@login_required
def issuance_history():
    issuance_records = Issuance.query.order_by(Issuance.issue_date.desc()).all()
    return render_template('issuance_history.html', issuance_records=issuance_records)



@app.route('/dashboardv2')
def dashboardv2():
    barcode_data = request.args.get('barcode')
    if barcode_data:
        try:
            po_number, material_code, md_number = barcode_data.split('|')
            print(f"Querying with PO Number: {po_number}, Code: {material_code}, MD Number: {md_number}")

            product = Product.query.filter_by(po_number=po_number, code=material_code, md_number=md_number).first()

            if product:
                return render_template('brdashboard.html', product=product)
            else:
                print(f"Product not found for PO Number: {po_number}, Code: {material_code}, MD Number: {md_number}")
                return "Product not found", 404
        except ValueError:
            return "Invalid barcode data format", 400
    return "Invalid request", 400



@app.route('/issued', methods=['POST'])
def issued_product():
    code = request.form.get('code')
    po_number = request.form.get('po_number')
    md_number = request.form.get('md_number')
    issue_quantity = int(request.form.get('issue_quantity'))

    # Query the product to be issued
    product_to_issue = Product.query.filter_by(code=code, po_number=po_number, md_number=md_number).first()
    
    if product_to_issue:
        
        current_shelf_life = product_to_issue.shelf_life_remaining
        older_products = Product.query.filter(
            Product.code == code,
            Product.shelf_life_remaining < current_shelf_life
        ).all()
        
        if older_products:
            flash('OLDER PRODUCTS AVAILABLE, CAN NOT DISPATCH', 'danger')
            return redirect(url_for('dashboardv2') + f"?barcode={po_number}|{code}|{md_number}")

        else:
        # Check if remaining_stock is enough for the issue
            if product_to_issue.remaining_stock >= issue_quantity:
                # Decrement the remaining_stock
                product_to_issue.remaining_stock -= issue_quantity
                product_to_issue.issuance = True
                db.session.commit()
                flash('Product issued successfully', 'success')
            else:
                flash('Insufficient quantity available', 'danger')
    else:
        flash('Product not found', 'danger')
         # Create issuance record
    issuance = Issuance(
        material_id=product_to_issue.id,
        code=product_to_issue.code,
        issue_quantity=issue_quantity,
        issue_date=datetime.utcnow()
    )
    db.session.add(issuance)
    if product_to_issue.remaining_stock <= 0:
        db.session.delete(product_to_issue)
        
    product_to_issue.total_issuances += issue_quantity
    product_to_issue.last_issuance_date = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('dashboard') + f"?barcode={po_number}|{code}|{md_number}")


import os

def generate_barcode_for_product(po_number, code, md_number):
    try:
        # Ensure the directory exists
        barcode_dir = 'static/barcodes'
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        # Create a barcode object
        code128 = barcode.get_barcode_class('code128')
        barcode_data = f"{po_number}|{code}|{md_number}"  # Encode PO number and material code
        barcode_instance = code128(barcode_data, writer=ImageWriter())

        # Save the barcode image
        filename = os.path.join(barcode_dir, f'{md_number}.png')

        # Normalize the path to use forward slashes
        filename = filename.replace("\\", "/")

        barcode_instance.save(filename)

        print(f'Barcode for {code} saved to {filename}')
        return filename  # Return the normalized barcode path
    except Exception as e:
        print(f'Failed to generate barcode for {code}: {e}')
        return None



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)