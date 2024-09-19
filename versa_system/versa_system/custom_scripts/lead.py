import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):
    """
    Map fields from the Lead DocType to Feasibility Check DocType.
    
    Parameters:
        source_name (str): The name of the Lead document to be mapped.
        target_doc (Document, optional): An existing target document to map to. Defaults to None.
    
    Returns:
        Document: The mapped target document.
    """

    # Use get_mapped_doc to map fields from Lead to Feasibility Check and related DocTypes
    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {
                    "first_name": "from_lead"
                    
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
            "Size Chart": {                               
                "doctype": "Size Chart",
                "field_map": {
                    'size': 'size',          
                    'dimensions': 'dimensions'
                },
            },
        }, target_doc)

    
    if not target_doc:
        frappe.throw("Target document could not be created.")

    return target_doc