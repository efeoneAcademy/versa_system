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
frappe.ui.form.on('Feasibility Check', {
    after_save: function(frm) {
        // Check if the current status is 'Lead' and update to 'Interest'
        if (frm.doc.status === 'Lead') {
            frm.set_value('status', 'Interest');
            frm.save(); // Save again to persist the change
        }
    },

    approve: function(frm) {
        // Approve the feasibility and update lead status if linked
        if (frm.doc.is_approved) {
            frm.set_value('status', 'Feasibility Approved');  // Set feasibility status

            if (frm.doc.from_lead) {
                frappe.call({
                    method: 'frappe.client.set_value',
                    args: {
                        doctype: 'Lead',
                        name: frm.doc.from_lead,
                        fieldname: 'status',
                        value: 'Feasibility Check Approved',
                    },
                    callback: function(response) {
                        if (response && !response.exc) {
                            frappe.msgprint(
                                `Lead ${frm.doc.from_lead} status updated to 'Feasibility Check Approved'.`,
                                'Status Updated'
                            );
                        }
                    }
                });
            }

            frm.save(); // Save the feasibility document after approval
        }
    },

    reject: function(frm) {
        // Reject the feasibility and update lead status if linked
        frm.set_value('status', 'Feasibility Rejected'); // Adjust rejection status

        if (frm.doc.from_lead) {
            frappe.call({
                method: 'frappe.client.set_value',
                args: {
                    doctype: 'Lead',
                    name: frm.doc.from_lead,
                    fieldname: 'status',
                    value: 'Feasibility Check Rejected', // Set lead status to rejected
                },
                callback: function(response) {
                    if (response && !response.exc) {
                        frappe.msgprint(
                            `Lead ${frm.doc.from_lead} status updated to 'Feasibility Check Rejected'.`,
                            'Status Updated'
                        );
                    }
                }
            });
        }

        frm.save(); // Save the document to persist the rejection
    }
});
