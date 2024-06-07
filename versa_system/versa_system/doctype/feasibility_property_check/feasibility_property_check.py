# Copyright (c) 2024, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FeasibilityPropertyCheck(Document):
	def on_update(self):
	    if self.workflow_state == "Approved":
	        # Fetch the related lead document
	        lead = frappe.get_doc("Lead", self.from_lead)

	        # Update the lead status0
	        lead.status = "Feasibility Check Approved"

	        # Save the changes to the lead document
	        lead.save()

	        # Optionally, you can add a comment to the lead document
	        lead.add_comment('Comment', 'Feasibility check approved and status updated.')

	    if self.workflow_state == "Rejected":
	        # Fetch the related lead document
	        lead = frappe.get_doc("Lead", self.from_lead)

	        # Update the lead status0
	        lead.status = "Feasibility Check Rejected"

	        # Save the changes to the lead document
	        lead.save()

	        # Optionally, you can add a comment to the lead document
	        lead.add_comment('Comment', 'Feasibility check rejected and status updated.')
