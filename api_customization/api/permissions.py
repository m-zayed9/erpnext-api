@frappe.whitelist()
def get_mobile_permissions(user):
    user_doc = frappe.get_doc("User", user)
    roles = [role.role for role in user_doc.roles]

    if "mobile_access" not in roles:
        return {"error": "Unauthorized"}

    # Define user-specific permissions
    permissions = {
        "sales_invoice": "read",
        "quotation": "write"
    }

    return permissions
