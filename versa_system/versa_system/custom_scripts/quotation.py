import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_quotation_to_final_design(source_name, target_doc=None):
    """
    Method to map a Quotation to a Final Design document.

    Args:
        source_name: The name of the Quotation document to be mapped.
        target_doc: The target document to which the Quotation should be mapped.

    Returns:
        The newly created Final Design document.
    """
    def set_missing_values(source, target):
        # Set any default or custom values if required
        pass

    target_doc = get_mapped_doc("Quotation", source_name,
        {
            "Quotation": {
                "doctype": "Final Design",
                "field_map": {
                    "party_name": "lead"
                },
            },
            "Quotation Item": {
                "doctype": "Final",  # Assuming 'Final' is the correct child DocType in Final Design
                "field_map": {
                    "item_name": "item_code"
                }
            },
            "Quotation Item": {  # Use a different key for the second child table
                "doctype": "Quotation Item",  # This is for the additional child table
                "field_map": {
                    "qty": "qty",
                    "uom": "uom"
                }
            }
        }, target_doc, set_missing_values)

    return target_doc
