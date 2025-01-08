
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Lead ID", "fieldname": "lead_id", "fieldtype": "Link", "options": "Lead", "width": 200},
        {"label": "Lead Name", "fieldname": "lead_name", "fieldtype": "Data", "width": 200},
        {"label": "Lead Owner", "fieldname": "lead_owner", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": "Lead Status", "fieldname": "lead_status", "fieldtype": "Select", "width": 100},
        {"label": "Creation Date", "fieldname": "creation", "fieldtype": "Datetime", "width": 150},
        {"label": "Feasibility Check ID", "fieldname": "feasibility_check_id", "fieldtype": "Link", "options": "Feasibility Check", "width": 200},
        {"label": "Feasibility Workflow", "fieldname": "feasibility_workflow", "fieldtype": "Data", "width": 200},
        {"label": "Design Request ID", "fieldname": "design_request_id", "fieldtype": "Link", "options": "Design Request", "width": 200},
        {"label": "Mockup Design Workflow", "fieldname": "mockup_workflow", "fieldtype": "Data", "width": 150},
        {"label": "Quotation ID", "fieldname": "quotation_id", "fieldtype": "Link", "options": "Quotation", "width": 200},
        {"label": "Quotation Date", "fieldname": "quotation_date", "fieldtype": "Date", "width": 150},
        {"label": "Quotation Workflow", "fieldname": "quotation_workflow", "fieldtype": "Data", "width": 150},  # Updated field label
        {"label": "Quotation Amount", "fieldname": "quotation_amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    conditions, values = get_conditions(filters)


    query = """
        SELECT
            l.name AS lead_id,
            l.lead_name,
            l.lead_owner,
            l.status AS lead_status,
            l.creation,
            fc.name AS feasibility_check_id,
            fc.workflow_state AS feasibility_workflow,
            dr.name AS design_request_id,
            dr.workflow_state AS mockup_workflow,
            q.name AS quotation_id,
            q.transaction_date AS quotation_date,
            q.workflow_state AS quotation_workflow,
            q.net_total AS quotation_amount
        FROM
            `tabLead` l
        LEFT JOIN
            `tabFeasibility Check` fc ON fc.lead = l.name
        LEFT JOIN
            `tabDesign Request` dr ON dr.lead = l.name AND dr.type = 'Mockup Design'
        LEFT JOIN
            `tabQuotation` q ON q.party_name = l.name
        {conditions}
    """.format(conditions=conditions)

    # Log query for debugging
    frappe.logger().debug({"query": query, "values": values})

    # Execute query and return data
    try:
        return frappe.db.sql(query, values, as_dict=True)
    except Exception as e:
        frappe.logger().error(f"Error fetching report data: {e}")
        return []

def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("lead_status"):
        conditions.append("l.status = %(lead_status)s")
        values["lead_status"] = filters["lead_status"]
    if filters.get("lead_name"):
        conditions.append("l.lead_name LIKE %(lead_name)s")
        values["lead_name"] = f"%{filters['lead_name']}%"
    if filters.get("creation_date"):
        conditions.append("DATE(l.creation) = %(creation_date)s")
        values["creation_date"] = filters["creation_date"]
    if filters.get("feasibility_check_id"):
        conditions.append("fc.name = %(feasibility_check_id)s")
        values["feasibility_check_id"] = filters["feasibility_check_id"]
    if filters.get("design_request_id"):
        conditions.append("dr.name = %(design_request_id)s")
        values["design_request_id"] = filters["design_request_id"]
    if filters.get("quotation_id"):
        conditions.append("q.name = %(quotation_id)s")
        values["quotation_id"] = filters["quotation_id"]
    if filters.get("quotation_date"):
        conditions.append("DATE(q.transaction_date) = %(quotation_date)s")
        values["quotation_date"] = filters["quotation_date"]
    if filters.get("quotation_workflow"):
        conditions.append("q.workflow_state = %(quotation_workflow)s")
        values["quotation_workflow"] = filters["quotation_workflow"]
    if filters.get("quotation_amount"):
        conditions.append("q.net_total = %(quotation_amount)s")
        values["quotation_amount"] = filters["quotation_amount"]

    if conditions:
        return "WHERE " + " AND ".join(conditions), values
    else:
        return "", values
