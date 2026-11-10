# Copyright (c) 2026, Manmohan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssetMaintenence(Document):

	def validate(self):
		self.validate_fields_filled()
		self.validate_request_date()
		self.validate_resolution_notes()
		self.validate_actor_changes()
		self.validate_transition()

	def validate_fields_filled(self):
		if not self.asset:
			frappe.throw("Asset cannot be empty")
		if not self.employee:
			frappe.throw("Employee cannot be empty")
		if not self.issue_description:
			frappe.throw("Issue description cannot be empty")


	def validate_request_date(self):
		if self.request_date and frappe.utils.getdate(self.request_date) > frappe.utils.getdate():
			frappe.throw("Request date cannot be in the future")

	def validate_resolution_notes(self):
		if self.status in ("Completed", "Rejected") and not self.feedback:
			frappe.throw("When rejecting or completing maintenance provide feedback")

	def validate_transition(self):

		allowed_transitions = {
			"Open": ["In Progress"],
			"In Progress": ["Completed", "Rejected"],
			"Completed": [],
			"Rejected": [],
			"Cancelled": []
		}

		prev_doc = self.get_doc_before_save()

		if not prev_doc:
			if self.status != "Open":
				frappe.throw("New requests must start with status 'Open'")
			return

		curr_status=self.status
		prev_status=prev_doc.status

		if prev_status == curr_status:
			return

		allowed_status = allowed_transitions.get(prev_status,[])

		if curr_status == "Cancelled" and prev_status == "Open":
			return

		if curr_status not in allowed_status:
			frappe.throw(f"Cannot change status from {prev_status} to {curr_status}.")

	def validate_actor_changes(self):
		prev_doc = self.get_doc_before_save()
		if not prev_doc:
			return

		roles = frappe.get_roles()
		is_worker = frappe.session.user == "Administrator" or "System Manager" in roles or "Maintenance Worker" in roles
		if is_worker:
			return

		employee = frappe.db.get_value(
			"Employee", {"user_id": frappe.session.user, "status": "Active"}, "name"
		)
		if not employee or prev_doc.employee != employee:
			frappe.throw("You can only update your own maintenance requests.", frappe.PermissionError)

		if self.status != prev_doc.status and not (prev_doc.status == "Open" and self.status == "Cancelled"):
			frappe.throw("Only maintenance workers can change request status.", frappe.PermissionError)

		editable_fields = {"asset", "priority", "issue_description", "status", "feedback"}
		for field in self.meta.fields:
			if not field.fieldname:
				continue
			if field.fieldname not in editable_fields and self.get(field.fieldname) != prev_doc.get(field.fieldname):
				frappe.throw("You cannot change these request fields.", frappe.PermissionError)
		if self.feedback != prev_doc.feedback and self.status != "Cancelled":
			frappe.throw("Only maintenance workers can add request feedback.", frappe.PermissionError)
		if self.status == "Cancelled" and self.feedback != "Cancelled by employee":
			frappe.throw("Employee cancellation notes cannot be changed.", frappe.PermissionError)


