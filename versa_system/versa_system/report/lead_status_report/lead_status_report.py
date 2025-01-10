
import frappe

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Lead ID", "fieldname": "lead_id", "fieldtype": "Link", "options": "Lead", "width": 150},
        {"label": "Lead Name", "fieldname": "lead_name", "fieldtype": "Data", "width": 200},
        {"label": "Lead Owner", "fieldname": "lead_owner", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": "Lead Status", "fieldname": "lead_status", "fieldtype": "Select", "options": "Open\nWorking\nClosed", "width": 100},
        {"label": "Creation Date", "fieldname": "creation", "fieldtype": "Datetime", "width": 150},

        # Feasibility Check fields
        {"label": "Feasibility Check ID", "fieldname": "feasibility_check_id", "fieldtype": "Link", "options": "Feasibility Check", "width": 150},
        {"label": "Feasibility Workflow", "fieldname": "feasibility_workflow", "fieldtype": "Data", "width": 150},

        # Quotation fields
        {"label": "Quotation ID", "fieldname": "quotation_id", "fieldtype": "Link", "options": "Quotation", "width": 150},
        {"label": "Quotation Date", "fieldname": "quotation_date", "fieldtype": "Date", "width": 150},
        {"label": "Quotation Workflow", "fieldname": "quotation_workflow", "fieldtype": "Data", "width": 150},
        {"label": "Quotation Amount", "fieldname": "quotation_total_amount", "fieldtype": "Currency", "width": 150},

        # Design Request fields
        {"label": "Final Design ID", "fieldname": "final_design_id", "fieldtype": "Link", "options": "Design Request", "width": 150},
        {"label": "Final Design Workflow", "fieldname": "final_design_workflow", "fieldtype": "Data", "width": 150},
        {"label": "Mockup Design ID", "fieldname": "mockup_design_id", "fieldtype": "Link", "options": "Design Request", "width": 150},
        {"label": "Mockup Design Workflow", "fieldname": "mockup_design_workflow", "fieldtype": "Data", "width": 150},

        # Sales Order fields
        {"label": "Sales Order ID", "fieldname": "sales_order_name", "fieldtype": "Link", "options": "Sales Order", "width": 200},
        {"label": "Sales Order Status", "fieldname": "sales_order_status", "fieldtype": "Data", "width": 150},
        {"label": "Sales Order Date", "fieldname": "sales_order_date", "fieldtype": "Date", "width": 150},

        # Sales Invoice fields
        {"label": "Sales Invoice ID", "fieldname": "sales_invoice_id", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": "Sales Invoice Status", "fieldname": "sales_invoice_status", "fieldtype": "Data", "width": 150},

        # Work Order fields
        {"label": "Work Order ID", "fieldname": "work_order_id", "fieldtype": "Link", "options": "Work Order", "width": 200},
        {"label": "Work Order Status", "fieldname": "work_order_status", "fieldtype": "Data", "width": 150},
        {"label": "Actual Start Date", "fieldname": "actual_start_date", "fieldtype": "Datetime", "width": 180},
        {"label": "Actual End Date", "fieldname": "actual_end_date", "fieldtype": "Datetime", "width": 180},

        # Delivery Note fields
        {"label": "Delivery Note ID", "fieldname": "delivery_note_id", "fieldtype": "Link", "options": "Delivery Note", "width": 200},
        {"label": "Delivery Note Date", "fieldname": "delivery_note_date", "fieldtype": "Date", "width": 150},
        {"label": "Delivery Note Status", "fieldname": "delivery_note_status", "fieldtype": "Data", "width": 150},
    ]

def get_data(filters=None):
    conditions = []
    params = {}

    # Dynamically build conditions based on filters
    if filters.get("lead_owner"):
        conditions.append("lead.lead_owner = %(lead_owner)s")
        params["lead_owner"] = filters.get("lead_owner")

    if filters.get("lead_status"):
        conditions.append("lead.status = %(lead_status)s")
        params["lead_status"] = filters.get("lead_status")

    if filters.get("quotation_id"):
        conditions.append("qt.name = %(quotation_id)s")
        params["quotation_id"] = filters.get("quotation_id")

    if filters.get("feasibility_check_id"):
        conditions.append("fc.name = %(feasibility_check_id)s")
        params["feasibility_check_id"] = filters.get("feasibility_check_id")

    if filters.get("sales_order_name"):
        conditions.append("so.name = %(sales_order_name)s")
        params["sales_order_name"] = filters.get("sales_order_name")

    if filters.get("sales_invoice_id"):
        conditions.append("si.name = %(sales_invoice_id)s")
        params["sales_invoice_id"] = filters.get("sales_invoice_id")

    if filters.get("work_order_id"):
        conditions.append("wo.name = %(work_order_id)s")
        params["work_order_id"] = filters.get("work_order_id")

    if filters.get("delivery_note_id"):
        conditions.append("dn.name = %(delivery_note_id)s")
        params["delivery_note_id"] = filters.get("delivery_note_id")

    if filters.get("final_design_id"):
        conditions.append("""
            (SELECT name FROM `tabDesign Request`
             WHERE type = 'Final Design' AND lead = lead.name LIMIT 1) = %(final_design_id)s
        """)
        params["final_design_id"] = filters.get("final_design_id")

    # Combine conditions
    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = f"WHERE {where_clause}"

    query = f"""
    SELECT
        lead.name AS lead_id,
        lead.lead_name,
        lead.lead_owner,
        lead.status AS lead_status,
        lead.creation,

        -- Feasibility Check
        fc.name AS feasibility_check_id,
        fc.workflow_state AS feasibility_workflow,

        -- Quotation
        qt.name AS quotation_id,
        qt.transaction_date AS quotation_date,
        qt.workflow_state AS quotation_workflow,
        qt.total AS quotation_total_amount,

        -- Final Design
        (SELECT name FROM `tabDesign Request`
         WHERE type = 'Final Design' AND lead = lead.name LIMIT 1) AS final_design_id,
        (SELECT workflow_state FROM `tabDesign Request`
         WHERE type = 'Final Design' AND lead = lead.name LIMIT 1) AS final_design_workflow,

        -- Mockup Design
        (SELECT name FROM `tabDesign Request`
         WHERE type = 'Mockup Design' AND lead = lead.name LIMIT 1) AS mockup_design_id,
        (SELECT workflow_state FROM `tabDesign Request`
         WHERE type = 'Mockup Design' AND lead = lead.name LIMIT 1) AS mockup_design_workflow,

        -- Sales Order
        so.name AS sales_order_name,
        so.status AS sales_order_status,
        so.transaction_date AS sales_order_date,

        -- Sales Invoice
        si.name AS sales_invoice_id,
        si.status AS sales_invoice_status,

        -- Work Order
        wo.name AS work_order_id,
        wo.status AS work_order_status,
        wo.actual_start_date AS actual_start_date,
        wo.actual_end_date AS actual_end_date,

        -- Delivery Note
        dn.name AS delivery_note_id,
        dn.posting_date AS delivery_note_date,
        dn.status AS delivery_note_status

    FROM
        `tabLead` AS lead
    LEFT JOIN
        `tabFeasibility Check` AS fc ON fc.lead = lead.name
    LEFT JOIN
        `tabQuotation` AS qt ON qt.party_name = lead.name
    LEFT JOIN
        `tabSales Order` so ON so.customer_name = qt.customer_name
    LEFT JOIN
        `tabSales Invoice` si ON si.customer_name = qt.customer_name
    LEFT JOIN
        `tabWork Order` wo ON wo.sales_order = so.name
    LEFT JOIN
        `tabDelivery Note` dn ON dn.customer_name = qt.customer_name

    {where_clause}

    ORDER BY
        lead.creation DESC
    LIMIT 50
    """
    return frappe.db.sql(query, params, as_dict=True)
