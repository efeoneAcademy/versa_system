import frappe
from frappe.model.document import Document

@frappe.whitelist()
def update_sales_order_status_on_work_order_completion(doc, method):
    
    current_status = frappe.db.get_value("Work Order", doc.name, "status")

    if current_status == "Completed" and doc.sales_order:
        try:
            sales_order = frappe.get_doc("Sales Order", doc.sales_order)

            if sales_order.status != "Proforma Invoice":
                sales_order.status = "Proforma Invoice"
                sales_order.save(ignore_permissions=True)
                frappe.db.commit()
        except frappe.DoesNotExistError:
            pass
        except Exception as e:
            pass