
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    pass
@frappe.whitelist()
def map_lead_to_feasibility_check(source_name, target_doc=None):
    """
    Map fields from Lead DocType to Feasibility Check DocType,
    including child table 'Enquiry Details'
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        pass

    target_doc = get_mapped_doc("Lead", source_name,
        {
            "Lead": {
                "doctype": "Feasibility Check",
                "field_map": {},
            },
            "Item Details": {  # Ensure that 'Enquiry Details' is the correct child table name
                "doctype": "Item Details",  # Ensure this matches the target child table
                "field_map": {
                    "item": "item",
                    "material": "material",
                    "brand": "brand",
                    "model": "model",
                    "rate_range": "rate_range",
                    "size": "size",
                    # "colour": "colour",
                    "design": "design",
                }
            }
        }, target_doc, set_missing_values)

    return target_doc


# @frappe.whitelist()
# def map_lead_to_feasibility_check(source_name, target_doc=None):
#     '''
#        Method: Method to map a Lead to Quotation doctype
#        output: data from lead is mapped to a new Quotation document
#     '''
#     # def set_missing_values(source, target):
#     #     target.feasibility_check = "Lead"
#     #     for row in target.item_details:
#     #         row.item_name = frappe.db.get_value("Item", row.item_code, "item_name")
#     #         row.uom = frappe.db.get_value("Item", row.item_code, "stock_uom")
#     #         row.rate = get_item_rate_from_rmb(row.item_code, source_name)
#
#     target_doc = get_mapped_doc("Lead", source_name,
#         {
#             "Lead": {
#                 "doctype": "Feasibility Check",
#                 "field_map": {
#                     "first_name": "first_name",
#
#                 },
#             },
#
#             # "Properties Table":{
#             #     "doctype": "Item Details",
#             #     "field_map": {
#             #         'first_name':'first_name',
#             #         'mobile_no':'mobile_no'
#             #     },
#             # },
#         }, target_doc)
#     return target_doc


# @frappe.whitelist()
# def map_lead_to_feasibility_check(source_name, target_doc=None):
#     def update_doc(source, target):
#         target.lead= source.name
#         target.first_name = source.first_name
#
#         target.item_details = []
#         for item in source.get("custom_item_details", []):
#             target.append("item_details", {
#                 "item": item.item,
#                 "material": item.material,
#                 "design": item.design,
#                 "brand": item.brand,
#                 "size_chart": item.size_chart,
#                 "rate_range": item.rate_range,
#                 "made": item.made
#             })
#
#     target_doc = get_mapped_doc("Lead", source_name, {
#         "Lead": {
#             "doctype": "Feasibility Check",
#             "field_map": {
#                 "name": "lead_id",
#                 "first_name": "first_name"
#             }
#         }
#     }, target_doc, update_doc)
#
#     return target_doc
