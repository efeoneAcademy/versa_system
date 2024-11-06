import frappe
from frappe import _
import json  # Import json module for parsing

@frappe.whitelist()
def update_lead(lead_name, details):
    # Check if the lead_name and details are provided
    if not lead_name or not details:
        frappe.throw(_('Lead name and details must be provided.'))

    # Fetch the Lead document
    lead = frappe.get_doc('Lead', lead_name)

    if not lead:
        frappe.throw(_('Lead not found: {0}').format(lead_name))

    # Parse the details string into a Python object
    try:
        details = json.loads(details)  # Convert JSON string to Python list
    except json.JSONDecodeError:
        frappe.throw(_('Invalid details format. Please provide valid JSON.'))

    # Clear existing child table entries
    lead.custom_enquiry_details = []

    # Update the Lead's child table with new details
    for row in details:
        lead.append('custom_enquiry_details', {
            'item': row.get('item'),
            'brand': row.get('brand'),
            'rate_range': row.get('rate_range'),
            'design': row.get('design'),
            'model': row.get('model'),
            'approve': row.get('approve')
        })

    # Save the updated Lead document
    lead.save()
    frappe.msgprint(_('Lead {0} updated successfully.').format(lead_name))