import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _

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

    return target_doc

@frappe.whitelist()
def map_lead_to_mockup_design(source_name, target_doc=None):
    """method to get Mockup Design for custom button in lead doctype by using mapdoc.
       output: data from lead is mapped to a new mockup design document
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

    return target_doc

@frappe.whitelist()
def get_lead_properties(lead_name):
    """method to  Get data from the Lead in to child table in Mockup Design.
    output: data from lead is mapped to a new mockup design document
    """
    if frappe.db.exists("Lead", lead_name):
        lead = frappe.get_doc("Lead", lead_name)
        custom_property_table = []
        for item in lead.custom_property_table:
            custom_property_table.append({
                'item_type': item.item_type,
                'material_type': item.material_type,
                'design': item.design,
                'model': item.model,
                'brand': item.brand,
                'size_chart': item.size_chart,
                'colour': item.colour,
            })
        return custom_property_table
    else:
        frappe.throw(_("Lead not found"))
