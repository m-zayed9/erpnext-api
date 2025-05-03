
import frappe

@frappe.whitelist()
def list_all_doctypes():
    try:
        all_doctypes = frappe.get_all("DocType", fields=["name"], order_by="name ASC")

        accessible_doctypes = [
            d["name"]
            for d in all_doctypes
            if frappe.has_permission(doctype=d["name"], ptype="read")
        ]

        return {"doctypes": accessible_doctypes}

    except Exception as e:
        frappe.log_error(f"Error fetching accessible DocTypes: {e}")
        return {"error": str(e)}
