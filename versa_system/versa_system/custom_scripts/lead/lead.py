import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
# Method to create a Feasibility Property Check from a Lead
def map_lead_to_feasibility_check(source_name, target_doc=None):
    def set_missing_values(source, target):
        pass

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Property Check",
                "field_map": {
                },
            },
            "Properties Table": {
                "doctype": "Feasibility Check",
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

    target_doc.submit()
    frappe.msgprint(('Feasibility Check created'), indicator="green", alert=1)
    frappe.db.commit()
    return target_doc.name
