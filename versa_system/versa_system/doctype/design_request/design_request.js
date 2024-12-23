// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Design Request', {
    refresh: function(frm) {
        // Ensure the 'type' field is read-only if its value is 'Mockup Design'
        if (frm.doc.type === 'Mockup Design') {
            frm.set_df_property('type', 'read_only', 1);
        }

        // Add a custom button when the workflow_state is 'Approved'
        if (frm.doc.workflow_state === "Approved") {
            frm.add_custom_button(__('Go to Lead'), function() {
                if (frm.doc.lead) {
                    frappe.set_route('Form', 'Lead', frm.doc.lead);
                } else {
                    frappe.msgprint(__('No Lead is linked to this Design Request.'));
                }
            }, __('Create Quotation from Lead')); // Group under "Actions"
        }
    },

    type: function(frm) {
        // Make the 'type' field read-only if its value is 'Mockup Design'
        if (frm.doc.type === 'Mockup Design') {
            frm.set_df_property('type', 'read_only', 1);
        } else {
            frm.set_df_property('type', 'read_only', 0);
        }
    }
});
