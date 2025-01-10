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
    # Validate if a feasibility check already exists for this lead
    existing_feasibility = frappe.db.exists(
        "Feasibility Check",
        {
            "lead": source_name,
            "docstatus": ["<", 2],
            "workflow_state": ["!=", "Rejected"]
        }
    )

    if existing_feasibility:
        frappe.msgprint(
            f"A feasibility check already exists for this lead (Lead: {source_name}).",
            title="Notification",
            indicator="red"
        )
        return None  

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
