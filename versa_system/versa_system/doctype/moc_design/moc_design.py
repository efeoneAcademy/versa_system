

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class MOCDesign(Document):
    pass

@frappe.whitelist()
def map_feasibility_check_to_moc_design(source_name, target_doc=None):
    """
    Map Feasibility Check to MOC Design, including only child table rows where 'feasible' is checked.
    """
    def set_missing_values(source, target):
        target.set("Lead Material Details", [])  

        filtered_materials = [row for row in source.get("feasible_material_details") if row.get("feasible")]

        for row in filtered_materials:
            target.append("moc_design", {
                "material_type": row.material_type,
                "product_item":row.product_item,
                "size": row.size,
                "brand": row.brand,
                "rate_range": row.rate_range,
                "image": row.image,
                "feasible": row.feasible,
                "quantity": row.quantity
            })

    target_doc = get_mapped_doc("Feasibility Check", source_name,
        {
            "Feasibility Check": {
                "doctype": "MOC Design",
                "field_map": {}
            }
        }, target_doc, set_missing_values)

    return target_doc
