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

        target.items = []

        if frappe.db.exists("Feasibility Check", {"from_lead": source.name}):
            feasibility_doc = frappe.get_doc("Feasibility Check", {"from_lead": source.name})
            for row in feasibility_doc.properties:
                if row.go_forward:
                    new_row = target.append("items", {
                        'item_code': row.item_code,
                        'qty': row.quantity,
                        'item_name':row.item_type
                    })
                    new_row.uom = frappe.db.get_value("Item", row.item_code, "stock_uom")
                    new_row.rate = get_item_rate_from_rmb(row.item_code, source_name)

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
        if frappe.db.exists("Feasibility Check", {"from_lead":source.name}):
            feasibility_doc = frappe.get_doc("Feasibility Check", {"from_lead":source.name})
            for row in feasibility_doc.properties:
                if row.go_forward:
                    target.append("properties", {
                        'item_type': row.item_type,
                        'item_code': row.item_code,
                        'quantity' : row.quantity,
                    })



    target_doc = get_mapped_doc("Lead", source_name,
    {
        "Lead": {
            "doctype": "Mockup Design",
            "field_map": {
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
        if frappe.db.exists("Mockup Design", {"from_lead":source.name}):
            mockup_doc = frappe.get_doc("Mockup Design", {"from_lead":source.name})
            for row in mockup_doc.properties:
                    target.append("properties_table", {
                        'item_type': row.item_type,
                        'item_code': row.item_code,
                        'quantity': row.quantity,
                        'mockup_design': row.mockup_design,
                    })


    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Final Design",
                "field_map": {
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
        size_chart_name = frappe.db.exists("Size Chart", {"reference_name": reference})
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


@frappe.whitelist()
def fetch_raw_material_details(reference=None):
    '''
        Method: Fetches Raw Material from a Raw Material Bundle based on a provided reference.

        Output: Returns a list containing raw material details
    '''
    if reference:
        raw_material_name = frappe.db.exists("Raw Material Bundle", {"reference_name": reference})
        if raw_material_name:
            raw_material = frappe.get_all("Raw Material",filters={"parenttype": "Raw Material Bundle","parent": raw_material_name},fields=["item_code", "quantity", "uom","rate","total_amount"])
            return raw_material
        else:
            frappe.msgprint("Raw Material not found for the given reference.")
            return []
    else:
        frappe.throw("Reference is required.")


@frappe.whitelist()
def fetch_feature_detail():
    '''
        Method: Fetches all feature details.

        Output: Returns a list containing Feature details
    '''
    feature_details = frappe.get_all("Features Table", filters={"parenttype": "Feature"}, fields=["attribute", "value"])
    if feature_details:
        return feature_details
    else:
        frappe.msgprint("No features found.")
        return []


@frappe.whitelist()
def get_item_rate_from_rmb(item_code, lead):
    '''
       Method: Fetches Total Rate of Raw Materials From Raw Material Bundle.

       output: Returns Total Rate.
    '''

    feasibility_check = frappe.db.exists("Feasibility Check", lead)
    if feasibility_check:
        feasibility_doc = frappe.get_doc("Feasibility Check", feasibility_check)
        for row in feasibility_doc.properties:
            if row.item_code == item_code:
                grand_total = 0
                rmr = frappe.db.exists("Raw Material Bundle", {"reference_doctype":"Feasibility Solution", "reference_name":row.name})
                if rmr:
                    rmr_doc = frappe.get_doc("Raw Material Bundle", rmr)
                    for rmr_row in rmr_doc.raw_material:
                        grand_total += rmr_row.total_amount
                return grand_total
    return 0
