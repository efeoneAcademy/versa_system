import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe import _

# After Install
def after_install():
    """Runs after the app is installed."""
    create_property_setters(get_property_setters())
    create_custom_fields(get_quotion_custom_fields(), ignore_validate=True)
    create_roles()

def after_migrate():
    """Runs after migration."""
    after_install()

def before_uninstall():
    delete_custom_fields(get_quotion_custom_fields())

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


def get_quotion_custom_fields():
    '''
        Custom fields that need to be added to the Student Group DocType
    '''
    return {
        "Quotation": [
            {
                "fieldname": "item_details",
                "fieldtype": "Table",
                "label": "item Details",
                "insert_after": "scan_barcode",
                "options":"Item Details"
            }
        ]
    }


def create_roles():
    """Create custom roles required by the app."""
    roles = [
        {"role_name": "Buyer", "desk_access": 1},
        {"role_name": "Feasibility Analyst", "desk_access": 1}
    ]

    for role in roles:
        if not frappe.db.exists("Role", role["role_name"]):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role["role_name"],
                "desk_access": role.get("desk_access", 1),
                "restrict_to_domain": role.get("restrict_to_domain", None)
            }).insert(ignore_permissions=True)
            frappe.db.commit()
