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
        calculate_total_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_total_amount(frm, cdt, cdn);
    }
});

function calculate_total_amount(frm, cdt, cdn) {
  /*
  * Function to calculate total amount Based on quantity and rate.
  */
    let d = locals[cdt][cdn];
    let amt = d.quantity * d.rate;
    frappe.model.set_value(cdt, cdn, 'total_amount', amt);
}
