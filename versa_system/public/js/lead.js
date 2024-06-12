frappe.ui.form.on('Lead', {
  refresh: function(frm) {
    setTimeout(() => {
      frm.remove_custom_button('Quotation', 'Create');
      frm.remove_custom_button('Customer', 'Create');
      frm.remove_custom_button('Prospect', 'Create');
      frm.remove_custom_button('Opportunity', 'Create');

      let quotation_button = frm.add_custom_button(__('New Quotation'), function() {
        frappe.model.open_mapped_doc({
          method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_quotation',
          frm: frm
        });
      }, __('Create'));

      let feasibility_check_button = frm.add_custom_button(__('Feasibility Check'), function() {
        frappe.model.open_mapped_doc({
          method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_feasibility_check',
          frm: frm
        });
      }, __('Create'));

      let mockup_design_button = frm.add_custom_button(__('Mockup Design'), function() {
        frappe.model.open_mapped_doc({
          method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_mockup_design',
          frm: frm
        });
      }, __('Create'));

      let final_design_button = frm.add_custom_button(__('Final Design'), function() {
        frappe.model.open_mapped_doc({
          method: 'versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_final_design',
          frm: frm
        });
      }, __('Create'));

      // Initialize all buttons to hidden
      mockup_design_button.hide();
      quotation_button.hide();
      feasibility_check_button.hide();
      final_design_button.hide();

      // Handle Lead buttons visibility based on status
      if (frm.doc.status === "Mockup Design Approved") {
        quotation_button.show();
      } else if (frm.doc.status === "Mockup Design Rejected") {
        // All buttons remain hidden
      } else if (frm.doc.status === "Mockup Design Pending") {
        mockup_design_button.show();
      } else if (frm.doc.status === "Lead") {
        feasibility_check_button.show();
      } else if (frm.doc.status === "Feasibility Check Approved") {
        mockup_design_button.show();
        quotation_button.show();
      } else if (frm.doc.status === "Feasibility Check Rejected") {
        // All buttons remain hidden
      } else if (frm.doc.status === "Quotation") {
        final_design_button.show();
      } else {
        // Default case for any other status
        mockup_design_button.show();
        feasibility_check_button.show();
      }

      set_model_query(frm);

    }, 10);
  }
});

frappe.ui.form.on("Properties Table", {
  item_type: function(frm, cdt, cdn) {
    set_model_query(frm);
  }
});

function set_model_query(frm) {
  /*
  * Function sets filter on Model field in Properties Table based on selected Item Type
  */
  frm.fields_dict["custom_property_table"].grid.get_field("model").get_query = function(doc, cdt, cdn) {
    var child = locals[cdt][cdn];
    return {
      filters: [
        ["item_type", "=", child.item_type]
      ]
    };
  }
}
