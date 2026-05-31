from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        database=os.getenv("DB_NAME", "devops_db"),
        user=os.getenv("DB_USER", "devops_user"),
        password=os.getenv("DB_PASSWORD", "devops_pass"),
        port=os.getenv("DB_PORT", "5432"),
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price INTEGER NOT NULL
        );
    """)

    cur.execute("SELECT COUNT(*) FROM products;")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
            INSERT INTO products (name, price)
            VALUES
            ('Laptop', 50000),
            ('Phone', 25000),
            ('Headphones', 3000);
        """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    return "Real-Time DevOps E-Commerce API"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/db")
def db_check():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"database": "connected", "version": version})


@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": row[0], "name": row[1], "price": row[2]} for row in rows])


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products WHERE id = %s;", (product_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify({"id": row[0], "name": row[1], "price": row[2]})


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data["name"]
    price = data["price"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;",
        (name, price),
    )
    product_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return (
        jsonify(
            {"message": "product added", "id": product_id, "name": name, "price": price}
        ),
        201,
    )


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    name = data["name"]
    price = data["price"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING id;",
        (name, price, product_id),
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify(
        {"message": "product updated", "id": product_id, "name": name, "price": price}
    )


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = %s RETURNING id;", (product_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify({"message": "product deleted", "id": product_id})


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)  # nosec B104