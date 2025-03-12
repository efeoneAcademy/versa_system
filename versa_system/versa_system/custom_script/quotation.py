
import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_moc_design_to_quotation(source_name, target_doc=None):
    """
    Map fields from MOC Design to Quotation, ensuring rate_range and rate are the same.
    """

    def set_missing_values(source, target):
        target.party_name = source.lead
        
        lead_materials = frappe.get_all(
            "Lead Material Details",
            filters={"parent": source.name},  
            fields=["product_item", "size", "brand", "rate_range", "quantity", "image", "feasible"]
        )

        for item in lead_materials:
            item_code = item.get("product_item") 

            if not item_code:
                frappe.throw(f"Product Item is missing for an entry in Lead Material Details: {item}")

            item_details = frappe.get_value("Item", item_code, ["item_name", "stock_uom"], as_dict=True)

            if not item_details:
                frappe.throw(f"Item {item_code} not found in Item Master.")

            if hasattr(target, "material_item"):
                target.append("material_item", {
                    "product_item": item_code,  
                    "size": item.get("size"),
                    "brand": item.get("brand"),
                    "rate_range": item.get("rate_range"),
                    "image": item.get("image"),
                    "feasible": item.get("feasible"),
                    "quantity": item.get("quantity")
                })

            if hasattr(target, "items"):
                target.append("items", {  
                    "item_code": item_code,  
                    "item_name": item_details["item_name"],  
                    "rate": item.get("rate_range"),
                    "qty": item.get("quantity"),
                    "uom": item_details["stock_uom"]  
                })

    target_doc = get_mapped_doc(
        "MOC Design", source_name,
        {
            "MOC Design": {
                "doctype": "Quotation",
                "field_map": {
                    "lead": "party_name"  
                }
            }
        },
        target_doc,  
        set_missing_values  
    )

    return target_doc
