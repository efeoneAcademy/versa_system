import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
@frappe.whitelist()
def map_lead_to_quotation(source_name, target_doc=None):
    '''
       Method: Method to map a Lead to Quotation doctype
       output: data from lead is mapped to a new Quotation document
    '''
    def set_missing_values(source, target):
        target.quotation_to = "Lead"

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "name": "party_name",
                },
            },

            "Properties Table":{
                "doctype": "Quotation Item",
                "field_map": {
                    'quantity':'qty',
                    'item_code':'item_code'
                },
            },
        }, target_doc, set_missing_values)
    return target_doc

@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):
    '''
        Method: Method to map a Lead to a Feasibility Check document
        Args:
         source_name: The name of the Lead document to be mapped
         target_doc: The target document to which the Lead and its Properties Table should be mapped.
        Output: Name of the newly created Feasibility Check document.
    '''
    def set_missing_values(source, target):
        pass

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {
                },
            },
            "Properties Table": {
                "doctype": "Feasibility Solution",
                "field_map": {
                    'item_type' : 'item_type',
                    'item_code' : 'item_code',
                    'quantity'  : 'quantity',
                    'low_range' : 'low_range',
                    'high_range': 'high_range',
                    'name'      : 'reference'

                },
            },
        }, target_doc, set_missing_values)

    return target_doc

@frappe.whitelist()
def map_lead_to_mockup_design(source_name, target_doc=None):
    """Method to get Mockup Design for custom button in lead doctype by using mapdoc.
       Output: data from lead is mapped to a new mockup design document
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
                'item_type'  : 'item_type',
                 'item_code' : 'item_code',
                 'quantity'  : 'quantity',
                 'low_range' : 'low_range',
                 'high_range': 'high_range'
            },
        },
    }, target_doc, set_missing_values)

    return target_doc

@frappe.whitelist()
def get_lead_properties(lead_name):
    """Method to get data from the Lead into child table in Mockup Design.
       Output: data from lead is mapped to a new mockup design document
    """
    if frappe.db.exists("Lead", lead_name):
        lead = frappe.get_doc("Lead", lead_name)
        custom_property_table = []
        for item in lead.custom_property_table:
            custom_property_table.append({
                'item_type' : item.item_type,
                'item_code' : item.item_code,
                'quantity'  : item.quantity,
                'low_range' : item.low_range,
                'high_range': item.high_range
            })
        return custom_property_table
    else:
        frappe.throw(_("Lead not found"))


@frappe.whitelist()
def map_lead_to_final_design(source_name, target_doc=None):
    '''
        Method: Method to map Lead information to Final Design document.

        Output: Updated Final Design document.
    '''
    def set_missing_values(source, target):
        '''
        Method: Sets missing values from Quotation items to the target Final Design document.

        Output: None
    '''
        quotation = frappe.get_all("Quotation", filters={"party_name": source_name}, fields=["name"])
        if quotation:
            quotation_doc = frappe.get_doc("Quotation", quotation[0].name)
            for item in quotation_doc.items:
                target.append('quotation_items', {
                    'item_code': item.item_code,
                    'item_group': item.item_group,
                    'stock_uom': item.stock_uom,
                      'qty'    : item.qty,
                      'rate'   :item.rate,
                      'amount'  :item.amount,
                      'item_name':item.item_name,
                      'uom'      :item.uom,
                })

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Final Design",
                "field_map": {
                },
            },
            "Properties Table": {
                "doctype": "Properties Table",
                "field_map": {
                    'item_type': 'item_type',
                    'item_code' : 'item_code',
                    'quantity'  : 'quantity',
                    'low_range' : 'low_range',
                    'high_range': 'high_range'
                },
            },
        }, target_doc, set_missing_values)

    return target_doc


@frappe.whitelist()
def fetch_size_chart_details(reference=None):
    '''
        Method: Fetches size attributes from a Size Chart based on a provided reference.

        Output: Returns a list containing size attribute details
    '''
    if reference:
        size_chart_name = frappe.db.get_value("Size Chart", {"reference_name": reference}, "name")
        if size_chart_name:
            size_attributes = frappe.get_all("Size Attribute",filters={"parenttype": "Size Chart","parent": size_chart_name},fields=["attribute", "value", "uom"])
            return size_attributes
        else:
            frappe.msgprint("Size Chart not found for the given reference.")
            return []
    else:
        frappe.throw("Reference is required.")



@frappe.whitelist()
def fetch_feature_details(reference=None):
    '''
        Method: Fetches  features from a Create Feature based on a provided reference.

        Output: Returns a list containing Feature details
    '''
    if reference:
        feature_name = frappe.db.get_value("Feature", {"reference_name": reference}, "name")
        if feature_name:
            feature_details = frappe.get_all("Features Table",filters={"parenttype": "Feature","parent": feature_name},fields=["attribute", "value"])
            return feature_details
        else:
            frappe.msgprint("Feature not found for the given reference.")
            return []
    else:
        frappe.throw("Reference is required.")
