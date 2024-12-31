// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt
frappe.ui.form.on('Feasibility Check', {
    refresh: function(frm) {
      if (frm.doc.workflow_state === "Approved") {
        // Check if child table 'item_details' exists
        if (!frm.doc.item_details || !frm.doc.item_details.length) {
            return; // Exit if the child table is empty
        }

        // Check if any row has 'is_customized' checked
        let show_button = frm.doc.item_details.some(row => row.is_feasible === 1 || row.is_feasible === true);

        if (show_button) {
            frm.add_custom_button(
                __("Create Mockup Design"),
                function () {
                    frappe.model.open_mapped_doc({
                        method: "versa_system.versa_system.doctype.design_request.design_request.map_feasibility_check_to_moc",
                        frm: frm,
                    });
                },
                __("Create")
            );
        }
      }
    }
});
