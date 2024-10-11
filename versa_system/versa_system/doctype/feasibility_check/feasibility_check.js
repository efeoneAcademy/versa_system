frappe.ui.form.on('Feasibility Check', {
    refresh: function(frm) {
        // Check if the Feasibility Check is not new and is approved
        if (frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Mockup Design'), function() {
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_feasibility_to_mockup_design',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});
