frappe.ui.form.on('Account', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.client_id) {
			frm.add_custom_button(__('Authorize'), function() {
				frm.call({
					method: 'get_authorization_url',
					doc: frm.doc,
					callback: function(r) {
						if (r.message) {
							window.location.href = r.message;
						}
					}
				});
			});
		}
	}
});
