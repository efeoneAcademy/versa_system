# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class MockupDesign(Document):
    def on_update(self):
        if self.workflow_state == "Approved":
            # Fetch the related lead document
            lead = frappe.get_doc("Lead", self.from_lead)

            # Update the lead status0
            lead.status = "Mockup Design Approved"

            # Save the changes to the lead document
            lead.save()

            # Optionally, you can add a comment to the lead document
            lead.add_comment('Comment', 'Mockup Design approved and status updated.')

        if self.workflow_state == "Rejected":
            # Fetch the related lead document
            lead = frappe.get_doc("Lead", self.from_lead)

            # Update the lead status0
            lead.status = "Mockup Design Rejected"

            # Save the changes to the lead document
            lead.save()

            # Optionally, you can add a comment to the lead document
            lead.add_comment('Comment', 'Mockup Design rejected and status updated.')


        if self.workflow_state == "Pending":
            # Fetch the related lead document
            lead = frappe.get_doc("Lead", self.from_lead)

            # Update the lead status0
            lead.status = "Mockup Design Pending"

            # Save the changes to the lead document
            lead.save()

            # Optionally, you can add a comment to the lead document
            lead.add_comment('Comment', 'Mockup Design Pending and status updated.')
