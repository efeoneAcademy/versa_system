// Copyright (c) 2024, efeone and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Features", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Features', {
    onload: function(frm) {
        frm.set_query('reference_doctype', function() {
            return {
                "filters": {
                    module: 'Versa System'
                }
            };
        });
    }
});
