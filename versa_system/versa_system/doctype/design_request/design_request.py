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

@frappe.whitelist()
def map_quotation_to_design_request(source_name, target_doc=None):
    """
    Map fields from Quotation DocType to Design Request DocType,
    including specified fields like 'lead', 'customer_name', and mapping 'item_code' to 'item' in Item Details.
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        target.type = "Final Design"

    # Get the mapped document
    target_doc = get_mapped_doc(
        "Quotation",
        source_name,
        {
            "Quotation": {
                "doctype": "Design Request",
                "field_map": {
                    "party_name": "lead",  # Map 'party_name' to 'lead'
                    "customer_name": "first_name",  # Map 'customer_name' to 'first_name'
                },
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
                },
            },
        },
        target_doc,
        set_missing_values
    )

    return target_doc




#Function to dynamically activate one workflow and deactivate another
def set_workflow(doc, method):
    if doc.type == "Mockup Design":
        frappe.db.set_value("Workflow", {"name": "Mockup Workflow"}, "is_active", 1)
        frappe.db.set_value("Workflow", {"name": "Final Design Workflow"}, "is_active", 0)
    elif doc.type == "Final Design":
        frappe.db.set_value("Workflow", {"name": "Mockup Workflow"}, "is_active", 0)
        frappe.db.set_value("Workflow", {"name": "Final Design Workflow"}, "is_active", 1)
