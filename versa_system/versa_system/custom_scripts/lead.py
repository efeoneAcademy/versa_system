import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {
    
                    "from_lead": "from_lead",              
                    "custom_material_type": "material_type"
                },
            },
            "Properties": {                               
                "doctype": "Properties",
                "field_map": {
                    'finishing': 'finishing',             
                    'color': 'color',
                    'material': 'material'
                },
            },
        }, target_doc)

    return target_doc
