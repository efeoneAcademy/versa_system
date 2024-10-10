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
        target.party_name = source.from_lead

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
