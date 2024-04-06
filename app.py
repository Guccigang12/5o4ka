from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
db = SQLAlchemy(app)

employee_product_association = db.Table(
    "employee_product",
    db.Column("employee_id", db.Integer, db.ForeignKey("employee.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"))
)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship("Product",
                               secondary=employee_product_association,
                               backref="employees")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form["name"]
    new_employee = Employee(name=name)
    db.session.add(new_employee)
    db.session.commit()
    return f"Работник {new_employee.name} устроен"


@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    new_product = Product(name=name)
    db.session.add(new_product)
    db.session.commit()
    return f"Продукт {new_product.name} создан"


@app.route("/assign_employee_product", methods=["POST"])  # post request always in json
def assign_employee_product():
    employee_id = request.form["employee_id"]
    product_id = request.form["product_id"]
    employee = Employee.query.get(employee_id)
    product = Product.query.get(product_id)
    employee.products.append(product)
    db.session.commit()
    return f"Продавец {employee.name} привязал к себе {product.name}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
