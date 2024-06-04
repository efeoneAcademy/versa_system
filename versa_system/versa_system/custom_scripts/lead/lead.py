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
