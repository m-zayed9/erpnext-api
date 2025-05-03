import frappe
from frappe import _


@frappe.whitelist()
def get_user_details():
    try:
        user_email = frappe.session.user
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
            "image": user.user_image,
        }
    except frappe.DoesNotExistError:
        frappe.throw(_("User not found"), frappe.DoesNotExistError)


@frappe.whitelist()
def update_user_details(
    first_name=None, middle_name=None, last_name=None, language=None, time_zone=None,user_image=None
):
    try:
        user_email = frappe.session.user
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
        if user_image:
            user.user_image = user_image

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
            "user_image": user.user_image,
        }

        return {"message": "User updated successfully", "user": user_data}
    except frappe.DoesNotExistError:
        frappe.throw(_("User not found"), frappe.DoesNotExistError)
