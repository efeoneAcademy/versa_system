// Copyright (c) 2025, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on("Feasibility Check", {
    refresh(frm) {
        if (frm.doc.workflow_state === "Approved") { 
            frm.add_custom_button(
                __("GoTo MOC Design"),
                function () {
                    frappe.model.open_mapped_doc({
                        method: "versa_system.versa_system.doctype.moc_design.moc_design.map_feasibility_check_to_moc_design",
                        source_name: frm.doc.name
                    });
                }
            );
        }
    },
});





