import frappe

def execute(filters=None):
    """
    Main function to execute the report. It defines the columns and fetches the data.
    """
    columns = get_columns()  # Define the columns for the report
    data = get_data(filters)  # Fetch the data for the report
    return columns, data

def get_columns():
    """
    Defines the columns to be displayed in the report.
    """
    return [
        {"label": "Lead ID", "fieldname": "lead_id", "fieldtype": "Link", "options": "Lead", "width": 200},
        {"label": "Lead Name", "fieldname": "lead_name", "fieldtype": "Data", "width": 200},
        {"label": "Item", "fieldname": "item", "fieldtype": "Data", "width": 200},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 200},
        {"label": "Creation Date", "fieldname": "creation", "fieldtype": "Datetime", "width": 180},
        {"label": "Feasibility Check ID", "fieldname": "feasibility_check_id", "fieldtype": "Link", "options": "Feasibility Check", "width": 200},
        {"label": "Feasibility Workflow", "fieldname": "feasibility_workflow", "fieldtype": "Data", "width": 200},
        {"label": "Mockup Workflow", "fieldname": "mockup_workflow", "fieldtype": "Data", "width": 150},
        {"label": "Mockup Design ID", "fieldname": "mockup_design_id", "fieldtype": "Link", "options": "Mockup Design", "width": 150},
        {"label": "Quotation ID", "fieldname": "quotation_name", "fieldtype": "Link", "options": "Quotation", "width": 200},
        {"label": "Quotation Status", "fieldname": "quotation_status", "fieldtype": "Data", "width": 150},
        {"label": "Quotation Date", "fieldname": "quotation_date", "fieldtype": "Date", "width": 150},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Final Design ID", "fieldname": "final_design_name", "fieldtype": "Link", "options": "Final Design", "width": 200},
        {"label": "Approval Status", "fieldname": "approval_status", "fieldtype": "Data", "width": 150},
        {"label": "Sales Order ID", "fieldname": "sales_order_name", "fieldtype": "Link", "options": "Sales Order", "width": 200},
        {"label": "Sales Order Status", "fieldname": "sales_order_status", "fieldtype": "Data", "width": 150},
        {"label": "Sales Order Date", "fieldname": "sales_order_date", "fieldtype": "Date", "width": 150},
        {"label": "Work Order ID", "fieldname": "work_order_id", "fieldtype": "Link", "options": "Work Order", "width": 200},
        {"label": "Work Order Status", "fieldname": "work_order_status", "fieldtype": "Data", "width": 150},
        {"label": "Actual Start Date", "fieldname": "actual_start_date", "fieldtype": "Datetime", "width": 180},
        {"label": "Actual End Date", "fieldname": "actual_end_date", "fieldtype": "Datetime", "width": 180},
        {"label": "BOM ID", "fieldname": "bom_number", "fieldtype": "Link", "options": "BOM", "width": 200},
        {"label": "Sales Invoice ID", "fieldname": "sales_invoice_id", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": "Delivery Note ID", "fieldname": "delivery_note_id", "fieldtype": "Link", "options": "Delivery Note", "width": 200},
        {"label": "Delivery Note Status", "fieldname": "delivery_note_status", "fieldtype": "Data", "width": 200},  # New column for Delivery Note Status
    ]

def get_data(filters=None):
    """
    Fetches the data to be displayed in the report.
    """
    query = """
        SELECT
            l.name AS lead_id,
            l.lead_name AS lead_name,
            l.status,
            l.creation,
            fc.workflow_state AS feasibility_workflow,
            fc.name AS feasibility_check_id,
            CASE
                WHEN fc.workflow_state = 'Approved' THEN md.workflow_state
                WHEN fc.workflow_state = 'Rejected' THEN 'No Mockup Design'
                ELSE 'Not Started'
            END AS mockup_workflow,
            md.name AS mockup_design_id,
            ed.item,
            q.name AS quotation_name,
            q.status AS quotation_status,
            q.transaction_date AS quotation_date,
            q.grand_total AS total_amount,
            fd.name AS final_design_name,
            fd.workflow_state AS approval_status,
            so.name AS sales_order_name,
            so.status AS sales_order_status,
            so.transaction_date AS sales_order_date,
            wo.name AS work_order_id,
            wo.status AS work_order_status,
            wo.actual_start_date AS actual_start_date,
            wo.actual_end_date AS actual_end_date,
            wo.bom_no AS bom_number,
            si.name AS sales_invoice_id,
            dn.name AS delivery_note_id,
            dn.status AS delivery_note_status
        FROM
            `tabLead` l
        LEFT JOIN
            `tabFeasibility Check` fc ON fc.from_lead = l.name
        LEFT JOIN
            `tabMockup Design` md ON md.from_lead = l.name AND fc.workflow_state = 'Approved'
        LEFT JOIN
            `tabEnqury Details` ed ON ed.parent = l.name
        LEFT JOIN
            `tabQuotation` q ON q.party_name = l.name
        LEFT JOIN
            `tabFinal Design` fd ON fd.from_lead = l.name
        LEFT JOIN
            `tabSales Order` so ON so.customer_name = q.customer_name
        LEFT JOIN
            `tabWork Order` wo ON wo.sales_order = so.name
        LEFT JOIN
            `tabSales Invoice` si ON si.customer_name = so.customer_name
        LEFT JOIN
            `tabDelivery Note` dn ON dn.customer_name = so.customer_name
        ORDER BY
            l.creation DESC, ed.idx
    """
    return frappe.db.sql(query, as_dict=True)
