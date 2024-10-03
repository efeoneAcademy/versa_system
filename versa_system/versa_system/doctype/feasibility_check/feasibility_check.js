// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Feasibility Check', {
    refresh: function(frm) {
        if (frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Mockup Design'), function() {
                frappe.call({
                    method: 'frappe.client.insert',
                    args: {
                        doc: {
                            doctype: 'Mockup Design',
                            from_lead: frm.doc.from_lead
                        }
                    },
                    callback: function(r) {
                        if (r.message) {
                            // Redirect to the newly created Mockup Design
                            frappe.set_route('Form', 'Mockup Design', r.message.name);
                        }
                    }
                });
            });
        }
    }
});
