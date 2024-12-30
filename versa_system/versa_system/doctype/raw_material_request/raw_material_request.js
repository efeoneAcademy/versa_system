// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Raw Material Request', {
    refresh: function(frm) {
        // Remove existing buttons to avoid duplicates
        frm.remove_custom_button(__('Raw Material Purchase'));
        frm.remove_custom_button(__('Go to Quotation'));

        // Check if any row has 'is_available' unchecked
        let has_unchecked = frm.doc.item_details.some(row => row.is_available === 0 || row.is_available === false);

        // Check if all rows have 'is_available' checked
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

        // Add "Go to Quotation" button if all rows are checked
        if (all_checked) {
            frm.add_custom_button(
                __('Go to Quotation'),
                function() {
                    // Add redirection logic to Quotation form here
                    frappe.set_route('List', 'Quotation');
                }
            );
        }
    }
});
