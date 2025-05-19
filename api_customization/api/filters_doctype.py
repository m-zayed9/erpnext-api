import frappe
import json

@frappe.whitelist()
def search_records(doctype, filters=None, fields=None):
    # Check if user has read permission for the doctype
    if not frappe.has_permission(doctype, "read"):
        frappe.throw(f"Insufficient Permission for {doctype}")
    
    filters = json.loads(filters) if filters else []
    fields = json.loads(fields) if fields else ["*"]
    
    # Method 1: Use get_list instead of get_all (automatically applies user permissions)
    data = frappe.get_list(
        doctype,
        filters=filters,
        fields=fields,
        ignore_permissions=False  # This is the default, but being explicit
    )
    
    # Alternative Method 2: Manually check permissions for each record
    # Uncomment the following if you need more granular control:
    """
    data = frappe.get_all(
        doctype,
        filters=filters,
        fields=fields
    )
    
    # Filter records based on user permissions
    filtered_data = []
    for record in data:
        if frappe.has_permission(doctype, "read", record.name):
            filtered_data.append(record)
    data = filtered_data
    """
    
    # Get doctype fields for filters (this part remains the same)
    doctype_fields = frappe.get_doc("DocType", doctype).fields
    filter_fields = [{
        'field_label': field.label,
        'field_name': field.fieldname,
        'field_type': field.fieldtype,
        'field_options': field.options.strip().split('\n') if field.options else []
    } for field in doctype_fields if field.in_standard_filter == 1]
    
    return {
        "data": data,
        "filters": filter_fields
    }

# Alternative implementation with more comprehensive permission checking
@frappe.whitelist()
def search_records_comprehensive(doctype, filters=None, fields=None):
    # First check if doctype exists and user can access it
    if not frappe.db.exists("DocType", doctype):
        frappe.throw(f"DocType {doctype} does not exist")
    
    # Check read permission
    if not frappe.has_permission(doctype, "read"):
        frappe.throw(f"No permission to read {doctype}")
    
    # Parse parameters
    filters = json.loads(filters) if filters else []
    fields = json.loads(fields) if fields else ["*"]
    
    # Add user-specific filters if needed (e.g., for multi-tenant scenarios)
    # This ensures users only see records they're allowed to see
    user_filters = []
    
    # Example: Add company filter if doctype has company field
    meta = frappe.get_meta(doctype)
    if meta.has_field("company"):
        user_companies = frappe.get_list("Company", 
            filters={"name": ["in", frappe.get_roles()]}, 
            pluck="name"
        )
        if user_companies:
            user_filters.append(["company", "in", user_companies])
    
    # Combine filters
    if user_filters:
        if isinstance(filters, list):
            filters.extend(user_filters)
        else:
            filters = [filters] + user_filters if filters else user_filters
    
    # Get data with permission checking
    try:
        data = frappe.get_list(
            doctype,
            filters=filters,
            fields=fields,
            ignore_permissions=False,
            limit_page_length=None  # Remove default limit if needed
        )
    except frappe.PermissionError:
        frappe.throw(f"Permission denied to access {doctype}")
    
    # Get filter fields
    doctype_fields = frappe.get_doc("DocType", doctype).fields
    filter_fields = [{
        'field_label': field.label,
        'field_name': field.fieldname,
        'field_type': field.fieldtype,
        'field_options': field.options.strip().split('\n') if field.options else []
    } for field in doctype_fields if field.in_standard_filter == 1]
    
    return {
        "data": data,
        "filters": filter_fields,
        "total_count": len(data)
    }