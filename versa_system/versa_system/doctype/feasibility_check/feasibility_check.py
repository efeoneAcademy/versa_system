
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    pass
@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Feasibility Check DocType,
    including child table 'Enquiry Details'
    """
    existing_feasibility = frappe.get_all(
        'Feasibility Check',
        filters={'lead': source_name},
        fields=['name']
    )

    if existing_feasibility:
        frappe.throw(f"A feasibility check already exists for this lead (Lead: {source_name}).")
    def set_missing_values(source, target):
        # Set any missing values if needed
        pass

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
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
