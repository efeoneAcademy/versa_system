import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Quotation(Document):
    pass

@frappe.whitelist()
def map_lead_to_quotation(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Quotation DocType,
    including child table 'Item Details' and 'Quotation Item'.
    """
    def set_missing_values(source, target):
        target.quotation_to = "Lead"
        target.party_name = source.name # Customer name


        # Set default values for child table rows if needed
        for item in target.items:
            item.qty = item.qty or 1  # Default quantity is 1

        # Ensure the 'Item Details' child table is also populated correctly
        for item_detail in source.custom_item_details:
            target.append('item_details', {
                'item': item_detail.item,
                'material': item_detail.material,
                'brand': item_detail.brand,
                'model': item_detail.model,
                'rate_range': item_detail.rate_range,
                'size_chart': item_detail.size_chart,
                'design': item_detail.design
            })

    def filter_approved_items(source, target, source_parent):
        """
        Filters rows based on a custom condition.
        Ensure 'approve' is a valid field in the child table of the Lead DocType.
        """
        if hasattr(source, "approve") and source.approve:  # Check if 'approve' exists and is true
            target.item_name = source.item
            target.item_code = source.item  # Map item details
            target.qty = source.qty or 1  # Default quantity is 1 if not set

    target_doc = get_mapped_doc(
        "Lead",  # Source DocType
        source_name,  # Source document name
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "lead_name": "customer_name",  # Map lead_name to customer_name
                    "email_id": "contact_email"  # Map email_id to contact_email
                }
            },
            "Item Details": {  # Child table in Lead
                "doctype": "Quotation Item",  # Target child table in Quotation
                "field_map": {
                    "item": "item_code",  # Map item to item_code
                    "material": "material",
                    "brand": "brand",
                    "model": "model",
                    "rate_range": "rate_range",
                    "size": "size",
                    "design": "design"
                },
                "postprocess": filter_approved_items  # Process each child row after mapping
            }
        },
        target_doc,  # Target document (Quotation)
        set_missing_values  # Additional processing for the target document
    )

    return target_doc
