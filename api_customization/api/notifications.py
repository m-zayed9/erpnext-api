
import frappe
from frappe.desk.doctype.notification_log.notification_log import get_notification_logs
@frappe.whitelist()
def list_notifications():
    return get_notification_logs().get('notification_logs' , [])






