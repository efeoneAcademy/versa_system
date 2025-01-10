frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        // Filter for custom item details
        frm.fields_dict['custom_item_details'].grid.get_field('item').get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['item_group', '=', 'Products']
                ]
            };
        };

        frm.fields_dict['custom_item_details'].grid.get_field('material').get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['item_group', '=', 'Raw Material']
                ]
            };
        };

        // Add "Feasibility Check" button
        frm.add_custom_button(
            __("Feasibility Check"),
            function () {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Feasibility Check",
                        filters: { lead: frm.doc.name },
                        fields: ["name"]
                    },
                    callback: function (response) {
                        if (response.message && response.message.length > 0) {
                            frappe.msgprint({
                                title: __("Message"),
                                indicator: "red",
                                message: `A feasibility check already exists for this lead: ${frm.doc.name}.`
                            });
                        } else {
                            frappe.model.open_mapped_doc({
                                method: "versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_lead_to_feasibility_check",
                                frm: frm,
                            });
                        }
                    }
                });
            },
            __("Create")
        );


                frm.add_custom_button(
                    __("Go to Final Design"),
                    function () {
                        frappe.model.open_mapped_doc({
                            method: "versa_system.versa_system.doctype.design_request.design_request.map_lead_to_design_request",
                            frm: frm,
                        });
                    },
                    __("Create")
                );

        // Add "Create Quotation" button
        if (!frm.is_new()) {
            frm.page.remove_inner_button(__('Quotation'), 'Create');
            frm.add_custom_button(__('Quotation'), function() {
                frappe.model.open_mapped_doc({
                    method: 'versa_system.versa_system.custom_script.quotation.map_lead_to_quotation',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});
