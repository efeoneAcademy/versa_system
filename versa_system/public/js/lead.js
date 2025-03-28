frappe.ui.form.on("Lead", {
    refresh: function(frm) {
        frm.add_custom_button(
            __("Feasibility Check"),
            function () {
                frappe.model.open_mapped_doc({
                    method: "versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_lead_to_feasibility_check",
                    source_name: frm.doc.name
                });
            },
            __("Create")
        );
    }
});

frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        frm.fields_dict['material_details'].grid.get_field('product_item').get_query = function(doc, cdt, cdn) {
            return {
                query: "versa_system.versa_system.custom_script.lead.get_only_products"
            };
        };
    }
});



 

