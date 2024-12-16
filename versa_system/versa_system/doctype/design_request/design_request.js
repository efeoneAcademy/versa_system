// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Design Request', {
    refresh: function(frm) {
      if (frm.doc.workflow_state === "Approved") {
        // Add a custom button
        frm.add_custom_button(__('Go to Lead'), function() {
            // Check if the 'lead' field exists and has a value
            if (frm.doc.lead) {
                // Redirect to the specific Lead document
                frappe.set_route('Form', 'Lead', frm.doc.lead);
            } else {
                frappe.msgprint(__('No Lead is linked to this Design Request.'));
            }
        }, __('Create Quatation from Lead')); // Group under "Actions"
      }
    }
});
