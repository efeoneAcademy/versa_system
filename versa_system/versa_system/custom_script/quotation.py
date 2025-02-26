
import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_moc_design_to_quotation(source_name, target_doc=None):
    """
    Map fields from MOC Design to Quotation, ensuring rate_range and rate are the same.
    """

    def set_missing_values(source, target):
        lead_materials = frappe.get_all(
            "Lead Material Details",
            filters={"parent": source.name},  
            fields=["material_type", "size", "brand", "rate_range", "quantity", "image", "feasible"]
        )

        for item in lead_materials:
            # Append to 'material_item' table if it exists
            if hasattr(target, "material_item"):
                target.append("material_item", {
                    "material_type": item.material_type,
                    "size": item.size,
                    "brand": item.brand,
                    "rate_range": item.rate_range,
                    "image": item.image,
                    "feasible": item.feasible,
                    "quantity": item.quantity
                })

            # Append to 'items' table if it exists
            if hasattr(target, "items"):
                target.append("items", {  
                    "item_code": item.material_type,  
                    "rate": item.rate_range,
                    "qty": item.quantity  
                })

    target_doc = get_mapped_doc(
        "MOC Design", source_name,
        {
            "MOC Design": {
                "doctype": "Quotation"
            }
        },  # Removed the duplicate 'Lead Material Details' mapping
        target_doc,  
        set_missing_values  
    )

    return target_doc

