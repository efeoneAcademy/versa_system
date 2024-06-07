frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        setTimeout(() => {
            frm.remove_custom_button('Quotation', 'Create');
            frm.remove_custom_button('Customer', 'Create');
            frm.remove_custom_button('Prospect', 'Create');
            frm.remove_custom_button('Opportunity', 'Create');
        }, 10);

        // Add custom Button 'New Quotation'
        let quotationButton = frm.add_custom_button(__('New Quotation'), function() {
            frappe.model.open_mapped_doc({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_quotation',
                frm: frm
            });
        }, __('Create'));
        // Add Custom Button 'Feasibility Property Check'
        let feasibilityCheckButton = frm.add_custom_button(__('Feasibility Property Check'), function() {
            frappe.model.open_mapped_doc({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_feasibility_check',
                frm: frm
            });
        }, __('Create'));
        //Add Custom Button 'Mockup Design'
        let mockupDesignButton = frm.add_custom_button(__('Mockup Design'), function() {
            frappe.model.open_mapped_doc({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_mockup_design',
                frm: frm
            });
        }, __('Create'));

        // Toggle visibility of buttons based on the value of status
        if (frm.doc.status === "Lead") {
            mockupDesignButton.hide();
            quotationButton.hide();
            feasibilityCheckButton.show();
        } else if(frm.doc.status === "Feasibility Check Approved"){
            mockupDesignButton.show();
            quotationButton.show();
            feasibilityCheckButton.hide();
        }else if (frm.doc.status === "Feasibility Check Rejected") {
            mockupDesignButton.hide();
            quotationButton.hide();
            feasibilityCheckButton.hide();

        } else {
              quotationButton.hide();
              mockupDesignButton.hide();
              feasibilityCheckButton.hide();
          }

        set_model_query(frm)

  }

});

frappe.ui.form.on("Properties Table", {
  item_type: function(frm, cdt, cdn) {
    set_model_query(frm)
  }
})

function set_model_query(frm) {
  /*
  * Function sets filter on Model field in Properties Table based on selected Item Type
  */
  frm.fields_dict["custom_property_table"].grid.get_field("model").get_query = function(doc, cdt, cdn) {
      var child = locals[cdt][cdn];
      return {
          filters:[
              ["item_type", "=", child.item_type]
          ]
      }
  }
}
