
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def update_sales_order_status_on_work_order_completion(doc, method):
    frappe.log_error("Hook Triggered: update_sales_order_status_on_work_order_completion")
    frappe.log_error(f"Work Order Submitted. Current Status: {doc.status}, Sales Order: {doc.sales_order}")
    # Fetch the latest status directly from the database
    current_status = frappe.db.get_value("Work Order", doc.name, "status")
    frappe.log_error(f"Fetched Work Order Status from DB: {current_status}")

    if current_status == "Completed" and doc.sales_order:
        try:
            sales_order = frappe.get_doc("Sales Order", doc.sales_order)
            frappe.log_error(f"Fetched Sales Order: {sales_order.name}")

            # Check if status needs to be updated
            if sales_order.status != "Proforma Invoice":
                sales_order.status = "Proforma Invoice"
                sales_order.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.log_error(f"Sales Order {sales_order.name} status successfully updated to 'Proforma Invoice'")
            else:
                frappe.log_error(f"Sales Order {sales_order.name} is already in 'Proforma Invoice' status.")
        except frappe.DoesNotExistError:
            frappe.log_error(f"Sales Order {doc.sales_order} linked to Work Order {doc.name} does not exist.")
        except Exception as e:
            frappe.log_error(f"Error updating Sales Order status: {str(e)}")
    else:
        frappe.log_error("Conditions not met for Sales Order status update.")
