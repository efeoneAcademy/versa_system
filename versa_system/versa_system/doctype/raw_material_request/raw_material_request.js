frappe.ui.form.on('Raw Material Request', {
    refresh: function(frm) {
        // Remove existing buttons to avoid duplicates
        frm.remove_custom_button(__('Raw Material Purchase'));
        frm.remove_custom_button(__('Go to Quotation'));

        // Check 'is_available' status in item_details
        let has_unchecked = frm.doc.item_details.some(row => row.is_available === 0 || row.is_available === false);
        let all_checked = frm.doc.item_details.every(row => row.is_available === 1 || row.is_available === true);

        // Add "Raw Material Purchase" button if any row is unchecked
        if (has_unchecked) {
            frm.add_custom_button(
                __('Raw Material Purchase'),
                function() {
                    frappe.model.open_mapped_doc({
                        method: "versa_system.versa_system.custom_script.material_request.map_raw_material_to_material_request",
                        frm: frm
                    });
                }
            );
        }
        // Add a custom button labeled 'Go to Quotation' in the form
        if (all_checked){
        frm.add_custom_button(__('Go to Quotation'), function() {
            if (!frm.doc.lead) {
                frappe.msgprint(__('No Lead is linked to this Raw Material Request.'));
                return;
            }
            frappe.call({
                method: "versa_system.versa_system.custom_script.quotation.get_quotations_by_lead",
                args: {
                    lead_name: frm.doc.lead
                },
                callback: function(response) {
                    if (response.message && response.message.length > 0) {
                        frappe.set_route("Form", "Quotation", response.message[0].name);
                    } else {
                        frappe.msgprint(__('No Quotation is linked to the Lead associated with this Raw Material Request.'));
                    }
                }
            });
        });
      }

        if (frm.fields_dict['item_details']) {
              frm.fields_dict['item_details'].grid.toggle_display('is_customized', false);  // Hide the 'is_customized' column in the child table
              frm.fields_dict['item_details'].grid.toggle_display('is_feasible', false);   // Hide the 'is_feasible' column in the child table

        }
    }
});
