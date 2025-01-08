frappe.query_reports["Lead Status and Workflow Report"] = {
    filters: [
        {
            fieldname: "lead_status",
            label: __("Lead Status"),
            fieldtype: "Select",
            options: ["Open", "Converted", "Lost", "Do Not Contact"],
            default: "Open"
        },
        {
            fieldname: "lead_name",
            label: __("Lead Name"),
            fieldtype: "Data",
            placeholder: __("Enter Lead Name")
        },
        {
            fieldname: "creation_date",
            label: __("Creation Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "feasibility_check_id",
            label: __("Feasibility Check ID"),
            fieldtype: "Link",
            options: "Feasibility Check"
        },
        {
            fieldname: "mockup_workflow",
            label: __("Mockup Design Workflow"),
            fieldtype: "Data"
        },


        {
            fieldname: "quotation_id",
            label: __("Quotation ID"),
            fieldtype: "Link",
            options: "Quotation"
        },
        {
            fieldname: "quotation_date",
            label: __("Quotation Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "quotation_workflow_state",
            label: __("Quotation Workflow State"),
            fieldtype: "Select",
            options: ["Draft", "Submitted", "Cancelled", "To Be Billed"]
        },
        {
            fieldname: "quotation_amount",
            label: __("Quotation Amount"),
            fieldtype: "Currency"
        }
    ],
