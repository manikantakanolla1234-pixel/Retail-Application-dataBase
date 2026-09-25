from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

app.secret_key = "secret123"


# ==================================================
# MYSQL CONNECTION
# ==================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="23ka1a0530@92",
    database="online_Retil_Application"
)

cursor = db.cursor()

print("Database Connected Successfully")


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==================================================
# REGISTER PAGE
# ==================================================

@app.route("/register")
def register_page():
    return render_template("register.html")


# ==================================================
# REGISTER USER
# ==================================================

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]
    address = request.form["address"]

    sql = """
    INSERT INTO Users
    (
        Name,
        Email,
        Password,
        Phone,
        Address
    )
    VALUES
    (%s, %s, %s, %s, %s)
    """

    values = (
        name,
        email,
        password,
        phone,
        address
    )

    cursor.execute(sql, values)
    db.commit()

    return """
    <h2>Registration Successful ✅</h2>
    <a href="/login">Login Now</a>
    """


# ==================================================
# LOGIN PAGE
# ==================================================

@app.route("/login")
def login_page():
    return render_template("login.html")


# ==================================================
# LOGIN USER
# ==================================================

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    sql = """
    SELECT *
    FROM Users
    WHERE Email=%s
    AND Password=%s
    """

    cursor.execute(sql, (email, password))

    user = cursor.fetchone()

    if user:

        session["user_id"] = user[0]
        session["username"] = user[1]

        return redirect("/products")

    else:

        return """
        <h2>Invalid Email or Password ❌</h2>
        <a href="/login">Try Again</a>
        """


# ==================================================
# PRODUCTS
# ==================================================

@app.route("/products")
def products():

    cursor.execute("""
        SELECT
            ProductID,
            CategoryID,
            ProductName,
            Description,
            Price,
            Stock,
            Image
        FROM Products
    """)

    products = cursor.fetchall()

    return render_template(
        "products.html",
        products=products
    )


# ==================================================
# CATEGORY PRODUCTS
# ==================================================

@app.route("/category/<name>")
def category(name):

    sql = """
    SELECT
        ProductID,
        CategoryID,
        ProductName,
        Description,
        Price,
        Stock,
        Image
    FROM Products
    WHERE CategoryID =
    (
        SELECT CategoryID
        FROM Categories
        WHERE CategoryName=%s
    )
    """

    cursor.execute(sql, (name,))

    products = cursor.fetchall()

    return render_template(
        "products.html",
        products=products,
        category=name
    )


# ==================================================
# ADD TO CART
# ==================================================

@app.route("/cart/add/<int:id>")
def add_cart(id):

    if "user_id" not in session:

        return """
        <h2>Please Login First</h2>
        <a href="/login">Login</a>
        """

    user_id = session["user_id"]

    cursor.execute(
        """
        SELECT *
        FROM Cart
        WHERE UserID=%s
        AND ProductID=%s
        """,
        (user_id, id)
    )

    item = cursor.fetchone()

    if item:

        cursor.execute(
            """
            UPDATE Cart
            SET Quantity=Quantity+1
            WHERE UserID=%s
            AND ProductID=%s
            """,
            (user_id, id)
        )

    else:

        cursor.execute(
            """
            INSERT INTO Cart
            (UserID, ProductID, Quantity)
            VALUES(%s, %s, 1)
            """,
            (user_id, id)
        )

    db.commit()

    return redirect("/cart")


# ==================================================
# VIEW CART
# ==================================================

@app.route("/cart")
def view_cart():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    sql = """
    SELECT
        Cart.CartID,
        Products.ProductName,
        Products.Price,
        Cart.Quantity
    FROM Cart
    JOIN Products
        ON Cart.ProductID=Products.ProductID
    WHERE Cart.UserID=%s
    """

    cursor.execute(sql, (user_id,))

    cart = cursor.fetchall()

    total = 0

    for item in cart:
        total += item[2] * item[3]

    return render_template(
        "cart.html",
        cart=cart,
        total=total
    )


# ==================================================
# REMOVE CART ITEM
# ==================================================

@app.route("/cart/remove/<int:id>")
def remove_cart(id):

    cursor.execute(
        """
        DELETE FROM Cart
        WHERE CartID=%s
        """,
        (id,)
    )

    db.commit()

    return redirect("/cart")


# ==================================================
# CUSTOMER MANAGEMENT
# ==================================================

@app.route("/customers")
def customers():

    search = request.args.get("search", "").strip()

    if search:

        sql = """
        SELECT
            CustomerID,
            FullName,
            Phone,
            Email,
            Address
        FROM Customers
        WHERE FullName LIKE %s
           OR Phone LIKE %s
           OR Email LIKE %s
        ORDER BY CustomerID DESC
        """

        value = "%" + search + "%"

        cursor.execute(
            sql,
            (value, value, value)
        )

    else:

        cursor.execute("""
        SELECT
            CustomerID,
            FullName,
            Phone,
            Email,
            Address
        FROM Customers
        ORDER BY CustomerID DESC
        """)

    customers = cursor.fetchall()

    return render_template(
        "customers.html",
        customers=customers,
        search=search
    )


# ==================================================
# CHECKOUT
# ==================================================

@app.route("/checkout")
def checkout():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("""
        SELECT
            Cart.CartID,
            Products.ProductID,
            Products.ProductName,
            Products.Price,
            Cart.Quantity
        FROM Cart
        JOIN Products
            ON Cart.ProductID = Products.ProductID
        WHERE Cart.UserID=%s
    """, (user_id,))

    cart = cursor.fetchall()

    if not cart:
        return """
        <h2>Your cart is empty ❌</h2>
        <a href="/products">Continue Shopping</a>
        """

    total = 0

    for item in cart:
        total += item[3] * item[4]

    return render_template(
        "checkout.html",
        cart=cart,
        total=total
    )


# ==================================================
# PLACE ORDER
# ==================================================

@app.route("/place_order", methods=["POST"])
def place_order():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # ----------------------------------------------
    # GET LOGGED-IN USER
    # ----------------------------------------------

    cursor.execute("""
        SELECT
            Name,
            Email,
            Password,
            Phone,
            Address
        FROM Users
        WHERE UserID=%s
    """, (user_id,))

    user = cursor.fetchone()

    if not user:
        return redirect("/login")

    name = user[0]
    email = user[1]
    password = user[2]
    phone = user[3]
    address = user[4]

    # ----------------------------------------------
    # FIND CUSTOMER
    # ----------------------------------------------

    cursor.execute("""
        SELECT CustomerID
        FROM Customers
        WHERE Email=%s
    """, (email,))

    customer = cursor.fetchone()

    # ----------------------------------------------
    # CREATE CUSTOMER IF NOT EXISTS
    # ----------------------------------------------

    if not customer:

        cursor.execute("""
            INSERT INTO Customers
            (
                FullName,
                Email,
                Password,
                Phone,
                Address
            )
            VALUES
            (%s, %s, %s, %s, %s)
        """, (
            name,
            email,
            password,
            phone,
            address
        ))

        db.commit()

        customer_id = cursor.lastrowid

    else:

        customer_id = customer[0]

    # ----------------------------------------------
    # GET CART
    # ----------------------------------------------

    cursor.execute("""
        SELECT
            Cart.CartID,
            Cart.ProductID,
            Products.ProductName,
            Products.Price,
            Cart.Quantity
        FROM Cart
        JOIN Products
            ON Cart.ProductID = Products.ProductID
        WHERE Cart.UserID=%s
    """, (user_id,))

    cart = cursor.fetchall()

    if not cart:
        return """
        <h2>Your cart is empty ❌</h2>
        <a href="/products">Continue Shopping</a>
        """

    # ----------------------------------------------
    # CALCULATE TOTAL
    # ----------------------------------------------

    total = 0

    for item in cart:

        price = item[3]
        quantity = item[4]

        total += price * quantity

    # ----------------------------------------------
    # PAYMENT METHOD
    # ----------------------------------------------

    payment_method = request.form.get(
        "payment_method",
        "Cash on Delivery"
    )

    # ----------------------------------------------
    # CREATE ORDER
    # ----------------------------------------------

    cursor.execute("""
        INSERT INTO Orders
        (
            CustomerID,
            TotalAmount
        )
        VALUES
        (%s, %s)
    """, (
        customer_id,
        total
    ))

    db.commit()

    order_id = cursor.lastrowid

    # ----------------------------------------------
    # CREATE ORDER DETAILS
    # ----------------------------------------------

    for item in cart:

        product_id = item[1]
        price = item[3]
        quantity = item[4]

        cursor.execute("""
            INSERT INTO OrderDetails
            (
                OrderID,
                ProductID,
                Quantity,
                Price
            )
            VALUES
            (%s, %s, %s, %s)
        """, (
            order_id,
            product_id,
            quantity,
            price
        ))

    # ----------------------------------------------
    # CREATE PAYMENT
    # ----------------------------------------------

    cursor.execute("""
        INSERT INTO Payments
        (
            OrderID,
            Amount,
            PaymentMethod
        )
        VALUES
        (%s, %s, %s)
    """, (
        order_id,
        total,
        payment_method
    ))

    # ----------------------------------------------
    # UPDATE PRODUCT STOCK
    # ----------------------------------------------

    for item in cart:

        product_id = item[1]
        quantity = item[4]

        cursor.execute("""
            UPDATE Products
            SET Stock = Stock - %s
            WHERE ProductID=%s
        """, (
            quantity,
            product_id
        ))

    # ----------------------------------------------
    # CLEAR CART
    # ----------------------------------------------

    cursor.execute("""
        DELETE FROM Cart
        WHERE UserID=%s
    """, (user_id,))

    db.commit()

    # ----------------------------------------------
    # SUCCESS PAGE
    # ----------------------------------------------

    return render_template(
        "order_success.html",
        order_id=order_id,
        total=total,
        payment_method=payment_method
    )

# ==================================================
# ORDER HISTORY
# ==================================================

@app.route("/orders")
def orders():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Get logged-in user's email
    cursor.execute("""
        SELECT Email
        FROM Users
        WHERE UserID=%s
    """, (user_id,))

    user = cursor.fetchone()

    if not user:
        return redirect("/login")

    email = user[0]

    # Find customer
    cursor.execute("""
        SELECT CustomerID
        FROM Customers
        WHERE Email=%s
    """, (email,))

    customer = cursor.fetchone()

    if not customer:
        return render_template(
            "orders.html",
            orders=[]
        )

    customer_id = customer[0]

    # Get orders
    cursor.execute("""
        SELECT
            Orders.OrderID,
            Orders.TotalAmount,
            Payments.PaymentMethod
        FROM Orders
        LEFT JOIN Payments
            ON Orders.OrderID = Payments.OrderID
        WHERE Orders.CustomerID=%s
        ORDER BY Orders.OrderID DESC
    """, (customer_id,))

    orders = cursor.fetchall()

    return render_template(
        "orders.html",
        orders=orders
    )
# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==================================================
# RUN APP
# ==================================================

print("CUSTOMER ROUTE LOADED")
print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)