frappe.ui.form.on('Mockup Design', {
    refresh: function(frm) {
        // Check if the workflow state is "Approved"
        if (frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Quotation'), function() {
                // Call the mapping function for Mockup Design to Quotation
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.doctype.mockup_design.mockup_design.map_mockup_design_to_quotation',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});
