frappe.query_reports["Lead Status Details"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "lead_id",
            label: __("Lead ID"),
            fieldtype: "Link",
            options: "Lead"
        },
        {
            fieldname: "item",
            label: __("Item"),
            fieldtype: "Link",
						options: "Item"
        },
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company"
        },
        {
            fieldname: "quotation_date",
            label: __("Quotation Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "sales_order_id",
            label: __("Sales Order ID"),
            fieldtype: "Link",
            options: "Sales Order"
        },
        {
            fieldname: "work_order_id",
            label: __("Work Order ID"),
            fieldtype: "Link",
            options: "Work Order"
        },
        {
            fieldname: "bom_id",
            label: __("BOM ID"),
            fieldtype: "Link",
            options: "BOM"
        },
        {
            fieldname: "delivery_note_id",
            label: __("Delivery Note ID"),
            fieldtype: "Link",
            options: "Delivery Note"
        },
				{
            "fieldname": "sales_invoice_id",
            "label": __("Sales Invoice ID"),
            "fieldtype": "Link",
            "options": "Sales Invoice"
        }
    ]
}
