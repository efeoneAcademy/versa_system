import frappe
from frappe.model.document import Document

class FeasibilityCheck(Document):

    def on_update(self):
        "IF the feasibility Check is Approved then the mockup design will be created "
        if self.workflow_state == 'Approved':
            # Create the Mockup Design document
            moc_design = frappe.get_doc({
                'doctype': 'Mockup Design',
                'from_lead': self.from_lead,
                'material': self.material  # Fetching material data from FeasibilityCheck
            })

            # Insert the new Mockup Design document
            moc_design.insert(ignore_permissions=True)
            frappe.msgprint(f'Mockup Design {moc_design.from_lead} created successfully.')
