frappe.ui.form.on('Lead', {
    refresh: function (frm) {
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

        frm.add_custom_button(
          __("Feasibility Check"),
          function () {
            frappe.model.open_mapped_doc({
              method:
                "versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_lead_to_feasibility_check",
              frm: frm,
            });
          },
          __("Create")
        );


//   frm.add_custom_button(__("Feasibility Check"), function() {
//     frappe.call({
//         method: 'versa_system.versa_system.doctype.feasibility_check.feasibility_check.map_lead_to_feasibility_check',
//         args: {
//             source_name: frm.doc.name
//         },
//         callback: function(r) {
//             if (r.message) {
//                 // Open the newly created Feasibility Check
//                 frappe.new_doc('Feasibility Check');
//             }
//         },
//         error: function(r) {
//             frappe.msgprint(__('Error creating Feasibility Check'));
//             console.error(r);
//         }
//     });
// }, __("Create"));
    }
});
