import frappe
from frappe.model.document import Document
from frappe import _
from frappe.model.mapper import get_mapped_doc

class FeasibilityCheck(Document):
    def on_update(self):
        """Update lead status when the feasibility check is updated."""
        update_lead_status_on_feasibility_check(self)

@frappe.whitelist()
def map_feasibility_to_mockup_design(source_name, target_doc=None):
    """
    Map fields from Feasibility Check DocType to Mockup Design DocType,
    including only approved rows from the 'Enquiry Details' child table.
    """
    def set_missing_values(source, target):
        """
        Set additional values for the target if needed.
        For example, you can populate specific fields in the target document.
        """
        target.from_feasibility_check = source.name

    def filter_approved_items(source, target, source_parent):
        """
        Only map rows where the 'approve' checkbox is checked in the child table.
        This function defines how each child row is processed.
        """
        if source.approve:
            target.item = source.item
            target.brand = source.brand
            target.rate_range = source.rate_range
            target.design = source.design
            target.model = source.model
            target.size = source.size
            target.colour = source.colour
            target.material = source.material
            target.made_machinehand = source.made_machinehand
            target.image = source.image

    # Map Feasibility Check to Mockup Design
    target_doc = get_mapped_doc(
        "Feasibility Check",
        source_name,
        {
            "Feasibility Check": {
                "doctype": "Mockup Design",
                "field_map": {}
            },
            "Enqury Details": {  # Ensure the child table doctype names are correct
                "doctype": "Enqury Details",  # Match the target child table doctype
                "postprocess": filter_approved_items,  # Process only approved items
                "condition": lambda doc: doc.approve  # Map rows where 'approve' is checked
            }
        },
        target_doc,
        set_missing_values  # Apply missing values after mapping
    )
    # Set the ignore_mandatory flag
    target_doc.flags.ignore_mandatory = True
    # Save the mapped document
    target_doc.save(ignore_permissions=True)
    # Return the mapped document to the frontend
    return target_doc

def update_lead_status_on_feasibility_check(doc):
    """Update the status of the associated lead when the feasibility check is approved or rejected."""
    if doc.from_lead:
        # Fetch the linked lead document
        lead = frappe.get_doc("Lead", doc.from_lead)

        # Update status based on workflow state
        if doc.workflow_state == "Approved":
            lead.status = "Feasibility Check Approved"  # Correct status
        elif doc.workflow_state == "Rejected":
            lead.status = "Feasibility Check Rejected"  # Correct status

        lead.save()
