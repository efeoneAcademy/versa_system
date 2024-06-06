//
//     frappe.ui.form.on('Quotation', {
//     refresh: function(frm) {
//         frm.add_custom_button(__('Final Design'), function() {
//             frappe.model.open_mapped_doc({
//                 method: 'versa_system.versa_system.custom_scripts.quotation.quotation.',
//                 frm: frm
//             });
//         }, __('Create'))
//     }
// });


frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Final Design'), function() {
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.custom_scripts.quotation.quotation.map_quotation_to_final_design',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});
