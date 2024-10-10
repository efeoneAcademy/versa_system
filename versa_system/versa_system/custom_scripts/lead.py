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
    Map fields from Lead DocType to Quotation DocType.
    """
    def set_missing_values(source, target):
        target.quotation_to = "Lead"
        target.party_name = source.name

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "name": "party_name"
                },
            },
        }, target_doc, set_missing_values)

    return target_doc
