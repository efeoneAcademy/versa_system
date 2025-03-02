

frappe.ui.form.on('Final Design', {
    refresh: function(frm) {
    if(!frm.is_new())
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
