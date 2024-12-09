frappe.ui.form.on("Lead", {
  refresh: function (frm) {
    // Check if the lead is already saved (not a new record)
    if (!frm.is_new()) {
      // Remove the default buttons after a brief delay to ensure the form has loaded
      setTimeout(() => {
        frm.remove_custom_button("Quotation", "Create");
        frm.remove_custom_button("Customer", "Create");
        frm.remove_custom_button("Prospect", "Create");
        frm.remove_custom_button("Opportunity", "Create");
      }, 2);

      // Update buttons based on status
      update_buttons(frm);
    }

    // Set query for 'item' field in the child table to show only 'Products'
    frm.fields_dict["custom_enquiry_details"].grid.get_field("item").get_query =
      function () {
        return {
          filters: { item_group: "Products" },
        };
      };

    // Set query for 'material' field in the child table to show only 'Raw Materials'
    frm.fields_dict["custom_enquiry_details"].grid.get_field(
      "material"
    ).get_query = function () {
      return {
        filters: { item_group: "Raw Material" },
      };
    };

    // Set filters for multiple fields based on the selected 'item' in the child table
    const fields_to_filter = ["model", "brand", "design", "size"];
    fields_to_filter.forEach(function (field) {
      frm.fields_dict["custom_enquiry_details"].grid.get_field(
        field
      ).get_query = function (doc, cdt, cdn) {
        const child = locals[cdt][cdn];
        return {
          filters: { item: child.item },
        };
      };
    });
  },

  status: function (frm) {
    // Update buttons when status changes
    update_buttons(frm);
    update_quotation_buttons(frm);
  },
});

function open_readonly_document(frm, doctype, filter_field) {
  frappe.call({
    method: "frappe.client.get",
    args: {
      doctype: doctype,
      filters: { [filter_field]: frm.doc.name },
    },
    callback: function (response) {
      if (response.message) {
        const document = response.message;
        frappe.set_route("Form", doctype, document.name);
        frappe.ui.form.on(doctype, "onload", function (frm) {
          frm.set_read_only();
        });
      } else {
        frappe.msgprint({
          title: __("No Document Found"),
          message: `No related ${doctype} document was found for this lead.`,
          indicator: "red",
        });
      }
    },
  });
}

// Function to update buttons based on status
function update_buttons(frm) {
  // Remove existing buttons before adding new ones
  frm.remove_custom_button(__("Feasibility Check"));
  frm.remove_custom_button(__("New Opportunity"));
  frm.remove_custom_button(__("New Quotation"));
  frm.remove_custom_button(__("View Quotation"));

  // Check status for feasibility check buttons
  if (
    frm.doc.status === "Lead" ||
    frm.doc.status === "Interested" ||
    frm.doc.status === "Feasibility Check Rejected"
  ) {
    frm.add_custom_button(
      __("Feasibility Check"),
      function () {
        frappe.call({
          method:
            "versa_system.versa_system.custom_scripts.lead.map_lead_to_feasibility_check",
          args: {
            source_name: frm.doc.name,
          },
          callback: function (response) {
            frappe.msgprint({
              title: __("Notification"),
              message: __("A Feasibility Check request has been sent."),
              indicator: "green",
            });
          },
        });
      },
      __("Create")
    );
  } else if (
    frm.doc.status === "Opportunity" ||
    frm.doc.status === "Feasibility Check Approved" ||
    frm.doc.status === "Converted" ||
    frm.doc.status === "Quotation" ||
    frm.doc.status === "Mockup Design Approved" ||
    frm.doc.status === "Mockup Design Rejected"
  ) {
    frm.add_custom_button(
      __("View Feasibility Check"),
      function () {
        open_readonly_document(frm, "Feasibility Check", "from_lead");
      },
      __("Create")
    );
  }

  // Check if the quotation is already saved (not a new record)
  if (
    frm.doc.status === "Feasibility Check Approved" ||
    frm.doc.status === "Mockup Design Approved" ||
    frm.doc.status === "Converted"
  ) {
    // Add New Quotation button
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
  } else if (
    frm.doc.status === "Converted" ||
    frm.doc.status === "Mockup Design Approved" ||
    frm.doc.status === "Quotation" ||
    frm.doc.status === "Final Design Approved" ||
    frm.doc.status === "Final Design Rejected" ||
    frm.doc.status === "Quotation Rejected"
  ) {
    // Check the status to add the View Quotation button
    frm.add_custom_button(
      __("View Quotation"),
      function () {
        open_readonly_document(frm, "Quotation", "party_name");
      },
      __("Create")
    );
  } else if (frm.doc.status === "Lost Quotation") {
    // Check the status to add the View Quotation button
    frm.add_custom_button(
      __("Lost Quotation"),
      function () {
        open_readonly_document(frm, "Quotation", "party_name");
      },
      __("Create")
    );
  }

  if (
    frm.doc.status === "Converted" ||
    frm.doc.status === "Mockup Design Approved" ||
    frm.doc.status === "Quotation" ||
    frm.doc.status === "Final Design Approved" ||
    frm.doc.status === "Final Design Rejected" ||
    frm.doc.status === "On Review"
  ) {
    // Add View Mockup Design button
    frm.add_custom_button(
      __("View Mockup Design"),
      function () {
        open_readonly_document(frm, "Mockup Design", "from_lead");
      },
      __("Create")
    );
  }

  if (frm.doc.status === "Final Design Approved") {
    // Add View Mockup Design button
    frm.add_custom_button(
      __("View Final Design"),
      function () {
        open_readonly_document(frm, "Final Design", "from_lead");
      },
      __("Create")
    );
  }
}
