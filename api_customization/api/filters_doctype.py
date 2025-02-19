# import frappe


# @frappe.whitelist()
# def search_records(doctype, query=None, filters=None):
#     """
#     Search and filter records in a given DocType dynamically, ensuring exactly four fields are returned.

#     :param doctype: The name of the ERPNext DocType (e.g., "Sales Invoice").
#     :param query: Search query string (e.g., invoice number, customer name).
#     :param filters: JSON object with filters (e.g., {"status": "Paid", "min_price": 100, "max_price": 500}).
#     :return: JSON with records and available filter values.
#     """
#     if not doctype:
#         return {"error": "Doctype is required"}

#     filters_dict = frappe.parse_json(filters) if filters else {}
#     search_conditions = []
#     or_conditions = []

#     # Fetch metadata to get available fields dynamically
#     meta = frappe.get_meta(doctype)
#     all_fields = [
#         df.fieldname
#         for df in meta.fields
#         if df.fieldtype not in ["Section Break", "Column Break"]
#     ]

#     # Ensure four fields are returned: prioritize common fields, then fill with others if needed
#     default_fields = ["name"]  # Always include the primary key
#     common_fields = ["status", "customer", "supplier", "total", "amount", "grand_total"]

#     # Select fields based on availability
#     selected_fields = default_fields + [
#         field for field in common_fields if field in all_fields
#     ]

#     # If selected fields are less than four, fill with any other available fields
#     while len(selected_fields) < 4 and len(selected_fields) < len(all_fields):
#         next_field = next((f for f in all_fields if f not in selected_fields), None)
#         if next_field:
#             selected_fields.append(next_field)

#     # Apply search query (OR condition)
#     if query:
#         or_conditions = [
#             [field, "like", f"%{query}%"] for field in selected_fields[:2]
#         ]  # Use first two fields for search

#     # Apply filters dynamically
#     all_conditions = []
#     for key, value in filters_dict.items():
#         if key in ["min_price", "max_price"] and "total" in all_fields:
#             comparator = ">=" if key == "min_price" else "<="
#             all_conditions.append(["total", comparator, float(value)])
#         elif key in all_fields:
#             all_conditions.append([key, "=", value])

#     # Fetch records with exactly four fields
#     records = frappe.get_all(
#         doctype,
#         or_filters=or_conditions if or_conditions else None,
#         filters=all_conditions if all_conditions else None,
#         fields=selected_fields[:4],
#         limit_page_length=50,
#     )

#     # Fetch available filter values
#     available_filters = {}
#     for field in ["status", "customer", "supplier"]:
#         if field in all_fields:
#             available_filters[field + "s"] = [
#                 x[field]
#                 for x in frappe.get_all(doctype, fields=[field], distinct=True)
#                 if x[field]
#             ]

#     # Get min & max price if applicable
#     if "total" in all_fields:
#         min_price = frappe.db.sql(f"SELECT MIN(total) FROM `tab{doctype}`")[0][0] or 0
#         max_price = frappe.db.sql(f"SELECT MAX(total) FROM `tab{doctype}`")[0][0] or 0
#         available_filters["price_range"] = {"min": min_price, "max": max_price}

#     return {
#         "records": records,
#         "filters": available_filters,
#     }

# for the access user

import frappe


@frappe.whitelist()
def search_records(doctype, query=None, filters=None):
    """
    Search and filter records in a given DocType dynamically, ensuring exactly four fields are returned
    and restricting access based on the current user's permissions.

    :param doctype: The name of the ERPNext DocType (e.g., "Sales Invoice").
    :param query: Search query string (e.g., invoice number, customer name).
    :param filters: JSON object with filters (e.g., {"status": "Paid", "min_price": 100, "max_price": 500}).
    :return: JSON with records and available filter values.
    """
    if not doctype:
        return {"error": "Doctype is required"}

    # Check if the current user has read permission for the DocType
    if not frappe.has_permission(doctype=doctype, ptype="read"):
        return {"error": f"You do not have permission to access {doctype}"}

    filters_dict = frappe.parse_json(filters) if filters else {}
    or_conditions = []

    # Fetch metadata to get available fields dynamically
    meta = frappe.get_meta(doctype)
    all_fields = [
        df.fieldname
        for df in meta.fields
        if df.fieldtype not in ["Section Break", "Column Break"]
    ]

    # Ensure four fields are returned: prioritize common fields, then fill with others if needed
    default_fields = ["name"]  # Always include the primary key
    common_fields = ["status", "customer", "supplier", "total", "amount", "grand_total"]

    # Select fields based on availability
    selected_fields = default_fields + [
        field for field in common_fields if field in all_fields
    ]

    # If selected fields are less than four, fill with any other available fields
    while len(selected_fields) < 4 and len(selected_fields) < len(all_fields):
        next_field = next((f for f in all_fields if f not in selected_fields), None)
        if next_field:
            selected_fields.append(next_field)

    # Apply search query (OR condition)
    if query:
        or_conditions = [
            [field, "like", f"%{query}%"] for field in selected_fields[:2]
        ]  # Use first two fields for search

    # Apply filters dynamically
    all_conditions = []
    for key, value in filters_dict.items():
        if key in ["min_price", "max_price"] and "total" in all_fields:
            comparator = ">=" if key == "min_price" else "<="
            all_conditions.append(["total", comparator, float(value)])
        elif key in all_fields:
            all_conditions.append([key, "=", value])

    # Fetch records with exactly four fields
    records = frappe.get_all(
        doctype,
        or_filters=or_conditions if or_conditions else None,
        filters=all_conditions if all_conditions else None,
        fields=selected_fields[:4],
        limit_page_length=50,
    )

    # Fetch available filter values based on accessible data
    available_filters = {}
    for field in ["status", "customer", "supplier"]:
        if field in all_fields and frappe.has_permission(doctype=doctype, ptype="read"):
            available_filters[field + "s"] = [
                x[field]
                for x in frappe.get_all(doctype, fields=[field], distinct=True)
                if x[field]
            ]

    # Get min & max price if applicable
    if "total" in all_fields:
        min_price = frappe.db.sql(f"SELECT MIN(total) FROM `tab{doctype}`")[0][0] or 0
        max_price = frappe.db.sql(f"SELECT MAX(total) FROM `tab{doctype}`")[0][0] or 0
        available_filters["price_range"] = {"min": min_price, "max": max_price}

    return {
        "records": records,
        "filters": available_filters,
    }
