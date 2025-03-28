 

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    pass

@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):
    """
    Map fields from Lead Doctype to Feasibility Check Doctype,
    including child table 'Material Details' -> 'Feasible Material Details'
    """
    def set_missing_values(source,target):
        pass

    

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {}
            },
            "Lead Material Details": { 
                "doctype": "Lead Material Details",  
                "field_map": {
                    "material_type": "material_type",
                    "product_item":"product_item",
                    "size": "size",
                    "brand": "brand",
                    "rate_range": "rate_range",
                    "image": "image",
                    "feasible": "feasible",
                    "quantity": "quantity"
                },
                "add_if_empty": True  
            }
        }, target_doc, set_missing_values)

    return target_doc








