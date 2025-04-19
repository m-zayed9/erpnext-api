import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_role_permissions(module=None):
    role_name = 'Mobile App'
    if not frappe.db.exists("Role", role_name):
        frappe.throw(
            title="Role Not Found",
            msg=_("The role '{0}' does not exist. Please create this role to start using the mobile app.").format(role_name),
            exc=frappe.exceptions.ValidationError
        )

    role_permissions = frappe.get_all(
        "Custom DocPerm",
        filters={"role": role_name},
        fields=["parent as doctype", "read", "write", "create", "delete", "submit", "cancel", "print", "email", "export", "import", "share"]
    ) or frappe.get_all(
        "DocPerm",
        filters={"role": role_name},
        fields=["parent as doctype", "read", "write", "create", "delete", "submit", "cancel", "print", "email", "export", "import", "share"]
    )

    permissions_dict = {perm["doctype"]: {k: v for k, v in perm.items() if k != "doctype"} for perm in role_permissions}

    if module:
        allowed_doctypes = set(frappe.get_all("DocType", filters={"module": module}, pluck="name"))
        permissions_dict = {doctype: perms for doctype, perms in permissions_dict.items() if doctype in allowed_doctypes}

    frappe.local.response.update({
        'doctypes': list(permissions_dict.keys()),
        'permissions_list': permissions_dict
    })
    return  


@frappe.whitelist()
def get_all_reports_with_roles(module):
    reports = frappe.get_all("Report", fields=["name", "module", "report_type"], filters=[['module' , '=' , module]])

    report_details = []

    for report in reports:
        report_name = report["name"]
        module = report["module"]
        report_type = report["report_type"]

        roles = frappe.get_all(
            "Has Role",
            filters={"parent": report_name, "parenttype": "Report"},
            fields=["role"]
        )
        role_list = [role["role"] for role in roles]

        if "Mobile App" in role_list :
            report_details.append({
                "Report Name": report_name,
                "Report Type": report_type
            })

    frappe.local.response.update({
        "status": "success",
        "data": report_details,
    })
    return  