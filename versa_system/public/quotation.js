frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        if (frm.doc.workflow_state === "Approved") {
            frm.add_custom_button(__('Go to Lead'), function() {
                if (frm.doc.party_name) {
                    frappe.set_route('Form', 'Lead', frm.doc.party_name);
                } else {
                    frappe.msgprint(__('No Lead is linked to the Quotation.'));
                }
            })
        }
    }
});
