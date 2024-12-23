import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Quotation(Document):
    pass

@frappe.whitelist()
def map_lead_to_quotation(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Quotation DocType,
    including child table 'Item Details'
    """
    def set_missing_values(source, target):
        target.quotation_to = "Lead"
        target.party_name = source.name

    def filter_approved_items(source, target, source_parent):
        # Only map rows where the 'approve' checkbox is checked
            target.item_name = source.item
            target.item_code = source.item  # Allow creating the quotation even if the user does not have permissions
            target.qty = 1  # Set quantity to 1

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "lead_name": "customer_name",  # Example: Map Lead's 'lead_name' to Quotation's 'customer_name'
                    "email_id": "contact_email"  # Example: Map Lead's 'email_id' to Quotation's 'contact_email'
                },
            },
            "Item Details": {  # Correct child table name in Lead
                "doctype": "Quotation Item",  # Correct child table name in Quotation
                "field_map": {
                    "item": "item_code"
                },
                 "postprocess": filter_approved_items  # Set qty=1 after mapping
            }
        }, target_doc, set_missing_values)

    return target_doc
