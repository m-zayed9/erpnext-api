
import frappe
from frappe import _


@frappe.whitelist(allow_guest=False)
def get_user_details(user_email):
    """Fetch user details by email."""
    try:
        user = frappe.get_doc("User", user_email)
        return {
            "email": user.email,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "username": user.username,
            "language": user.language,
            "time_zone": user.time_zone,
        }
    except frappe.DoesNotExistError:
        frappe.throw(_("User not found"), frappe.DoesNotExistError)


@frappe.whitelist(allow_guest=False)
def update_user_details(
    user_email,
    first_name=None,
    middle_name=None,
    last_name=None,
    language=None,
    time_zone=None,
):
    """Update user details"""
    try:
        user = frappe.get_doc("User", user_email)

        if first_name:
            user.first_name = first_name
        if middle_name:
            user.middle_name = middle_name
        if last_name:
            user.last_name = last_name
        if language:
            user.language = language
        if time_zone:
            user.time_zone = time_zone

        user.save()
        frappe.db.commit()
        user_data = {
            "email": user.email,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "username": user.username,
            "language": user.language,
            "time_zone": user.time_zone,
        }

        return {"message": "User updated successfully", "user": user_data}
    except frappe.DoesNotExistError:
        frappe.throw(_("User not found"), frappe.DoesNotExistError)
