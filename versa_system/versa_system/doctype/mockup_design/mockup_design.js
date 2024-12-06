frappe.ui.form.on('Mockup Design', {
    refresh: function (frm) {
        // Ensure the form is saved before adding buttons
        if (!frm.is_new()) {
            // Add a custom button to navigate to the linked Lead
            if (frm.doc.from_lead) {
                frm.add_custom_button(__('Go to Lead'), function () {
                    frappe.set_route('Form', 'Lead', frm.doc.from_lead);
                });
            }
        }

        // Add a 'Quotation' button if the workflow state is 'Approved'
        if (frm.doc.workflow_state === 'Approved') {
            frm.add_custom_button(__('Quotation'), function () {
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.doctype.mockup_design.mockup_design.map_mockup_design_to_quotation',
                    frm: frm
                });
            }, __('Create'));
        }
    }, 
 // Function to update the Lead with table data from Feasibility Check
  all_select: function (frm) {
    if (frm.doc. all_select) {
      // Loop through all rows in the Details child table
      frm.doc.lead_details.forEach(row => {
        frappe.model.set_value(row.doctype, row.name, 'md_approved', 1); // Check the Approve column
      });
    } else {
      // Uncheck the Approve column when Select All is unchecked
      frm.doc.lead_details.forEach(row => {
        frappe.model.set_value(row.doctype, row.name, 'md_approved', 0); // Uncheck the Approve column
      });
    }
  }	
});
 