import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    pass

@frappe.whitelist()
def map_feasibility_to_mockup_design(source_name, target_doc=None):
    """
    Map fields from Feasibility Check DocType to Mockup Design DocType,
    including the child table 'Enquiry Details' and its data.
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        pass

    target_doc = get_mapped_doc("Feasibility Check", source_name,
        {
            "Feasibility Check": {
                "doctype": "Mockup Design",
                "field_map": {}
            },
            "Enqury Details": {  # Mapping the child table
                "doctype": "Enqury Details",  # Ensure this matches the target child table in Mockup Design
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
