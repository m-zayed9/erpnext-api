import frappe

@frappe.whitelist()
def search_purchase_invoices(query=None, filters=None):
    """
    Search and filter Purchase Invoices.

    :param query: Search query string (e.g., invoice number or supplier name).
    :param filters: JSON object with filters (e.g., {"status": "Paid", "min_price": 100, "max_price": 500}).
    :return: JSON with records and available filter values.
    """
    doctype = "Purchase Invoice"

    # Initialize filters
    filters_dict = frappe.parse_json(filters) if filters else {}
    conditions = {}

    # Apply additional filters
    if filters_dict:
        if "status" in filters_dict:
            conditions["status"] = filters_dict["status"]
        if "supplier" in filters_dict:
            conditions["supplier"] = filters_dict["supplier"]
        if "min_price" in filters_dict:
            conditions["total"] = [">=", float(filters_dict["min_price"])]
        if "max_price" in filters_dict:
            conditions["total"] = ["<=", float(filters_dict["max_price"])]

    # Fetch records
    records = frappe.get_list(
        doctype,
        filters=conditions,
        fields=["name", "status", "supplier", "total"],
        or_filters=(
            [["name", "like", f"%{query}%"], ["supplier", "like", f"%{query}%"]]
            if query
            else None
        ),
        limit_page_length=50,  # Add limit to avoid fetching too many records
    )

    # Debugging

    # Fetch available filter values
    statuses = frappe.get_all(doctype, fields=["status"], distinct=True)
    suppliers = frappe.get_all(doctype, fields=["supplier"], distinct=True)

    # Get min & max price for UI sliders
    min_price = frappe.db.sql(f"SELECT MIN(total) FROM `tab{doctype}`")[0][0] or 0
    max_price = frappe.db.sql(f"SELECT MAX(total) FROM `tab{doctype}`")[0][0] or 0

    return {
        "records": records,
        "filters": {
            "statuses": [s["status"] for s in statuses if s["status"]],
            "suppliers": [c["supplier"] for c in suppliers if c["supplier"]],
            "price_range": {"min": min_price, "max": max_price},
        },
    }
