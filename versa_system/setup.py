# import os
# import click
# import frappe
# from frappe import _
# from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# # Installation Functions
# def after_install():
#     create_custom_fields(get_lead_custom_fields(), ignore_validate=True)
#     # create_custom_roles('')

# def after_migrate():
#     after_install()

# def before_uninstall():
#     delete_custom_fields(get_lead_custom_fields())


# # Helper Function
# def delete_custom_fields(custom_fields: dict):
#     """
#     Method to Delete custom fields.
#     Args:
#         custom_fields: a dict like {'Task': [{fieldname: 'your_fieldname', ...}]}
#     """
#     for doctype, fields in custom_fields.items():
#         frappe.db.delete(
#             "Custom Field",
#             {
#                 "fieldname": ("in", [field["fieldname"] for field in fields]),
#                 "dt": doctype,
#             },
#         )
#         frappe.clear_cache(doctype=doctype)

# # Custom Field Definitions
# def get_lead_custom_fields():
#     """
#     Custom fields that need to be added to the Customer DocType.
#     """
#     return {
#         "Lead": [
            
#             {
#                 "fieldname": "Tree",
#                 "fieldtype": "Data",
#                 "label": "tree",
#                 "insert_after": "source"
#             },
            
#         ]
#     }
