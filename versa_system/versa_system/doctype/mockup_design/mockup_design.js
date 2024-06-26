// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mockup Design', {
    from_lead: function(frm) {
        /*
        * Function to populate child table on selecting Lead.
        */
        if (frm.doc.from_lead) {
            frappe.call({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.get_lead_properties',
                args: {
                    lead_name: frm.doc.from_lead
                },
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table("properties");

                        r.message.forEach(function(item) {
                            var row = frm.add_child("properties");
                            row.item_type = item.item_type;
                            row.item_code = item.item_code;
                            row.quantity = item.quantity;
                            row.low_range = item.low_range;
                            row.high_range = item.high_range;
                        });

                        frm.refresh_field("properties");
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('Properties', {
    create_raw_material: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frappe.new_doc('Raw Material Bundle', {
            'reference_doctype': 'Properties',
            'reference_name': row.name,
        });
    },

    show_features: function(frm, cdt, cdn) {
        /**
        * Function to display features for a selected property.
        * Fetches and displays feature details in a message box.
        */
        let row = locals[cdt][cdn];
        frappe.call({
            method: 'versa_system.versa_system.custom_scripts.lead.lead.fetch_feature_detail',
            args: {
                property_name: row.name  // Ensure this argument is correctly passed if required by your method
            },
            callback: function(response) {
                if (response.message && response.message.length > 0) {
                    let feature_html = '<table class="table table-bordered">';
                    feature_html += '<tr><th>Attribute</th><th>Value</th></tr>';
                    response.message.forEach(attr => {
                        feature_html += `<tr><td>${attr.attribute}</td><td>${attr.value}</td></tr>`;
                    });

                    feature_html += '</table>';

                    frappe.msgprint({
                        title: 'Features',
                        message: feature_html
                    });
                } else {
                    frappe.msgprint(__('No Features available for this property.'));
                }
            }
        });
    }
});

frappe.ui.form.on('Mockup Design', {
    onload: function(frm) {
        frm.set_query('from_lead', function() {
            return {
                filters: {
                    Status: ['in', ['Feasibility Check Approved', 'Quotation']]
                }
            };
        });
    }
});

frappe.ui.form.on('Mockup Design', {
    refresh: function(frm) {
        if (frm.doc.properties) {

            // Update docfield properties to hide the fields
            frm.fields_dict.properties.grid.update_docfield_property('final_design', 'hidden', 1);
            frm.fields_dict.properties.grid.update_docfield_property('create_size_chart', 'hidden', 1);
            frm.fields_dict.properties.grid.update_docfield_property('create_features', 'hidden', 1);
            frm.fields_dict.properties.grid.update_docfield_property('low_range', 'hidden', 1);
            frm.fields_dict.properties.grid.update_docfield_property('high_range', 'hidden', 1);
        }
    }
});
