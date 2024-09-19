import frappe
from frappe.model.document import Document

class FeasibilityCheck(Document):

    def on_update(self):
        "IF the feasibility Check is Approved then the moc design will be created "
        if self.workflow_state == 'Approved':
                    moc_design = frappe.get_doc({
                        'doctype': 'Mockup Design',
                        'from_lead': self.from_lead
                    })
                    
                    moc_design.insert(ignore_permissions=True)
                    frappe.msgprint(f'Mockup Design {moc_design.from_lead} created successfully.')
                
