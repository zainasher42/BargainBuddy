from flask import render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Product

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
            new_product = Product(title=title, price=price, inventory=inventory, expiry_year=expiry_year,
                                max_discount=max_discount, image_filename=image_filename)
            db.session.add(new_product)
            db.session.commit()

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
