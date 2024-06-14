// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt


frappe.ui.form.on('Mockup Design', {
    from_lead: function(frm) {
      /*
      * Function to populate  child table on selecting Lead.
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
