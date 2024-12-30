
frappe.ui.form.on('Design Request', {
    refresh: function(frm) {
      if (frm.doc.workflow_state === "Approved" && frm.doc.type === "Mockup Design") {
        // Add a custom button
        frm.add_custom_button(__('View Lead'), function() {
            // Check if the 'lead' field exists and has a value
            if (frm.doc.lead) {
                // Redirect to the specific Lead document
                frappe.set_route('Form', 'Lead', frm.doc.lead);
            } else {
                frappe.msgprint(__('No Lead is linked to this Design Request.'));
            }
        }, __('Create Quatation from Lead')); // Group under "Actions"
      }

      // Add a custom button
      if (frm.doc.workflow_state === "Approved" && frm.doc.type === "Final Design") {
        frm.add_custom_button(__('Raw Material Check'), function() {
          frappe.model.open_mapped_doc({
            method: "versa_system.versa_system.doctype.raw_material_request.raw_material_request.map_lead_to_raw_material_request",
            frm: frm,
          });
        }, __('Create')); // Group under "Create"
      }
    },
});
