frappe.ui.form.on("Feasibility Check", {
  refresh: function (frm) {
    // Check if the Feasibility Check is not new and is approved
    if (frm.doc.workflow_state === "Approved") {
      // Add the Mockup Design button
      frm.add_custom_button(
        __("Mockup Design"),
        function () {
          frappe.call({
            method: "versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_feasibility_to_mockup_design",
            args: {
              source_name: frm.doc.name,
            },
            callback: function (response) {
              frappe.msgprint({
                title: __("Notification"),
                message: __("A Mockup Design request has been sent."),
                indicator: "green",
              });
            },
          });
        },
        __("Create")
      );

      // Call the function to update the Lead and add the navigation button
      updateAndNavigateToLead(frm);
    }

    // Fetch the status of the related Mockup Design
    frappe.db.get_value(
      "Mockup Design",
      { from_lead: frm.doc.from_lead },
      "workflow_state",
      function (value) {
        if (value && value.workflow_state === "Approved") {
          frm.remove_custom_button(__("Mockup Design"));
        }
      }
    );

    // Add "Go to Lead" button if the workflow state is "Approved" or "Rejected"
    if (
      frm.doc.workflow_state === "Approved" ||
      frm.doc.workflow_state === "Rejected"
    ) {
      frm.add_custom_button(__("Go to Lead"), function () {
        if (!frm.doc.from_lead) {
          frappe.msgprint(__("Please select a Lead before proceeding."));
          return;
        }
        frappe.set_route("Form", "Lead", frm.doc.from_lead);
      });
    }
  },

  after_save: function (frm) {
    // Check if the current status is 'Lead' and update to 'Interest'
    if (frm.doc.status === "Lead") {
      frm.set_value("status", "Interest");
      frm.save(); // Save again to persist the change
    }
  },

  validate: function (frm) {
    // Ensure at least one row in the child table is approved
    const isApproved = frm.doc.details.some((row) => row.approve);
    if (!isApproved) {
      frappe.throw(
        __("At least one row in the details table must be approved before saving.")
      );
    }
  },

  select_all: function (frm) {
    if (frm.doc.select_all) {
      // Loop through all rows in the Details child table
      frm.doc.details.forEach((row) => {
        frappe.model.set_value(row.doctype, row.name, "approve", 1); // Check the Approve column
      });
    } else {
      // Uncheck the Approve column when Select All is unchecked
      frm.doc.details.forEach((row) => {
        frappe.model.set_value(row.doctype, row.name, "approve", 0); // Uncheck the Approve column
      });
    }
  },
});

// Function to update the Lead with table data from Feasibility Check
function update_lead_from_feasibility_check(frm) {
  const details = frm.doc.details.map((row) => ({
    item: row.item,
    brand: row.brand,
    rate_range: row.rate_range,
    design: row.design,
    model: row.model,
    approve: row.approve,
  }));

  frappe.call({
    method: "versa_system.versa_system.custom_scripts.fesibility.update_lead",
    args: {
      lead_name: frm.doc.from_lead,
      details: JSON.stringify(details), // Ensure details are sent as JSON string
    },
  });
}

// Function to update the Lead and navigate to it
function updateAndNavigateToLead(frm) {
  if (frm.doc.from_lead) {
    update_lead_from_feasibility_check(frm);

    // Add a button to navigate to the Lead
    frm.add_custom_button(__("Go to Lead"), function () {
      frappe.set_route("Form", "Lead", frm.doc.from_lead);
    });
  }
}
