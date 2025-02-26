// Copyright (c) 2025, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Design', {
    refresh: function(frm) {
        frm.add_custom_button(
            __("GoTo Material Check"),
            function () {
                frappe.model.open_mapped_doc({
                    method: "versa_system.versa_system.doctype.material_check.material_check.final_design_to_material_check",
                    source_name: frm.doc.name
                });
            },
            
        );
    }
});
