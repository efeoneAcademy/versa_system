frappe.query_reports["Lead Status Report"] = {
  filters: [
    {
         fieldname: "lead_owner",
         label: __("Lead Owner"),
         fieldtype: "Link",
         options: "User",
       },
       {
         fieldname: "lead_status",
         label: __("Lead Status"),
         fieldtype: "Select",
         options: ["", "Open", "Replied", "Opportunity","Lost","Quotation","Interested","Converted","Do Not Contact"],
       },
       {
         fieldname: "quotation_date_from",
         label: __("Quotation Date From"),
         fieldtype: "Date",
       },
       {
         fieldname: "quotation_date_to",
         label: __("Quotation Date To"),
         fieldtype: "Date",
       },
       {
         fieldname: "quotation_id",
         label: __("Quotation ID"),
         fieldtype: "Link",
         options: "Quotation",
       },
       {
         fieldname: "feasibility_check_id",
         label: __("Feasibility Check ID"),
         fieldtype: "Link",
         options: "Feasibility Check",
       },
       {
         fieldname: "sales_order_name",
         label: __("Sales Order ID"),
         fieldtype: "Link",
         options: "Sales Order",
       },
       {
         fieldname: "sales_invoice_id",
         label: __("Sales Invoice ID"),
         fieldtype: "Link",
         options: "Sales Invoice",
       },
       {
         fieldname: "work_order_id",
         label: __("Work Order ID"),
         fieldtype: "Link",
         options: "Work Order",
       },
       {
         fieldname: "delivery_note_id",
         label: __("Delivery Note ID"),
         fieldtype: "Link",
         options: "Delivery Note",
       },
       {
         fieldname: "final_design_id",
         label: __("Final Design ID"),
         fieldtype: "Link",
         options: "Design Request",
       }
  ]
};
