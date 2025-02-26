# Copyright (c) 2025, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FinalDesign(Document):
    pass

@frappe.whitelist()
def map_quotation_to_final_design(source_name, target_doc=None):
    
    def set_missing_values(source, target):
        pass 

    target_doc = get_mapped_doc(
        "Quotation", source_name,
        {
            "Quotation": {
                "doctype": "Final Design",
                "field_map": {}
                
            },
            "Lead Material Details": {  
                "doctype": "Lead Material Details",  
                "field_map": {
                    "material_type": "material_type",
                    # "size": "size",
                    # "brand": "brand",
                    # "rate_range": "rate_range",
                    "image": "image",
                    # "feasible": "feasible",
                    "quantity": "quantity"
                },
                "add_if_empty": True 
            }
        },
        target_doc,  
        set_missing_values  
    )

    return target_doc

