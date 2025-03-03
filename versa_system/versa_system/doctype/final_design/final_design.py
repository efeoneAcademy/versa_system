
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FinalDesign(Document):

    def before_save(self):
        if self.lead:
            self.fetch_lead_items()

    def fetch_lead_items(self):
        # Fetch Lead document
        lead_doc = frappe.get_doc("Lead", self.lead)

        # Clear existing items in the child table
        self.set("items", [])

        # Check if the lead has a child table named 'lead_material_details'
        if hasattr(lead_doc, "lead_material_details"):
            for item in lead_doc.lead_material_details:
                self.append("items", {
                    "material_type": item.material_type,
                    "image": item.image,
                    "quantity": item.quantity
                })


@frappe.whitelist()
def map_quotation_to_final_design(source_name, target_doc=None):
    
    def set_missing_values(source, target):
        pass 

    target_doc = get_mapped_doc(
        "Quotation", source_name,
        {
            "Quotation": {  
                "doctype": "Final Design",
                "field_map": {}
            },
            "Lead Material Details": {  
                "doctype": "Lead Material Details",  
                "field_map": {
                    "material_type": "material_type",
                    "image": "image",
                    "quantity": "quantity"
                },
                "add_if_empty": True 
            }
        },
        target_doc,  
        set_missing_values  
    )

    return target_doc


