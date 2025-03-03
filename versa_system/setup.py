import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe import _

# After Install
def after_install():
    """Runs after the app is installed."""
    create_property_setters(get_property_setters())

def after_migrate():
    """Runs after migration."""
    after_install()

def get_property_setters():
    """
    Define specific property setters that need to be added to the Sales Order DocType only.
    """
    return [
        {
            "doctype_or_field": "DocField",
            "doc_type": "Sales Order",
            "field_name": "status",
            "property": "options",
            "value": "Draft\nOn Hold\nTo Deliver and Bill\nTo Bill\nTo Deliver\nCompleted\nCancelled\nClosed\nProforma Invoice"
        },
        {
            "doctype_or_field": "DocField",
            "doc_type": "Sales Order",
            "field_name": "status",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": 1
        }
    ]

def create_property_setters(property_setter_datas):
    """
    Method to create custom property setters.
    Args:
        property_setter_datas: list of dicts for property setter objects
    """
    for data in property_setter_datas:
        # Check for existing property setter based on relevant fields
        if frappe.db.exists("Property Setter", {
            "doc_type": data["doc_type"],
            "field_name": data["field_name"],
            "property": data["property"]
        }):
            continue

        try:
            property_setter = frappe.new_doc("Property Setter")
            property_setter.update(data)
            property_setter.flags.ignore_permissions = True
            property_setter.insert()
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Error creating property setter for {data['doc_type']} - {data['field_name']}: {str(e)}")