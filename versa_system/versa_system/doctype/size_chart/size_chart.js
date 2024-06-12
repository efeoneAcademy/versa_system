

frappe.ui.form.on('Size Chart', {
    onload: function(frm) {
        frm.set_query('reference_doctype', function() {
            return {
              "filters":{
                module: 'Versa System'
              }

            };
        });
    }
});
