import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    def on_update(self):
        """Update lead status when the feasibility check is updated."""
        update_lead_status_on_feasibility_check(self)


@frappe.whitelist()
def map_feasibility_to_mockup_design(source_name, target_doc=None):
    """
    Map fields from Feasibility Check DocType to Mockup Design DocType,
    including the child table 'Enquiry Details' and its data.
    """
    def set_missing_values(source, target):
        # Set any missing values if needed
        pass

    target_doc = get_mapped_doc("Feasibility Check", source_name,
        {
            "Feasibility Check": {
                "doctype": "Mockup Design",
                "field_map": {}
            },
            "Enqury Details": {  # Mapping the child table
                "doctype": "Enqury Details",  # Ensure this matches the target child table in Mockup Design
                "field_map": {
                    "item": "item",
                    "material": "material",
                    "brand": "brand",
                    "model": "model",
                    "rate_range": "rate_range",
                    "size": "size",
                    "colour": "colour",
                    "design": "design",
                }
            }
        }, target_doc, set_missing_values)

    return target_doc
    
import frappe
from frappe.model.document import Document

class FeasibilityCheck(Document):
    def on_update(self):
        # Call the update lead status function when the document is updated
        update_lead_status_on_feasibility_check(self)

def update_lead_status_on_feasibility_check(doc):
    """Update the status of the associated lead when the feasibility check is approved or rejected."""
    if doc.from_lead:
        try:
            # Fetch the linked lead document
            lead = frappe.get_doc("Lead", doc.from_lead)
            
            # Update status based on workflow state
            if doc.workflow_state == "Approved":
                lead.status = "Feasibility Check Approved"
            elif doc.workflow_state == "Rejected":
                lead.status = "Feasibility Check Rejected"
            
            lead.save()

            # Display success message
            frappe.msgprint(
                f"Lead {lead.name} status updated to '{lead.status}'.",
                alert=True
            )
        except frappe.DoesNotExistError:
            frappe.throw(f"The lead {doc.from_lead} does not exist.")
        except Exception as e:
            frappe.log_error(f"Failed to update lead status: {str(e)}")
            frappe.throw("An error occurred while updating the lead status.")
