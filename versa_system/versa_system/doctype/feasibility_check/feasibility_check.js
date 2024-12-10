// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Feasibility Check", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Feasibility Check', {
    refresh: function(frm) {
        // Add a custom button to the Lead form
        frm.add_custom_button(__('Create MOC UP Design'), function() {
            frappe.new_doc('MOC UP Design');
            // frappe.model.open_mapped_doc({
            //     method: "versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_lead_to_feasibility_check",  // Path to the server-side function
            //     source_name: frm.doc.name  // The ID of the current Lead
            // });xz
        }, __("Create"));
    }
});
// refresh: function(frm) {
//         // Add custom button to redirect to Feasibility Check
//         frm.add_custom_button('Create MOC UP Design', function() {
//             // Check if lead is saved
//             if (!frm.doc.name) {
//                 frappe.msgprint('Please save the Feasibility c first');
//                 return;
//             }
//
//             // Create or redirect to Feasibility Check
//             frappe.new_doc('Feasibility Check', {
//                 lead: frm.doc.name
//             });
//         }, __('Create'));
//     }
// });
