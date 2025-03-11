frappe.ui.form.on("Sales Order", {
  refresh: function (frm) {
    setStatusIndicator(frm);
  },

  status: function (frm) {
    setStatusIndicator(frm);
  },
});

function setStatusIndicator(frm) {
  if (frm.doc.status === "Proforma Invoice") {
    frm.page.set_indicator("Proforma Invoice", "blue");
  } else if (frm.doc.status === "To Deliver and Bill") {
    frm.page.set_indicator("To Deliver and Bill", "red");
  }
}