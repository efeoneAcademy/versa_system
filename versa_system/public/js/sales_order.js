
frappe.ui.form.on("Sales Order", {
    refresh: function (frm) {
      // Set the indicator label based on the current status
      setStatusIndicator(frm);
    },
  
    status: function (frm) {
      // Update the indicator label dynamically when the status changes
      setStatusIndicator(frm);
    },
  });
  
  // Function to set the indicator label based on status
  function setStatusIndicator(frm) {
    if (frm.doc.status === "Proforma Invoice") {
      frm.page.set_indicator("Proforma Invoice", "blue");
    } else if (frm.doc.status === "To Deliver and Bill") {
      frm.page.set_indicator("To Deliver and Bill", "red");
    }
  }
   