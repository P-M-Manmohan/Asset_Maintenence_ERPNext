import frappe


def create_roles():
	for role in ("Maintenance User", "Maintenance Worker"):
		if not frappe.db.exists("Role", role):
			frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert(ignore_permissions=True)
