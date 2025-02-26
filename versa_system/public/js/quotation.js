frappe.ui.form.on("Quotation", {
    refresh: function(frm) {
        frm.add_custom_button(
            __("GoTo Final Design"),
            function () {
                frappe.model.open_mapped_doc({
                    method: "versa_system.versa_system.doctype.final_design.final_design.map_quotation_to_final_design",
                    source_name: frm.doc.name
                });
            },
            __("Create")
        );
    }
});