import frappe

@frappe.whitelist()
def get_only_products(doctype, txt='', searchfield='name', start=0, page_len=20, filters=None):
    """
    Fetch only 'Products' from the Item doctype.
    """
    items = frappe.db.get_list(
        "Item",
        filters={"item_group": "Products"},  
        fields=["name"],
        order_by="modified DESC",
        start=start,
        page_length=page_len
    )

    return [(item["name"],) for item in items]  
