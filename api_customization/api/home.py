import frappe


@frappe.whitelist()
def list_user_modules():
    """Fetch modules the logged-in user has access to, including tasks, reports, and charts."""

    # Get user roles
    user_roles = frappe.get_roles(frappe.session.user)

    # Get allowed modules linked to user roles
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

    if not allowed_modules:
        return {"message": "No accessible modules"}

    # Fetch tasks, reports, and charts for each module
    modules_data = []
    for module in allowed_modules:
        module_name = module["module_name"]

        # Get common tasks (Doctypes linked to the module)
        common_tasks = frappe.get_all(
            "DocType", filters={"module": module_name}, fields=["name"]
        )

        # Get reports linked to the module
        reports = frappe.get_all(
            "Report",
            filters={"module": module_name},
            fields=["name", "ref_doctype", "report_type"],
        )

        # Get charts linked to the module
        charts = frappe.get_all(
            "Dashboard Chart", filters={"module": module_name}, fields=["name"]
        )

        modules_data.append(
            {
                "module": module_name,
                "app_name": module["app_name"],
                "common_tasks": common_tasks,
                "reports": reports,
                "charts": charts,
            }
        )

    return modules_data
