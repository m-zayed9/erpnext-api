import frappe
import json

@frappe.whitelist()
def search_records(doctype , filters=None, fields=None):

    filters = json.loads(filters) if filters else []
    fields = json.loads(fields) if fields else ["*"]

    data = frappe.get_all(
        doctype,
        filters=filters,
        fields=fields  
    )

    doctype_fields = frappe.get_doc("DocType", doctype).fields

    fields = [{
        'field_lable':field.label,
        'field_name':field.fieldname,
        'field_type':field.fieldtype,
        'field_options':field.options.strip().split('\n') if field.options else []
    
        } for field in doctype_fields if field.in_standard_filter==1
    ]
    return {
        "data":data,
        "filters": fields
    }
