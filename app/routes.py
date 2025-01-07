from flask import render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Product
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def init_routes(app):
    def allowed_file(filename):
        """Check if the file has an allowed extension."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route("/")
    def home():
        """Home Page: Displays product listings."""
        products = Product.query.all()
        return render_template("index.html", products=products)

    @app.route("/add-product", methods=["GET", "POST"])
    def add_product():
        """Add Product Page: Allows user to add new products with images."""
        if request.method == "POST":
            # Retrieve form data
            title = request.form["title"]  # Retrieve the title
            price = float(request.form["price"])
            inventory = int(request.form["inventory"])
            expiry_year = int(request.form["expiry_year"])
            max_discount = price * 0.15
            discount = max_discount * 0.5  # Example initial discount

            # Handle file upload
            file = request.files.get("image")
            image_filename = None
            if file and allowed_file(file.filename):
                # Save the file securely
                image_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            elif file:
                flash("Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.", "error")
                return redirect(request.url)

            # Add product to the database
            if (price>0 and inventory>0 and expiry_year>=2025):
                new_product = Product(title=title, price=price, inventory=inventory, expiry_year=expiry_year,
                                    max_discount=max_discount, image_filename=image_filename)
                db.session.add(new_product)
                db.session.commit()
                flash('Product Successfully Added!', 'success')
            
            else:
                flash('Invalid Inputs', 'danger')

            return redirect(url_for("home"))
        return render_template("add_product.html")

    @app.route("/chat-bot", methods=["GET", "POST"])
    def chat_bot():
        """Bargaining Chat Bot Page."""
        if request.method == "POST":
            # Simulate bargaining logic
            offered_discount = float(request.form["offered_discount"])
            max_discount = float(request.form["max_discount"])
            response = "Accepted" if offered_discount <= max_discount else "Rejected"
            return jsonify({"response": response})
        return render_template("chat_bot.html")
    
    # Load the trained AI model
    price_model = tf.keras.models.load_model('./app/price_optimization_model.h5')

    # Load the scaler used during training (assume it's saved as a pickle file)
    import pickle
    with open('./app/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    @app.route('/product/<int:product_id>')
    def product_page(product_id):
        """Product Page: Display details and optimized pricing for a specific product."""
        product = Product.query.get_or_404(product_id)

        # Maximum discount calculation
        maximum_discount = float(product.price) * 0.15

        # Product features
        product_features = {
            'price': float(product.price),
            'Inventory': float(product.inventory),
            'Expiry Year': float(product.expiry_year),
            'Maximum Discount': maximum_discount
        }

        # Convert product features to a DataFrame
        product_df = pd.DataFrame([product_features])

        # Preprocess the features
        numerical_columns = ['price', 'Inventory', 'Maximum Discount', 'Expiry Year']
        product_df[numerical_columns] = scaler.transform(product_df[numerical_columns])

        # Load the training columns
        with open('./app/columns.pkl', 'rb') as f:
            training_columns = pickle.load(f)

        # Align columns with training data
        product_df = product_df.reindex(columns=training_columns, fill_value=0)

        # Predict the discount
        predicted_discount = price_model.predict(product_df)[0][0]

        # Ensure the predicted discount is viable
        if predicted_discount > maximum_discount:
            predicted_discount = maximum_discount
        elif predicted_discount < 0:
            predicted_discount = float(product.price) * 0.05  # Minimum discount (e.g., 5% of price)

        # Render the product page with the predicted discount
        return render_template('product.html', product=product, predicted_discount=int(predicted_discount))
