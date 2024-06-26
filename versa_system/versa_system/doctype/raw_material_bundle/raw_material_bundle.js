frappe.ui.form.on('Raw Material Bundle', {
    onload: function(frm) {
        frm.set_query('reference_doctype', function() {
            return {
                "filters": {
                    module: 'Versa System'
                }
            };
        });

        set_item_code_query(frm);  
    }
});

function set_item_code_query(frm) {
    /*
    * Function sets filter on item_code field in raw_material child table
    * to show only items with item_group 'Raw Material'
    */
    frm.fields_dict['raw_material'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
        return {
            filters: [
                ["item_group", "=", "Raw Material"]
            ]
        };
    };
}

function calculate_total_amount(frm, cdt, cdn) {
    /**
    * Function to calculate total amount based on quantity and rate.
    */
    let d = locals[cdt][cdn];
    let amt = d.quantity * d.rate;
    frappe.model.set_value(cdt, cdn, 'total_amount', amt);
}

frappe.ui.form.on('Raw Material', {
    quantity: function(frm, cdt, cdn) {
        calculate_total_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_total_amount(frm, cdt, cdn);
    }
});
