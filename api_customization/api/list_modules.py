import frappe



@frappe.whitelist()
def get_user_modules():
    user = frappe.session.user
    modules = frappe.get_all(
        "Module Def",
        fields=["name"]
    )

    blocked_modules = list(map(lambda i: i['module'] , frappe.get_all(
        "Block Module",
        filters=[['parent' , '=' , user]],
        fields=["module"]
    )))


    allowed_modules = [
        module['name'] for module in modules if module['name'] not in blocked_modules
    ]
    return allowed_modules

