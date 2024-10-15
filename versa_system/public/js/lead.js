frappe.ui.form.on("Lead", {
  refresh: function (frm) {
    // Check if the lead is already saved (not a new record)
    if (!frm.is_new()) {
      // Add custom button for Feasibility Check
      frm.add_custom_button(
        __("Feasibility Check"),
        function () {
          frappe.model.open_mapped_doc({
            method:
              "versa_system.versa_system.custom_scripts.lead.map_lead_to_feasibility_check", // Path to your Python method
            frm: frm,
          });
        },
        __("Create")
      );

      // Add custom button for New Quotation
      frm.add_custom_button(
        __("New Quotation"),
        function () {
          frappe.model.open_mapped_doc({
            method:
              "versa_system.versa_system.custom_scripts.lead.map_lead_to_quotation", // Path to your Python method
            frm: frm,
          });
        },
        __("Create")
      );

      // Remove the default buttons (Quotation, Customer, Prospect, Opportunity)
      setTimeout(() => {
        frm.remove_custom_button("Quotation", "Create");
        frm.remove_custom_button("Customer", "Create");
        frm.remove_custom_button("Prospect", "Create");
        frm.remove_custom_button("Opportunity", "Create");
      }, 10);
    }
  },
});
