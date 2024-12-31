import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class MaterialRequest(Document):
    pass

@frappe.whitelist()
def map_raw_material_to_material_request(source_name, target_doc=None):
    """
    Map fields from Raw Material Request to Material Request,
    including child table 'Item Details' and set qty to 1 in Material Request Item.
    """
    def set_missing_values(source, target):
        # Set the Material Request Type
        target.material_request_type = "Purchase"
        target.schedule_date = frappe.utils.nowdate()

    def set_item_defaults(source, target, source_parent):
        # Set default qty to 1 for each item in the child table
        target.qty = 1

    target_doc = get_mapped_doc("Raw Material Request", source_name,
        {
            "Raw Material Request": {
                "doctype": "Material Request",
                "field_map": {
                    # Map fields if necessary
                },
            },
            "Item Details": {  # Ensure this matches the child table in Raw Material Request
                "doctype": "Material Request Item",  # Ensure this matches the child table in Material Request
                "field_map": {
                    "item": "item_code"
                },
                "postprocess": set_item_defaults  # Set qty=1 after mapping
            }
        }, target_doc, set_missing_values)

    return target_doc
