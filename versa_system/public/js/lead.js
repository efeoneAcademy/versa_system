// In lead_custom_script.js

frappe.ui.form.on("Lead", {
    refresh: function(frm) {
        frm.add_custom_button(__("Feasibility Property Check"), function() {
            frappe.call({
                method: "versa_system.versa_system.custom_scripts.lead.lead.map_lead_to_feasibility_check",
                args: {
                    source_name: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.set_route("Form", "Feasibility Property Check", r.message);
                    }
                }
            });
        }, __("Create"));
    }
});


// frappe.ui.form.on('Lead', {
//     refresh: function(frm) {
//         frm.add_custom_button(__('Feasibility Check'), function() {
//
//         }, __('Create'));
//     }
// });
