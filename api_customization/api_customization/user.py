import frappe
from frappe import _
from frappe.core.doctype.user.user import User

class CustomUser(User):
    def validate(self):
        super().validate()
        max_users = frappe.conf.get("max_users", 10)  # Get the max users limit from site_config.json
        current_user_count = frappe.db.count("User", {"enabled": 1})

        if self.is_new() and current_user_count >= max_users:
            frappe.throw(_("User limit reached! You can only create {0} users.").format(max_users))
