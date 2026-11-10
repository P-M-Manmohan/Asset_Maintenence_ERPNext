import frappe


def get_context(context):
	context.no_cache = 1
	context.logged_in = frappe.session.user != "Guest"
	context.can_manage_requests = context.logged_in and (
		"Maintenance Worker" in frappe.get_roles() or "System Manager" in frappe.get_roles()
	)
	return context
