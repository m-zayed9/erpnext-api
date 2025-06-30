import frappe
from frappe import _

@frappe.whitelist()
def get_user_modules():
    user = frappe.session.user

    # Load user's preferred language
    user_lang = frappe.db.get_value("User", user, "language") or frappe.local.lang

    # Set language for this request
    frappe.local.lang = user_lang

    # Fetch modules
    modules = frappe.get_all(
        "Module Def",
        fields=["name"]
    )

    # Get blocked modules
    blocked_modules = list(map(
        lambda i: i['module'],
        frappe.get_all(
            "Block Module",
            filters=[['parent', '=', user]],
            fields=["module"]
        )
    ))

    # Keep allowed modules
    allowed_modules = [
        module['name'] for module in modules
        if module['name'] not in blocked_modules
    ]

    # Translate module names
    translated_modules = [_(module_name) for module_name in allowed_modules]

    return translated_modules
