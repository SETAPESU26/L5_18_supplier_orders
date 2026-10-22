"""Purchase order tracker for a stores department."""
import logging
import sqlite3


def create_connection():
    """Create an in-memory database with an empty orders table."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, supplier TEXT, "
        "item TEXT, quantity INTEGER, received INTEGER)"
    )
    return conn


def place_order(conn, supplier, item, quantity):
    """Insert a new, not yet received order for a supplier."""
    conn.execute(
        "INSERT INTO orders (supplier, item, quantity, received) "
        "VALUES (?, ?, ?, 0)",
        (supplier, item, quantity),
    )


def mark_received(conn, order_id):
    """Mark the order with the given id as received."""
    conn.execute("UPDATE orders SET received = 1 WHERE id = ?", (order_id,))


def notify_warehouse(supplier):
    """Tell the warehouse about a delivery from the supplier."""
    print("notifying warehouse about " + supplier)


def cleanup(conn):
    """Delete all received orders."""
    try:
        conn.execute("DELETE FROM orders WHERE received = 1")
    except sqlite3.Error as err:
        logging.error("Cleanup failed: %s", err)


def pending_count(conn):
    """Return the number of orders not yet received."""
    row = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    ).fetchone()
    return row[0]


def main():
    """Run a short demonstration of the order tracker."""
    conn = create_connection()
    orders = [("Acme Steel", "rods", 40), ("Bolt Co", "bolts", 500)]
    order_total = 0
    for supplier, item, quantity in orders:
        place_order(conn, supplier, item, quantity)
        order_total += quantity
    mark_received(conn, 1)
    notify_warehouse("Acme")
    print(pending_count(conn), order_total)
    cleanup(conn)


if __name__ == "__main__":
    main()
