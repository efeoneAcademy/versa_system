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
  from_lead: function (frm) {
    /*
     * Function to populate items child table on selecting Lead.
     */
    if (frm.doc.from_lead) {
      frappe.call({
        method:
          "versa_system.versa_system.custom_scripts.quotation.py.get_lead_properties", // Ensure this path is correct
        args: {
          lead_name: frm.doc.from_lead,
        },
        callback: function (r) {
          if (r.message) {
            // Clear existing child table data
            frm.clear_table("items");

            // Populate child table with data from the Lead
            r.message.forEach(function (item) {
              var row = frm.add_child("items");
              row.item_code = item.item_code; // Ensure these fields match your Lead's response

              // Add any additional fields you want to populate
            });

            // Refresh the child table field to show updated data
            frm.refresh_field("items");
          } else {
            frappe.msgprint(__("No items found for the selected Lead."));
          }
        },
        error: function (err) {
          frappe.msgprint(
            __("Error while fetching Lead items: {0}", [err.message])
          );
        },
      });
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
