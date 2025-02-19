import frappe


# @frappe.whitelist()
# def get_user_modules():
#     """Return modules the logged-in user has access to"""
#     user_roles = frappe.get_roles(frappe.session.user)

#     print("user_role",user_roles)
#     # Fetch allowed modules
#     modules = frappe.get_all(
#         "Module Def",
#         filters={"restrict_to_domain": ["in", user_roles]},
#         fields=["module_name", "app_name"],
#     )

#     return modules


@frappe.whitelist()
def get_user_modules():
    """Return modules the logged-in user has access to"""
    user_roles = frappe.get_roles(frappe.session.user)

    allowed_modules = frappe.db.sql(
        """
        SELECT DISTINCT md.module_name, md.app_name 
        FROM `tabModule Def` md
        LEFT JOIN `tabHas Role` hr ON md.module_name = hr.parent
        WHERE hr.role IN %(roles)s
    """,
        {"roles": user_roles},
        as_dict=True,
    )

    return allowed_modules


# @frappe.whitelist()
# def get_user_modules():
#     """Return all modules (for debugging)"""
#     modules = frappe.get_all("Module Def", fields=["module_name", "app_name"])
#     return modules
