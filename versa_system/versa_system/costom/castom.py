import frappe

def create_work_order_from_sales_order(doc, method, is_from_sales_order=True):
    """
    Create Work Orders from Sales Order items,
    linking the Sales Order to the Work Order and setting the Work Order status to Draft.
    Skips creation if a Work Order for the item already exists.
    """
    
    if not is_from_sales_order:
        frappe.msgprint("Work Order creation is not triggered from Sales Order.")
        return

    for item in doc.items:
        # Check if the quantity is greater than zero
        if item.qty > 0:
            # Check if a Work Order already exists for this Sales Order and item
            existing_work_order = frappe.db.exists("Work Order", {
                "sales_order": doc.name,
                "production_item": item.item_code
            })
            if existing_work_order:
                frappe.msgprint(f"Work Order for {item.item_code} already exists.")
                continue  # Skip creating if it already exists

            # Create Work Order
            work_order = frappe.new_doc("Work Order")
            work_order.production_item = item.item_code  # Set the production item
            work_order.qty = item.qty  # Set the quantity to manufacture
            work_order.sales_order = doc.name  # Link the Work Order to the Sales Order
            work_order.company = doc.company  # Set company same as Sales Order
            
            # Set the Work Order status to Draft
            work_order.workflow_state = "Draft"  # Set state to Draft

            # Optionally set additional fields as required
            # work_order.some_field = value
            
            work_order.insert()  # Insert the Work Order in Draft state
            frappe.msgprint(f"Work Order created for {item.item_code} in Draft state.")
