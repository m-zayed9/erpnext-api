
import frappe
from frappe.desk.notifications import get_open_count
from datetime import datetime

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


@frappe.whitelist(allow_guest=True)
def item_calender(item_name):
    result = get_open_count('Item' , item_name)['timeline_data']
    converted_list = [
        {
            "date": datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d"),
            "value": value
        }
        for ts, value in result.items()
    ]
    return converted_list




