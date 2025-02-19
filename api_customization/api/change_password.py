import frappe
from frappe import _


@frappe.whitelist(allow_guest=False)
def change_password(user_email, old_password, new_password):
    try:
        user = frappe.get_doc("User", user_email)

        # Verify old password
        if not frappe.utils.password.check_password(user.name, old_password):
            frappe.throw(_("Incorrect old password"), frappe.AuthenticationError)

        # Set new password
        frappe.utils.password.update_password(user.name, new_password)

        # Ensure the change is saved
        user.save()
        frappe.db.commit()

        return {"message": "Password updated successfully"}
    except frappe.DoesNotExistError:
        frappe.throw(_("User not found"), frappe.DoesNotExistError)
    except Exception as e:
        frappe.throw(_("An error occurred: {0}").format(str(e)))
