frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        // Add "Go to Lead" button for Approved Quotations
        if (frm.doc.workflow_state === "Approved") {
            // Button to navigate to Lead
            frm.add_custom_button(__('Go to Lead'), function() {
                if (frm.doc.party_name) {
                    frappe.set_route('Form', 'Lead', frm.doc.party_name);
                } else {
                    frappe.msgprint(__('No Lead is linked to the Quotation.'));
                }
            });

            // Add "Go to Final Design" button for Approved Quotations
            frm.add_custom_button(__('Go to Final Design'), function() {
                frappe.model.open_mapped_doc({
                    method: "versa_system.versa_system.doctype.design_request.design_request.map_quotation_to_design_request",
                    frm: frm,
                });
            }, __("Create"));
        }
        if (frm.fields_dict['item_details']) {
              frm.fields_dict['item_details'].grid.toggle_display('is_customized', false);
              frm.fields_dict['item_details'].grid.toggle_display('is_feasible', false);
              frm.fields_dict['item_details'].grid.toggle_display('is_available', false);
        }
    }
});
