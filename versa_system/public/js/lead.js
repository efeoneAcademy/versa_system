frappe.ui.form.on("Lead", {
  refresh: function (frm) {
    // Check if the lead is already saved
    if (!frm.is_new()) {
      frm.add_custom_button(
        __("Feasibility Check"),
        function () {
          frappe.model.open_mapped_doc({
            method:
              "versa_system.versa_system.custom_scripts.lead.map_lead_to_feasibility_check",
            frm: frm,
          });
        },
        __("Create")
      );

      frm.add_custom_button(
        __("New Quotation"),
        function () {
          frappe.model.open_mapped_doc({
            method:
              "versa_system.versa_system.custom_scripts.lead.map_lead_to_quotation",
            frm: frm,
          });
        },
        __("Create")
      );

      frm.add_custom_button(
        __("Mockup Design"),
        function () {
          frappe.model.open_mapped_doc({
            method:
              "versa_system.versa_system.custom_scripts.lead.map_lead_to_mockup_design",
            frm: frm,
          });
        },
        __("Create")
      );

      // Removing default buttons
      setTimeout(() => {
        frm.remove_custom_button("Quotation", "Create");
        frm.remove_custom_button("Customer", "Create");
        frm.remove_custom_button("Prospect", "Create");
        frm.remove_custom_button("Opportunity", "Create");
      }, 10);
    }
  },
});
