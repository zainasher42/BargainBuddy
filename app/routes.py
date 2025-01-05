from flask import render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Product

def init_routes(app):
    @app.route("/")
    def home():
        """Home Page: Displays product listings."""
        #products = Product.query.all()
        products = [
        {
            "name": "Product 1",
            "shop_name": "Shop 1",
            "price": "$1,999.00",
            "sales": "120 sales",
            "image_url": url_for('static', filename='images/button-icon-cart-plus-solid0.svg')
        },
        {
            "name": "Product 2",
            "shop_name": "Shop 2",
            "price": "$999.00",
            "sales": "85 sales",
            "image_url": url_for('static', filename='images/button-icon-cart-plus-solid0.svg')
        }
    ]
        return render_template("index.html", products=products)

    @app.route("/add-product", methods=["GET", "POST"])
    def add_product():
        """Add Product Page: Allows user to add new products."""
        if request.method == "POST":
            # Retrieve form data
            price = float(request.form["price"])
            inventory = int(request.form["inventory"])
            expiry_year = int(request.form["expiry_year"])
            max_discount = price * 0.15

            # Add product to the database
            new_product = Product(price=price, inventory=inventory, expiry_year=expiry_year,
                                  max_discount=max_discount)
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
