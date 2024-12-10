# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MOCUPDesign(Document):
	pass
# @frappe.whitelist()
# def map_lead_to_moc(source_name, target_doc=None):
#     """
#     Map fields from Lead DocType to Feasibility Check DocType,
#     including child table 'Enquiry Details'
#     """
#     def set_missing_value(source, target):
#         # Set any missing values if needed
#         pass
#
#     target_doc = get_mapped_doc("Feasibility Check", source_name,
#         {
#             "Lead": {
#                 "doctype": "MOC UP Design",
#                 "field_map": {},
#             },
#             # "Item Details": {  # Ensure that 'Enquiry Details' is the correct child table name
#             #     "doctype": "Item Details",  # Ensure this matches the target child table
#             #     "field_map": {
#             #         "item": "item",
#             #         "material": "material",
#             #         "brand": "brand",
#             #         "model": "model",
#             #         "rate_range": "rate_range",
#             #         "size": "size",
#             #         # "colour": "colour",
#             #         "design": "design",
#             #     }
#             # }
#         }, target_doc, set_missing_value)
#
#     return target_doc
