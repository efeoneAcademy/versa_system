// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt


frappe.ui.form.on('Mockup Design', {
    from_lead: function(frm) {
        if (frm.doc.from_lead) {
            frappe.call({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.get_lead_properties',
                args: {
                    lead_name: frm.doc.from_lead
                },
                callback: function(r) {
                    console.log('Response received:', r);
                    if (r.message) {
                        frm.clear_table("properties");

                        r.message.forEach(function(item) {
                            var row = frm.add_child("properties");
                            row.item_type = item.item_type;
                            row.material_type = item.material_type;
                            row.design = item.design;
                            row.model = item.model;
                            row.brand = item.brand;
                            row.size_chart = item.size_chart;
                            row.colour = item.colour;
                        });

                        frm.refresh_field("properties");
                    }
                }
            });
        }
    }
});
