# # # # Copyright (c) 2025, efeone and contributors
# # #  # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from frappe.model.mapper import get_mapped_doc

# class FeasibilityCheck(Document):
#     pass

# @frappe.whitelist()
# def map_lead_to_feasibility_check(source_name, target_doc=None):
#     """
#     Map fields from Lead Doctype to Feasibility Check Doctype,
#     including child table 'Material Details' -> 'Feasible Material Details'
#     """
#     def set_missing_values(source,target):
#         pass

#     target_doc = get_mapped_doc("Lead", source_name,
#         {
#             "Lead": {
#                 "doctype": "Feasibility Check",
#                 "field_map": {}
#             },
#             "Lead Material Details": { 
#                 "doctype": "Lead Material Details",  
#                 "field_map": {
#                     "material_type": "material_type",
#                     "size": "size",
#                     "brand": "brand",
#                     "rate_range": "rate_range",
#                     "image": "image",
#                     "feasible": "feasible",
#                     "quantity": "quantity"
#                 },
#                 "add_if_empty": True  
#             }
#         }, target_doc, set_missing_values)

#     return target_doc

import frappe
from frappe.model.document import Document

class FeasibilityCheck(Document):
    def before_save(self):
        if self.lead:
            self.fetch_lead_items()

    def fetch_lead_items(self):
        try:
            lead_doc = frappe.get_doc("Lead", self.lead)

            if hasattr(lead_doc, "lead_material_details"):
                self.set("feasible_material_details", [])  # Reset existing child table

                for item in lead_doc.lead_material_details:
                    self.append("feasible_material_details", {
                        "material_type": item.material_type,
                        "size": item.size,
                        "brand": item.brand,
                        "rate_range": item.rate_range,
                        "image": item.image,
                        "feasible": item.feasible,
                        "quantity": item.quantity
                    })
        except Exception as e:
            frappe.logger().error(f"Error in fetch_lead_items: {str(e)}")
            frappe.throw(f"Error fetching lead items: {str(e)}")

@frappe.whitelist()
def get_lead_material_details(lead_name):
    """Fetch child table data from a selected Lead and return as JSON"""
    try:
        lead_doc = frappe.get_doc("Lead", lead_name)

        material_details = []
        if hasattr(lead_doc, "lead_material_details"):
            for item in lead_doc.lead_material_details:
                material_details.append({
                    "material_type": item.material_type,
                    "size": item.size,
                    "brand": item.brand,
                    "rate_range": item.rate_range,
                    "image": item.image,
                    "feasible": item.feasible,
                    "quantity": item.quantity
                })

        return material_details

    except Exception as e:
        frappe.logger().error(f"Error fetching lead material details: {str(e)}")
        frappe.throw(f"Error fetching lead material details: {str(e)}")






