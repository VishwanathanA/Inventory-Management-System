from flask import Flask, render_template, request, redirect, url_for, flash
from modules import db, Product, Location, ProductMovement

app = Flask(__name__)

# Use your online Filess.io database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Inventory_solidtrack:866f3c71dd935f9863eb9f2814996f90c5c13c4c@lq6mtr.h.filess.io:61002/Inventory_solidtrack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "dev-key"

# Initialize the database with Flask app
db.init_app(app)

# Home page
@app.route('/')
def index():
    return redirect(url_for('view_products'))

# Product routes
@app.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('product/list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form.get('product_id', '').strip()
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Product name is required!', 'error')
            return render_template('product/form.html')
        
        # Check if custom ID already exists
        if product_id and Product.query.get(product_id):
            flash('Product ID already exists!', 'error')
            return render_template('product/form.html')
        
        # Create product with or without custom ID
        if product_id:
            product = Product(product_id=product_id, name=name, description=description)
        else:
            product = Product(name=name, description=description)
            
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('view_products'))
    
    return render_template('product/form.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Product name is required!', 'error')
            return render_template('product/form.html', product=product)
        
        product.name = name
        product.description = description
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('view_products'))
    
    return render_template('product/form.html', product=product)

@app.route('/products/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product has movements
    movements = ProductMovement.query.filter_by(product_id=product_id).first()
    if movements:
        flash('Cannot delete product with existing movements!', 'error')
        return redirect(url_for('view_products'))
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('view_products'))

# Location routes
@app.route('/locations')
def view_locations():
    locations = Location.query.all()
    return render_template('location/list.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form.get('location_id', '').strip()
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Location name is required!', 'error')
            return render_template('location/form.html')
        
        # Check if custom ID already exists
        if location_id and Location.query.get(location_id):
            flash('Location ID already exists!', 'error')
            return render_template('location/form.html')
        
        # Create location with or without custom ID
        if location_id:
            location = Location(location_id=location_id, name=name, description=description)
        else:
            location = Location(name=name, description=description)
            
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('view_locations'))
    
    return render_template('location/form.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Location name is required!', 'error')
            return render_template('location/form.html', location=location)
        
        location.name = name
        location.description = description
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('view_locations'))
    
    return render_template('location/form.html', location=location)

@app.route('/locations/delete/<location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    # Check if location has movements
    movements_from = ProductMovement.query.filter_by(from_location=location_id).first()
    movements_to = ProductMovement.query.filter_by(to_location=location_id).first()
    
    if movements_from or movements_to:
        flash('Cannot delete location with existing movements!', 'error')
        return redirect(url_for('view_locations'))
    
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('view_locations'))

# Movement routes - FIXED for frontend compatibility
@app.route('/movements')
def view_movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    
    # Prepare movement data with product and location names for frontend
    movement_data = []
    for movement in movements:
        product = Product.query.get(movement.product_id)
        from_loc = Location.query.get(movement.from_location) if movement.from_location else None
        to_loc = Location.query.get(movement.to_location) if movement.to_location else None
        
        movement_data.append({
            'movement_id': movement.movement_id,
            'timestamp': movement.timestamp,
            'product': product,
            'from_loc': from_loc,
            'to_loc': to_loc,
            'quantity': movement.quantity,
            'product_id': movement.product_id,
            'from_location': movement.from_location,
            'to_location': movement.to_location
        })
    
    return render_template('movement/list.html', movements=movement_data)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    products = Product.query.all()
    locations = Location.query.all()
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        quantity = int(request.form['quantity'])
        
        # Validation
        if not from_location and not to_location:
            flash('At least one location (From or To) must be specified!', 'error')
            return render_template('movement/form.html', products=products, locations=locations)
        
        if from_location == to_location:
            flash('From and To locations cannot be the same!', 'error')
            return render_template('movement/form.html', products=products, locations=locations)
        
        if quantity <= 0:
            flash('Quantity must be greater than 0!', 'error')
            return render_template('movement/form.html', products=products, locations=locations)
        
        # Check stock availability for outgoing movements
        if from_location:
            # Calculate current stock using SQL functions for accuracy
            stock_in = db.session.query(func.coalesce(func.sum(ProductMovement.quantity), 0)).filter(
                ProductMovement.product_id == product_id,
                ProductMovement.to_location == from_location
            ).scalar()
            
            stock_out = db.session.query(func.coalesce(func.sum(ProductMovement.quantity), 0)).filter(
                ProductMovement.product_id == product_id,
                ProductMovement.from_location == from_location
            ).scalar()
            
            current_stock = stock_in - stock_out
            
            if current_stock < quantity:
                flash(f'Insufficient stock! Only {current_stock} units available in source location.', 'error')
                return render_template('movement/form.html', products=products, locations=locations)
        
        movement = ProductMovement(
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            quantity=quantity
        )
        
        db.session.add(movement)
        db.session.commit()
        flash('Movement recorded successfully!', 'success')
        return redirect(url_for('view_movements'))
    
    return render_template('movement/form.html', products=products, locations=locations)

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    products = Product.query.all()
    locations = Location.query.all()
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        quantity = int(request.form['quantity'])
        
        # Validation
        if not from_location and not to_location:
            flash('At least one location (From or To) must be specified!', 'error')
            return render_template('movement/form.html', movement=movement, products=products, locations=locations)
        
        if from_location == to_location:
            flash('From and To locations cannot be the same!', 'error')
            return render_template('movement/form.html', movement=movement, products=products, locations=locations)
        
        if quantity <= 0:
            flash('Quantity must be greater than 0!', 'error')
            return render_template('movement/form.html', movement=movement, products=products, locations=locations)
        
        movement.product_id = product_id
        movement.from_location = from_location
        movement.to_location = to_location
        movement.quantity = quantity
        
        db.session.commit()
        flash('Movement updated successfully!', 'success')
        return redirect(url_for('view_movements'))
    
    return render_template('movement/form.html', movement=movement, products=products, locations=locations)

@app.route('/movements/delete/<movement_id>', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Movement deleted successfully!', 'success')
    return redirect(url_for('view_movements'))

# --------------------------
# Helper function to calculate stock
# --------------------------
def calculate_stock(product_id, location_id):
    """
    Calculate current stock of a product at a specific location.
    Stock = total received - total sent
    """
    stock_in = db.session.query(func.coalesce(func.sum(ProductMovement.quantity), 0)).filter(
        ProductMovement.product_id == product_id,
        ProductMovement.to_location == location_id
    ).scalar()
    
    stock_out = db.session.query(func.coalesce(func.sum(ProductMovement.quantity), 0)).filter(
        ProductMovement.product_id == product_id,
        ProductMovement.from_location == location_id
    ).scalar()
    
    return stock_in - stock_out

# Balance report
@app.route('/report')
def report():
    products = Product.query.all()
    locations = Location.query.all()
    balances = []

    for product in products:
        for location in locations:
            qty = calculate_stock(product.product_id, location.location_id)
            balances.append({
                'product_name': product.name,
                'location_name': location.name,
                'quantity': qty
            })

    return render_template('report.html', balances=balances)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
