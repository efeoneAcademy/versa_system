// /home/hanihassan/frappe-bench/apps/versa_system/versa_system/versa_system/doctype/raw_material/raw_material.js

frappe.ui.form.on("Raw Material", {
  lead: function (frm) {
    if (frm.doc.lead) {
      // Fetch enquiry details from the server
      frappe.call({
        method:
          "versa_system.versa_system.doctype.raw_material.raw_material.fetch_enquiry_details", // Correct module path
        args: {
          lead: frm.doc.lead,
        },
      });
    } else {
      // Clear fields if no lead is selected
      frm.set_value("raw_materials", []); // Clear child table if no lead is selected
    }
  },

  refresh: function (frm) {
    // Filter for Item Type field (show only Products)
    frm.set_query("item", function () {
      return {
        filters: {
          item_group: "Products", // Filter for items that belong to "Products"
        },
      };
    });

    // Filter for Material field (show only Raw Materials)
    frm.set_query("material", function () {
      return {
        filters: {
          item_group: "Raw Material", // Filter for items that belong to "Raw Material"
        },
      };
    });
  },
});

// Child Table logic for Raw Materials
frappe.ui.form.on("Raw Materials", {
  // Triggered when the item is added to the child table
  raw_materials_add: function (frm) {
    frm.fields_dict["raw_materials"].grid.get_field("item").get_query =
      function () {
        return {
          filters: {
            item_group: "Raw Material", // Filter for items that belong to "Raw Material"
          },
        };
      };
  },

  // Triggered when the quantity field is changed in the child table
  quantity: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn]; // Access the current row in the "Raw Materials" child table
    row.total_amount = row.quantity * row.rate || 0; // Calculate total amount (Quantity * Rate)
    frm.refresh_field("raw_materials"); // Refresh the "Raw Materials" child table field to show updated total amount
  },

  // Triggered when the rate field is changed in the child table
  rate: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn]; // Access the current row in the "Raw Materials" child table
    row.total_amount = row.quantity * row.rate || 0; // Calculate total amount (Quantity * Rate)
    frm.refresh_field("raw_materials"); // Refresh the "Raw Materials" child table field to show updated total amount
  },
});
