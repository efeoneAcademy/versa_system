import os
import click
import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    create_custom_fields(get_versa_custom_fields(), ignore_validate=True)

def after_migrate():
    after_install()

def before_uninstall():
    delete_custom_fields(get_versa_custom_fields())

def delete_custom_fields(custom_fields: dict):
    '''
    Method to Delete custom fields
    args:
        custom_fields: a dict like {'Your Doctype': [{fieldname: 'your_fieldname', ...}]}
    '''
    for doctype, fields in custom_fields.items():
        frappe.db.delete(
            "Custom Field",
            {
                "fieldname": ("in", [field["fieldname"] for field in fields]),
                "dt": doctype,
            },
        )
        frappe.clear_cache(doctype=doctype)

def get_versa_custom_fields():
    '''
    Custom fields that need to be added to the Lead Doctype in the Versa module
    '''
    return {
        "Lead": [
            {
                "fieldname": "custom_enquiry_details",
                "fieldtype": "Table",
                "label": "Enquiry Details",
                "options": "Enquiry Details",  # Assuming 'Enquiry Details' is the child doctype
                "insert_after": "request_type"
            },
            {
                "fieldname": "salutation",
                "fieldtype": "Select",
                "label": "Salutation",
                "options": "\nMr.\nMrs.\nMs.\nDr.",
                "insert_after": "naming_series"
            },
            {
                "fieldname": "gender",
                "fieldtype": "Select",
                "label": "Gender",
                "options": "\nMale\nFemale\nOther",
                "insert_after": "last_name"
            },
            {
                "fieldname": "no_of_employees",
                "fieldtype": "Select",
                "label": "No of Employees",
                "options": "\n1-10\n11-50\n51-200\n201-500\n501-1000\n1001+",
                "insert_after": "company_name"
            },
            {
                "fieldname": "annual_revenue",
                "fieldtype": "Currency",
                "label": "Annual Revenue",
                "insert_after": "no_of_employees"
            },
            {
                "fieldname": "industry",
                "fieldtype": "Link",
                "label": "Industry",
                "options": "Industry",
                "insert_after": "annual_revenue"
            },
            {
                "fieldname": "market_segment",
                "fieldtype": "Link",
                "label": "Market Segment",
                "options": "Market Segment",
                "insert_after": "industry"
            },
            {
                "fieldname": "territory",
                "fieldtype": "Link",
                "label": "Territory",
                "options": "Territory",
                "insert_after": "market_segment"
            },
            {
                "fieldname": "fax",
                "fieldtype": "Data",
                "label": "Fax",
                "insert_after": "phone_ext"
            }
        ]
    }
