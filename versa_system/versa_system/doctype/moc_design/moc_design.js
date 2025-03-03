// Copyright (c) 2025, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("MOC Design", {
	refresh(frm) {
    if (frm.doc.workflow_state === "Approved") { // Ensure the button appears only after saving
        frm.add_custom_button(
            __("GoTo Quotation"),
            function () {
                frappe.model.open_mapped_doc({
                    method: "versa_system.versa_system.custom_script.quotation.map_moc_design_to_quotation",
                    source_name: frm.doc.name
                });
            }
        );
    }

	},
});
