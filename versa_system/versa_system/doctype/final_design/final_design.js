// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Design', {
    from_lead: function(frm) {
        /*
        * Function to populate child table on selecting Lead.
        */
        if (frm.doc.from_lead) {
            // Fetch Lead Properties
            frappe.call({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.get_lead_properties',
                args: {
                    lead_name: frm.doc.from_lead
                },
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table("properties_table");

                        r.message.forEach(function(item) {
                            var row = frm.add_child("properties_table");
                            row.item_type = item.item_type;
                            row.material_type = item.material_type;
                            row.design = item.design;
                            row.model = item.model;
                            row.brand = item.brand;
                            row.size_chart = item.size_chart;
                            row.colour = item.colour;
                        });

                        frm.refresh_field("properties_table");
                    } else {
                        frappe.msgprint(__('No properties found for this Lead.'));
                    }
                }
            });

            // Fetch the relevant Quotation for the Lead
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Quotation',
                    filters: {
                        party_name: frm.doc.from_lead
                    },
                    fields: ['name']
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let quotation_name = r.message[0].name;

                        // Fetch Quotation Items from the Quotation
                        frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                doctype: 'Quotation',
                                name: quotation_name
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frm.clear_table('quotation_items');
                                    $.each(r.message.items || [], function(i, d) {
                                        let row = frm.add_child('quotation_items');
                                        row.item_code = d.item_code;
                                        row.item_name = d.item_name;
                                        row.qty = d.qty;
                                        row.rate = d.rate;
                                        row.uom = d.uom;
                                        row.conversion_factor = d.conversion_factor;
                                    });
                                    frm.refresh_field('quotation_items');
                                } else {
                                    frappe.msgprint(__('No items found in the Quotation.'));
                                }
                            }
                        });
                    } else {
                        frappe.msgprint(__('No Quotation found for this Lead.'));
                    }
                }
            });
        }
    }
});
