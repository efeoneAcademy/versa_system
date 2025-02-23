

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class MOCDesign(Document):
    pass

@frappe.whitelist()
def map_feasibility_check_to_moc_design(source_name, target_doc=None):
    """
    Map fields from Feasibility Check to MOC Design,
    including child table 'Feasible Material Details' -> 'MOC Material Details'
    """
    def set_missing_values(source, target):
        pass 

    target_doc = get_mapped_doc(
        "Feasibility Check", source_name,
        {
            "Feasibility Check": {
                "doctype": "MOC Design",
                "field_map": {}
                
            },
            "Lead Material Details": {  
                "doctype": "Lead Material Details",  
                "field_map": {
                    "material_type": "material_type",
                    "size": "size",
                    "brand": "brand",
                    "rate_range": "rate_range",
                    "image": "image",
                    "feasible": "feasible",
                    "quantity": "quantity"
                },
                "add_if_empty": True 
            }
        },
        target_doc,  
        set_missing_values  
    )

    return target_doc

