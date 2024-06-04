frappe.ui.form.on('Lead', {
  refresh: function(frm) {
    frm.add_custom_button(__('New Quotation'), function() {
      frappe.model.open_mapped_doc({
          method : 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_quotation',
          frm : frm
        });
    }, __('Create'));

    setTimeout(() => {
      frm.remove_custom_button('Quotation', 'Create');
      frm.remove_custom_button('Customer', 'Create');
      frm.remove_custom_button('Prospect', 'Create');
      frm.remove_custom_button('Opportunity', 'Create');
    }, 10);
  }
});
