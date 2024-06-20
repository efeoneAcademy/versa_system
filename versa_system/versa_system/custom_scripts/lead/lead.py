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
        for row in target.items:
            row.item_name = frappe.db.get_value("Item", row.item_code, "item_name")
            row.uom = frappe.db.get_value("Item", row.item_code, "stock_uom")
            row.rate = get_item_rate_from_rmb(row.item_code, source_name)

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Quotation",
                "field_map": {
                    "lead_name": "party_name",
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

def get_item_rate_from_rmb(item_code, lead):
    grand_total = 0
    feasibility_check = frappe.db.exists("Feasibility Check", lead)
    if feasibility_check:
        feasibility_doc = frappe.get_doc("Feasibility Check", feasibility_check)
        for row in feasibility_doc.properties:
            rmr = frappe.db.exists("Raw Material Bundle", {"reference_doctype":"Feasibility Solution", "reference_name":row.name})
            if rmr:
                rmr_doc = frappe.get_doc("Raw Material Bundle", rmr)
                for row in rmr_doc.raw_material:
                    grand_total += row.total_amount
    print("the returned value is : ", grand_total)
    return grand_total
