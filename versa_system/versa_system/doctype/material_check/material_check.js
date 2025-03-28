// Copyright (c) 2025, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Material Check", {
	refresh(frm) {
        if(!frm.is_new())
        frm.add_custom_button(
            __("Material Request"),
            function () {
                frappe.set_route("Form", "Material Request", "new-material-request");
            }
        );
        if(!frm.is_new())
        frm.add_custom_button(
            __("Work Order"),
            function () {
                frappe.set_route("Form", "Work Order", "new-material-request","New Work Order");
            }
        );
	},
});

