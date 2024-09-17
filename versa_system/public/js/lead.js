frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        frm.add_custom_button(__('Feasibility Check'), function() {
            frappe.model.open_mapped_doc({
                method: 'versa_system.versa_system.custom_scripts.lead.map_lead_to_feasibility_check',
                frm: frm
            });
        }, __('Create'));
    }
});
