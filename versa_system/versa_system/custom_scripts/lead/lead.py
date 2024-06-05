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
def map_lead_to_feasibility_check(source_name, target_doc=None):
    '''
        Method : Method to map a Lead to a Feasibility Property Check document

        Args :
         source_name : The name of the Lead document to be mapped
         target_doc : The target document to which the Lead and its Properties Table should be mapped.

        Output :  Name of the newly created Feasibility Property Check document.
    '''
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
