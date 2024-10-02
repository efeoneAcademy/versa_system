frappe.ui.form.on("Raw Material", {
  refresh: function (frm) {
    // Filter for Item Type field (show only Products)
    frm.set_query("item_type", function () {
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
