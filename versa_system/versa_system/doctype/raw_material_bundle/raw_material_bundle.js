// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Raw Material Bundle', {
    onload: function(frm) {
        frm.set_query('reference_doctype', function() {
            return {
                "filters": {
                    module: 'Versa System'
                }
            };
        });
    }
});

frappe.ui.form.on('Raw Material', {
    quantity: function(frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        let amt = d.quantity * d.rate;
        frappe.model.set_value(cdt, cdn, 'total_amount', amt);
        frm.refresh_field('raw_material'); // Refresh the raw_material field
    },
    rate: function(frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        let amt = d.quantity * d.rate;
        frappe.model.set_value(cdt, cdn, 'total_amount', amt);
        frm.refresh_field('raw_material'); // Refresh the raw_material field
    }
});
