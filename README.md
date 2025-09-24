# Inventory Management System

A comprehensive Flask-based web application for managing inventory, tracking product movements across multiple locations, and generating balance reports.

## 📋 Overview

This Inventory Management System provides a complete solution for businesses to track their products across various locations. The application allows you to manage products, locations, and product movements while maintaining accurate stock levels through a robust tracking system.

## ✨ Features

### 🔧 Core Functionality
- **Product Management**: Add, edit, and delete products with unique identifiers
- **Location Management**: Manage multiple storage locations (warehouses, stores, etc.)
- **Movement Tracking**: Record product transfers between locations with timestamps
- **Stock Balance Reporting**: Real-time inventory balance across all locations
- **Data Validation**: Prevent invalid movements and ensure data integrity

### 🛡️ Business Logic
- **Stock Validation**: Prevents movements that would result in negative inventory
- **Dependency Checks**: Prevents deletion of products/locations with existing movements
- **Custom ID Support**: Option to use custom identifiers or auto-generated UUIDs
- **Audit Trail**: Complete history of all product movements with timestamps

## 🏗️ Project Structure

```
inventory-management-system/
├── app.py                 # Main Flask application
├── modules.py            # Database models (Product, Location, ProductMovement)
├── templates/            # HTML templates
│   ├── product/
│   │   ├── list.html     # Product listing
│   │   └── form.html     # Add/edit product form
│   ├── location/
│   │   ├── list.html     # Location listing
│   │   └── form.html     # Add/edit location form
│   ├── movement/
│   │   ├── list.html     # Movement history
│   │   └── form.html     # Add/edit movement form
│   └── report.html       # Balance report
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/VishwanathanA/Inventory-Management-System.git
cd inventory-management-system
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. Create a MySQL database named `inventory_db`
2. Update the database connection string in `app.py` if needed:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/inventory_db'
```

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📊 Database Models

### Product
- `product_id` (Primary Key): Unique identifier (UUID or custom)
- `name`: Product name (required)
- `description`: Product description

### Location
- `location_id` (Primary Key): Unique identifier (UUID or custom)
- `name`: Location name (required)
- `description`: Location description

### ProductMovement
- `movement_id` (Primary Key): Unique identifier (UUID)
- `timestamp`: Movement date and time (auto-generated)
- `product_id`: Reference to product (required)
- `from_location`: Source location (optional for incoming goods)
- `to_location`: Destination location (optional for outgoing goods)
- `quantity`: Number of units moved (required)

## 🎯 API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirects to products page |
| `/products` | GET | List all products |
| `/products/add` | GET, POST | Add new product |
| `/products/edit/<id>` | GET, POST | Edit existing product |
| `/products/delete/<id>` | POST | Delete product |
| `/locations` | GET | List all locations |
| `/locations/add` | GET, POST | Add new location |
| `/locations/edit/<id>` | GET, POST | Edit existing location |
| `/locations/delete/<id>` | POST | Delete location |
| `/movements` | GET | List all movements |
| `/movements/add` | GET, POST | Add new movement |
| `/movements/edit/<id>` | GET, POST | Edit existing movement |
| `/movements/delete/<id>` | POST | Delete movement |
| `/report` | GET | Generate balance report |

## 💡 Usage Examples

### Adding a Product
1. Navigate to Products page
2. Click "Add Product"
3. Enter product details (ID is optional - auto-generated if empty)
4. Save the product

### Recording a Movement
1. Go to Movements page
2. Click "Add Movement"
3. Select product, source/destination locations, and quantity
4. The system validates stock availability before recording

### Viewing Inventory Balance
1. Access the Balance Report from the navigation
2. View current stock levels for all products across all locations

## 🔒 Validation Rules

- **Product/Location Deletion**: Only allowed if no movements exist
- **Movement Validation**: 
  - At least one location (from or to) must be specified
  - From and to locations cannot be the same
  - Quantity must be positive
  - Sufficient stock must exist for outgoing movements
- **Unique IDs**: Custom IDs must be unique across products/locations

## 🛠️ Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Templating**: Jinja2
- **UUID Generation**: Python uuid module

## 📈 Stock Calculation Logic

The system calculates current stock using the formula:
```
Stock = Total Received - Total Sent
```

For each product at each location:
- **Stock In**: Sum of all movements where location is destination
- **Stock Out**: Sum of all movements where location is source

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL server is running
   - Check database credentials in app.py
   - Ensure database 'inventory_db' exists

2. **Module Import Errors**
   - Activate virtual environment
   - Run `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port in `app.run(port=5001)`
   - Kill existing process using port 5000

