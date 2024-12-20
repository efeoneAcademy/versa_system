// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Raw Material Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Raw Material Request', {
    refresh: function(frm) {
        // Check if any row has 'is_available' unchecked
        let show_button = frm.doc.item_details.some(row => row.is_available === 0 || row.is_available === false);

        if (show_button) {
            frm.add_custom_button(
                __('Raw Material Purchase'),
                function() {
                    // Add button functionality here
                }
            );
        }
    }
});
