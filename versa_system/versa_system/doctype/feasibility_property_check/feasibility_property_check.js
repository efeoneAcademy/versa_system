// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Feasibility Property Check", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        frm.add_custom_button(__('Create Feasibility Property Check'), function() {
            frappe.model.open_mapped_doc({
                method: 'versa_system.versa_system.doctype.feasibility_property_check.feasibility_property_check.map_lead_to_feasibility_check',
                frm: frm
            });
        }, __('Create'));
    }
});
