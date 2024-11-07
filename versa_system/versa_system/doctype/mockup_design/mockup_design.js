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
frappe.ui.form.on('Mockup Design', {
    after_save: function(frm) {
        // Check if the current status is 'Lead' and update it to 'Feasibility Approved'
        // Check if the current status is 'Lead' and update it to 'Mockup Design Approved'
        if (frm.doc.status === 'Lead') {
            frm.set_value('status', 'Mockup Design Approved');
            frm.save(); // Save again to persist the change
        }
    },

    approve: function(frm) {
        // Approve the mockup design and update lead status if linked
        if (frm.doc.is_approved) {
        if (frm.doc.is_approved && frm.doc.status !== 'Mockup Design Approved') {
            frm.set_value('status', 'Mockup Design Approved');  // Set mockup design status

            // Update the linked lead's status if applicable
            if (frm.doc.from_lead) {
                frappe.call({
                    method: 'frappe.client.set_value',
                    args: {
                        doctype: 'Lead',
                        name: frm.doc.from_lead,
                        fieldname: 'status',
                        value: 'Mockup Design Approved',
                    },
                    callback: function(response) {
                        if (response && !response.exc) {
                        if (response && response.message && !response.exc) {
                            frappe.msgprint(
                                `Lead ${frm.doc.from_lead} status updated to 'Mockup Design Approved'.`,
                                'Status Updated'
                            );
                        } else {
                            frappe.msgprint('Failed to update lead status.', 'Error');
                        }
                    }
                });
            }

            frm.save(); // Save the mockup design document after approval
        }
    },

    reject: function(frm) {
        // Reject the mockup design and update lead status if linked
        frm.set_value('status', 'Mockup Design Rejected'); // Set mockup design rejection status

        // Update the linked lead's status if applicable
        if (frm.doc.from_lead) {
            frappe.call({
                method: 'frappe.client.set_value',
                args: {
                    doctype: 'Lead',
                    name: frm.doc.from_lead,
                    fieldname: 'status',
                    value: 'Mockup Design Rejected', // Set lead status to rejected
                },
                callback: function(response) {
                    if (response && !response.exc) {
                        frappe.msgprint(
                            `Lead ${frm.doc.from_lead} status updated to 'Mockup Design Rejected'.`,
                            'Status Updated'
                        );
                    } else {
                        frappe.msgprint('Failed to update lead status.', 'Error');
                    }
                }
            });
        }

        frm.save(); // Save the document to persist the rejection
        if (frm.doc.status !== 'Mockup Design Rejected') {
            frm.set_value('status', 'Mockup Design Rejected'); // Set mockup design rejection status

            // Update the linked lead's status if applicable
            if (frm.doc.from_lead) {
                frappe.call({
                    method: 'frappe.client.set_value',
                    args: {
                        doctype: 'Lead',
                        name: frm.doc.from_lead,
                        fieldname: 'status',
                        value: 'Mockup Design Rejected', // Set lead status to rejected
                    },
                    callback: function(response) {
                        if (response && response.message && !response.exc) {
                            frappe.msgprint(
                                `Lead ${frm.doc.from_lead} status updated to 'Mockup Design Rejected'.`,
                                'Status Updated'
                            );
                        } else {
                            frappe.msgprint('Failed to update lead status.', 'Error');
                        }
                    }
                });
            }

            frm.save(); // Save the document to persist the rejection
        }
    }
});
