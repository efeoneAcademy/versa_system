# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc



class DesignRequest(Document):
	pass
@frappe.whitelist()
def map_feasibility_check_to_moc(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Feasibility Check DocType,
    including child table 'Enquiry Details'
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        pass

    target_doc = get_mapped_doc("Feasibility Check", source_name,
        {
            "Feasibility Check": {
                "doctype": "Design Request",
                "field_map": {},
            },
            "Item Details": {  # Ensure that 'Item Details' is the correct child table name
                "doctype": "Item Details",  # Ensure this matches the target child table
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
        }, target_doc, set_missing_values)

    return target_doc.save()

@frappe.whitelist()
def map_lead_to_design_request(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Design Request DocType,
    including child table 'Enquiry Details'
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        target.type = "Final Design"

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Design Request",
                "field_map": {},
            },
            "Item Details": {  # Ensure that 'Item Details' is the correct child table name
                "doctype": "Item Details",  # Ensure this matches the target child table
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
        }, target_doc, set_missing_values)

    return target_doc
