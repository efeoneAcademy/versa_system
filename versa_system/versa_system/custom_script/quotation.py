

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def map_moc_design_to_quotation(source_name, target_doc=None):
    """
    Map fields from MOC Design to Quotation,
    """
    def set_missing_values(source, target):
        pass 

    target_doc = get_mapped_doc(
        "MOC Design", source_name,
        {
            "MOC Design": {
                "doctype": "Quotation",
                "field_map": {}
                
            },
            "Lead Material Details": {  
                "doctype": "Lead Material Details",  
                "field_map": {
                    "material_type": "material_type",
                    "size": "size",
                    "brand": "brand",
                    "rate_range": "rate_range",
                    "image": "image",
                    "feasible": "feasible",
                    "quantity": "quantity"
                },
                "add_if_empty": True 
            }
        },
        target_doc,  
        set_missing_values  
    )

    return target_doc
# import frappe
# from frappe.model.mapper import get_mapped_doc

# @frappe.whitelist()
# def map_moc_design_to_quotation(source_name, target_doc=None):
#     def set_missing_values(source, target):
#         target.run_method("set_missing_values")

#     target_doc = get_mapped_doc(
#         "MOC Design", source_name,
#         {
#             "MOC Design": {
#                 "doctype": "Quotation"
#             },
#             "Lead Material Details": {  
#                 "doctype": "Quotation Item",
#                 "field_map": {
#                     "material_type": "item_code",  
#                     "quantity": "qty",  
#                     "rate_range": "rate", 
#                 }
#             }
#         },
#         target_doc,
#         set_missing_values
#     )

#     if not target_doc.items:
#         frappe.throw("No items were added from MOC Design. Please check the source data.")

#     return target_doc

