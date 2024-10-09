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
                "field_map": {
                
                },
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

@frappe.whitelist()
def map_lead_to_mockup_design(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Mockup Design DocType.
    """
    def set_missing_values(source, target):
        target.mockup_design_to = "Lead"
        target.from_lead = source.name
        if hasattr(source, 'custom_images'):
            target.custom_images = source.custom_images  # Assuming you want to map this field

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Mockup Design",
                "field_map": {
                    "first_name": "from_lead",
                    "custom_material_type": "material_type"
                },
            },
            "Properties": {
                "doctype": "Properties",
                "field_map": {
                    'finishing': 'finishing',
                    'color': 'color',
                    'material': 'material'
                },
            },
        }, target_doc, set_missing_values)

    return target_doc
