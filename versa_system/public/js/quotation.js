frappe.ui.form.on("Quotation", {
  onload: function (frm) {
    // Check if the quotation status is "Approved" when the form loads
    if (!frm.is_new() && frm.doc.workflow_state === "Approved") {
      // Add 'Final Design' button in the dropdown
      add_final_design_button(frm);
    }
  },
  refresh: function (frm) {
    // Manage button visibility on refresh
    frm.remove_custom_button(__("Final Design")); // Remove previous instances
    if (!frm.is_new() && frm.doc.workflow_state === "Approved") {
      add_final_design_button(frm);
    }
  },
});

function add_final_design_button(frm) {
  frm.add_custom_button(
    __("Final Design"),
    function () {
      frappe.model.open_mapped_doc({
        method:
          "versa_system.versa_system.custom_scripts.quotation.map_quotation_to_final_design", // Adjust to your path
        frm: frm,
      });
    },
    __("Create")
  );
}
