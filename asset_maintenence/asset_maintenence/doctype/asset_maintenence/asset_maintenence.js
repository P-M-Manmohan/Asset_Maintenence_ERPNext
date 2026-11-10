// Copyright (c) 2026, Manmohan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Asset Maintenence", {
	refresh(frm) {
		frm.toggle_display(
			"feedback",
			["Completed", "Rejected", "Cancelled"].includes(frm.doc.status)
		)

		if (["Completed", "Rejected", "Cancelled"].includes(frm.doc.status)) {
			frm.disable_form();
		} else {
			frm.enable_form();
		}

		frm._status_confirmation_done = false;
	},

	setup(frm){

		frm.set_query("asset", function() {
			return {
				filters: {
					status: ["in", ["Submitted", "Partially Depreciated", "Fully Depreciated"]]
				}
			};
		});

	},

	before_save(frm) {
		const requires_confirmation = ["Completed", "Rejected"].includes(
				frm.doc.status
			);

			if (requires_confirmation && !frm._status_confirmation_done) {

				frappe.validated = false;

				frappe.confirm(
					`Are you sure you want to mark this request as ${frm.doc.status}?`,

					function() {
						// User confirms
						frm._status_confirmation_done = true;
						frm.save();
					},

					function() {
						// User cancels
						frm._status_confirmation_done = false;
					}
				);
			}

	},



	status(frm){
		frm.toggle_display(
			"feedback",
			["Completed", "Rejected", "Cancelled"].includes(frm.doc.status)
		)
	}
});
