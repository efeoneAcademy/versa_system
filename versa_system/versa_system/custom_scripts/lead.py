import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Feasibility Check DocType,
    including child table 'Enquiry Details'
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        pass

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {},
            },
            "Enqury Details": {  # Ensure that 'Enquiry Details' is the correct child table name
                "doctype": "Enqury Details",  # Ensure this matches the target child table
                "field_map": {
                    "item": "item",
                    "material": "material",
                    "brand": "brand",
                    "model": "model",
                    "rate_range": "rate_range",
                    "size": "size",
                    "colour": "colour",
                    "design": "design",
                }
            }
        },
        target_doc,
        set_missing_values
    )
    
    target_doc.save(ignore_permissions=True)  # Save without permission checks

    return target_doc

@frappe.whitelist()
def map_lead_to_quotation(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Quotation DocType,
    including only approved rows from the 'Enquiry Details' child table.
    """
    def set_missing_values(source, target):
        target.quotation_to = "Lead"
        target.party_name = source.name

    def filter_approved_items(source, target, source_parent):
        # Only map rows where the 'approve' checkbox is checked
        if source.approve:
            target.item_name = source.item
            target.item_code = source.item

    # Map Lead to Quotation, applying the filter to child table rows
    target_doc = get_mapped_doc(
        "Lead",
        source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "name": "party_name"  # Map the Lead name to Quotation's party_name
                },
            },
            "Enqury Details": {  # Source child table name
                "doctype": "Quotation Item",  # Target child table DocType
                "postprocess": filter_approved_items,  # Process only approved items
                "condition": lambda doc: doc.approve  # Only map rows where 'approve' is checked
            }
        },
        target_doc,
        set_missing_values
    )

    return target_doc

@frappe.whitelist()
def update_lead_status_on_save(doc, method):
    """Automatically change lead status to 'Interested' when saved."""
    if doc.status == "Lead":
        doc.status = "Interested"
