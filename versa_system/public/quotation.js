frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        // Add "Go to Lead" button for Approved Quotations
        if (frm.doc.workflow_state === "Approved") {
            frm.add_custom_button(__('Go to Lead'), function() {
                if (frm.doc.party_name) {
                    frappe.set_route('Form', 'Lead', frm.doc.party_name);
                } else {
                    frappe.msgprint(__('No Lead is linked to the Quotation.'));
                }
            });
        }

        // Add "Go to Final Design" button
        frm.add_custom_button(__('Go to Final Design'), function() {
            // Action for the "Go to Final Design" button
            frappe.set_route('Form', 'Final Design', frm.doc.name);
        });
    }
});
