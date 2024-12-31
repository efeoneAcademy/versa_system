# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc



class RawMaterialRequest(Document):
	pass

@frappe.whitelist()
def map_lead_to_raw_material_request(source_name, target_doc=None):
    """
    Map fields from Design Request DocType to Raw Material Request DocType,
    including child table 'Item Details'
    """
    def set_missing_values(source, target):
        # Any additional field setup
        pass

    target_doc = get_mapped_doc(
        "Design Request", source_name,
        {
            "Design Request": {
                "doctype": "Raw Material Request",  # Fixed extra space in DocType name
                "field_map": {},
            },
            "Item Details": {  # Ensure this matches the child table in Design Request
                "doctype": "Item Details",  # Ensure this matches the child table in Raw Material Request
                "field_map": {
                    "item": "item",
                    "material": "material",
                    "brand": "brand",
                    "model": "model",
                    "rate_range": "rate_range",
                    "size": "size",
                    "design": "design",
                }
            }
        },
        target_doc,
        set_missing_values
    )

    return target_doc
