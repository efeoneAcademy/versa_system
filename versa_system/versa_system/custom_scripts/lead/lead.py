import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_lead_to_quotation(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.quotation_to = "Lead"

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "name":"party_name"
                },
            },

        }, target_doc, set_missing_values)
    return target_doc

@frappe.whitelist()
def custom_button_for_mockup_design(source_name, target_doc=None):
    """method:to get MockupDesign for custom button in lead doctype by using mapdoc.
       args:source_name,target_doc
       output:created the button MockupDesign and fetchedthe data
    """
    def set_missing_values(source, target):
        pass

    target_doc = get_mapped_doc("Lead", source_name,
    {
        "Lead": {
            "doctype": "Mockup Design",
            "field_map": {
            },
        },
         "Properties Table": {
                "doctype": "Properties Table",
                 "field_map": {
                    'item_type': 'item_type',
                    'meterial_type': 'meterial_type',
                    'design': 'design',
                    'model': 'model',
                    'brand': 'brand',
                    'size_chart': 'size_chart',
                    'rate_range': 'rate_range'
                },
            },
    }, target_doc, set_missing_values)

    target_doc.insert()
    frappe.db.commit()
    return target_doc.name
