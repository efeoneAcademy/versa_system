

import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def map_quotation_to_final_design(source_name, target_doc=None):
    '''
        Method: Method to map a Quotation to a Final Design document.

        Args:
         source_name: The name of the Quotation document to be mapped.
         target_doc: The target document to which the Quotation should be mapped.

        Output: Name of the newly created Final Design document.
    '''
    def set_missing_values(source, target):
        pass

    target_doc = get_mapped_doc("Quotation", source_name,
        {
            "Quotation": {
                "doctype": "Final Design",
                "field_map": {
                    'from_lead': 'from_lead',  

                },
            },

        }, target_doc, set_missing_values)

    return target_doc
