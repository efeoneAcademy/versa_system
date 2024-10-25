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
        }, target_doc, set_missing_values)

    return target_doc

@frappe.whitelist()
def map_lead_to_quotation(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Quotation DocType,
    including child table 'items' mapped to 'Quotation Item'
    """
    def set_missing_values(source, target):
        target.quotation_to = "Lead"
        target.party_name = source.name

    # Correct mapping with the child table and its fields
    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {

                    "name": "party_name"  # Map the Lead name to Quotation's party_name
                },
            },
            "Enqury Details": {  # Assuming the child table in Lead is 'lead_items'
                "doctype": "Quotation Item",  # Actual child table DocType is 'Quotation Item'
                "field_map": {
                    "item": "item_name",
                    "item": "item_code",
                     # Map the rate if available
                }
            }
        }, target_doc, set_missing_values)

    return target_doc
@frappe.whitelist()
def update_lead_status_on_save(doc, method):
    """Automatically change lead status to 'Interested' when saved."""
    if doc.status == "Lead":
        doc.status = "Interested"
