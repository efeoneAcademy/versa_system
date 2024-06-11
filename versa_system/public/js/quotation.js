frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        create_final_design_button(frm)
    }
});

function create_final_design_button(frm) {
  /*
  * Adds a custom button to the Quotation form to map Quotations to Final Design documents.
  */
  if (!frm.is_new() && frm.doc.workflow_state === 'Approved') {
      frm.add_custom_button(__('Final Design'), function() {
          frappe.model.open_mapped_doc({
              method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_final_design',
              args: {
                			docname: frm.doc.name
                		},
          });
      }, __('Create'));
  }
}
