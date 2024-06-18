frappe.ui.form.on('Feasibility Check', {
    from_lead: function(frm) {
        if (frm.doc.from_lead) {
            frappe.call({
                method: 'versa_system.versa_system.custom_scripts.lead.lead.get_lead_properties',
                args: {
                    lead_name: frm.doc.from_lead
                },
                callback: function(r) {
                    console.log('Response received:', r);
                    if (r.message) {
                        frm.clear_table("properties");
                        r.message.forEach(function(item) {
                            var row = frm.add_child("properties");
                            row.item_type = item.item_type;
                            row.material_type = item.material_type;
                            row.design = item.design;
                            row.model = item.model;
                            row.brand = item.brand;
                            row.size_chart = item.size_chart;
                            row.colour = item.colour;
                            row.row_id =item.name;
                        });
                        frm.refresh_field("properties");
                    }
                }
            });
        }
    }

});

frappe.ui.form.on('Feasibility Solution', {
    create_raw_material: function(frm, cdt , cdn) {
        let row = locals[cdt][cdn];
        frappe.new_doc('Raw Material Bundle', {
            'reference_doctype': 'Feasibility Solution',
            'reference_name': row.name,
        })
    },
    /*
    Function to view size chart attributes
     */
    view_size_chart: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        console.log(row);
        frappe.call({
            method: 'versa_system.versa_system.custom_scripts.lead.lead.fetch_size_chart_details',
            args: {
                'reference': row.reference
            },
            callback: function(response) {
                if (response.message && response.message.length > 0) {
                    let size_html = '<table class="table table-bordered">';
                    size_html += '<tr><th>Attribute</th><th>Value</th><th>UOM</th></tr>';
                    response.message.forEach(attr => {
                        size_html += `<tr><td>${attr.attribute}</td><td>${attr.value}</td><td>${attr.uom}</td></tr>`;
                    });

                    size_html += '</table>';

                    frappe.msgprint({
                        title: 'Size Attributes',
                        message: size_html
                    });
                } else {
                    frappe.msgprint(__('No size attributes available for this Feasibility Solution.'));
                }
            }
        });
    }
});


frappe.ui.form.on('Feasibility Check', {
    validate: function(frm) {
        // Check if all "Go Forward" checkboxes in the child table are checked
        var allChecked = frm.doc.properties.every(function(row) {
            return row.go_forward;
        });

        // Set the "Go Forward" checkbox in the parent document accordingly
        frm.set_value('go_forward', allChecked);
    }
});
