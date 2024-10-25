# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class MockupDesign(Document):
    pass

@frappe.whitelist()
def map_mockup_design_to_quotation(source_name, target_doc=None):
    """
    Map fields from Mockup Design DocType to Quotation DocType.
    """
    def set_missing_values(source, target):
        target.quotation_to = "Mockup Design"
        target.party_name = source.name
        target.customer_name = source.from_lead
    target_doc = get_mapped_doc("Mockup Design", source_name,
        {
            "Mockup Design": {
                "doctype": "Quotation",
                "field_map": {
                    "from_lead": "party_name"
                },
            },
        }, target_doc, set_missing_values)

    return target_doc
import frappe
from frappe.model.document import Document

class MockupDesign(Document):
    def on_update(self):
        # Call the function to update lead status when the document is updated
        update_lead_status_on_mockup_design(self)

def update_lead_status_on_mockup_design(doc):
    """Update the status of the associated lead when the mockup design is approved or rejected."""
    if doc.from_lead:
        try:
            # Fetch the linked lead document
            lead = frappe.get_doc("Lead", doc.from_lead)
            
            # Update status based on workflow state
            if doc.workflow_state == "Approved":
                lead.status = "Mockup Design Approved"
            elif doc.workflow_state == "Rejected":
                lead.status = "Mockup Design Rejected"
            
            lead.save()

            # Display success message
            frappe.msgprint(
                f"Lead {lead.name} status updated to '{lead.status}'.",
                alert=True
            )
        except frappe.DoesNotExistError:
            frappe.throw(f"The lead {doc.from_lead} does not exist.")
        except Exception as e:
            # Log the error for debugging purposes
            frappe.log_error(f"Failed to update lead status: {str(e)}")
            frappe.throw("An error occurred while updating the lead status.")
