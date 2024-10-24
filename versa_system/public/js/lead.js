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

    // Set query for 'item' field in the child table to show only 'Products'
    frm.fields_dict["custom_enquiry_details"].grid.get_field("item").get_query =
      function () {
        return {
          filters: {
            item_group: "Products", // Adjust according to your item group
          },
        };
      };

    // Set query for 'material' field in the child table to show only 'Raw Materials'
    frm.fields_dict["custom_enquiry_details"].grid.get_field(
      "material"
    ).get_query = function () {
      return {
        filters: {
          item_group: "Raw Material",
        },
      };
    };

    // Set filters for multiple fields (model, brand, design, size) based on the selected 'item' in the child table 'custom_enquiry_details'
    const fields_to_filter = ["model", "brand", "design", "size"];
    fields_to_filter.forEach(function (field) {
      frm.fields_dict["custom_enquiry_details"].grid.get_field(
        field
      ).get_query = function (doc, cdt, cdn) {
        var child = locals[cdt][cdn]; // Get the current child row
        return {
          filters: {
            item: child.item, // Filter based on the selected item in the same row
          },
        };
      };
    });
  },
});
