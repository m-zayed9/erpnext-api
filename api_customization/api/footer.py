import frappe


@frappe.whitelist()
def get_module_home(module_name):
    """Fetch home page data for a module, including key insights and shortcut apps."""
    if not module_name:
        return {"error": "Module name is required"}

    # Get the main chart for insights
    chart = frappe.get_all(
        "Dashboard Chart", filters={"module": module_name}, fields=["name"]
    )

    # Get shortcut apps (linked DocTypes)
    shortcuts = frappe.get_all(
        "DocType", filters={"module": module_name}, fields=["name"]
    )

    # Get frequently used apps from User Preferences
    user_apps = frappe.get_all(
        "User Permission",
        filters={"user": frappe.session.user, "allow": "DocType"},
        fields=["for_value"],
    )

    pinned_apps = [app["for_value"] for app in user_apps]

    return {
        "module": module_name,
        "chart": chart,
        "shortcuts": shortcuts,
        "pinned_apps": pinned_apps,
    }
