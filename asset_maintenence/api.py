import frappe
from frappe import _

DOCTYPE = "Asset Maintenence"
EMPLOYEE_ROLE = "Maintenance User"
WORKER_ROLE = "Maintenance Worker"
TERMINAL_STATUSES = ("Completed", "Rejected", "Cancelled")


def _is_worker(user=None):
	user = user or frappe.session.user
	return user == "Administrator" or "System Manager" in frappe.get_roles(user) or WORKER_ROLE in frappe.get_roles(user)


def _employee_for_user(user=None):
	user = user or frappe.session.user
	return frappe.db.get_value("Employee", {"user_id": user, "status": "Active"}, "name")


def _require_employee():
	if EMPLOYEE_ROLE not in frappe.get_roles():
		frappe.throw(_("You need the Maintenance User role to submit or review requests."), frappe.PermissionError)
	employee = _employee_for_user()
	if not employee:
		frappe.throw(_("Your user is not linked to an active Employee record."), frappe.PermissionError)
	return employee


def get_request_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_worker(user):
		return ""
	employee = _employee_for_user(user)
	if not employee:
		return "1=0"
	return "`tabAsset Maintenence`.employee = " + frappe.db.escape(employee)


def has_request_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_worker(user):
		return True
	employee = _employee_for_user(user)
	if not employee or doc.employee != employee:
		return False
	if permission_type in ("write", "delete"):
		return doc.status == "Open"
	return True


def _require_worker():
	if not _is_worker():
		frappe.throw(_("Only maintenance workers can manage requests."), frappe.PermissionError)


@frappe.whitelist()
def get_dashboard_data(view="employee", status=None, priority=None, from_date=None, to_date=None, hide_closed=0):
	if view not in ("employee", "worker"):
		frappe.throw(_("Invalid dashboard view."))
	if view == "worker":
		_require_worker()
		filters = {}
	else:
		employee = _require_employee()
		filters = {"employee": employee}
	if status:
		filters["status"] = status
	elif view == "worker" and frappe.utils.cint(hide_closed):
		filters["status"] = ["not in", ["Completed", "Rejected"]]
	if priority:
		filters["priority"] = priority
	if from_date and to_date:
		filters["request_date"] = ["between", [from_date, to_date]]
	elif from_date:
		filters["request_date"] = [">=", from_date]
	elif to_date:
		filters["request_date"] = ["<=", to_date]
	fields = ["name", "employee", "asset", "request_date", "priority", "status", "assigned_to", "issue_description", "feedback", "modified"]
	list_method = frappe.get_all if view == "worker" else frappe.get_list
	requests = list_method(DOCTYPE, filters=filters, fields=fields, order_by="creation desc", limit_page_length=200)
	assets = frappe.get_all(
		"Asset",
		filters={"status": ["in", ["Submitted", "Partially Depreciated", "Fully Depreciated"]]},
		fields=["name", "asset_name"],
		order_by="asset_name asc",
		limit_page_length=500,
	) if view == "employee" else []
	return {"requests": requests, "assets": assets, "employee": _employee_for_user() if view == "employee" else None}


@frappe.whitelist()
def get_request(name):
	doc = frappe.get_doc(DOCTYPE, name)
	if _is_worker():
		_require_worker()
	else:
		doc.check_permission("read")
	return {field: doc.get(field) for field in ("name", "employee", "asset", "request_date", "priority", "status", "assigned_to", "issue_description", "feedback")}


@frappe.whitelist()
def create_request(asset, priority, issue_description):
	if _is_worker():
		frappe.throw(_("Maintenance workers cannot submit employee requests."), frappe.PermissionError)
	employee = _require_employee()
	doc = frappe.get_doc({
		"doctype": DOCTYPE,
		"employee": employee,
		"asset": asset,
		"request_date": frappe.utils.today(),
		"priority": priority,
		"issue_description": issue_description,
		"status": "Open",
	})
	doc.insert()
	return {"name": doc.name}


@frappe.whitelist()
def edit_request(name, asset, priority, issue_description):
	doc = frappe.get_doc(DOCTYPE, name)
	if not has_request_permission(doc, permission_type="write") or _is_worker():
		frappe.throw(_("You can only edit your own open requests."), frappe.PermissionError)
	doc.asset = asset
	doc.priority = priority
	doc.issue_description = issue_description
	doc.save()
	return {"name": doc.name}


@frappe.whitelist()
def cancel_request(name):
	doc = frappe.get_doc(DOCTYPE, name)
	if _is_worker() or not has_request_permission(doc, permission_type="write"):
		frappe.throw(_("You can only cancel your own open requests."), frappe.PermissionError)
	doc.status = "Cancelled"
	doc.feedback = "Cancelled by employee"
	doc.save()
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist()
def update_request(name, status, feedback=None):
	_require_worker()
	if status not in ("In Progress", "Completed", "Rejected"):
		frappe.throw(_("Invalid request status."))
	doc = frappe.get_doc(DOCTYPE, name)
	if doc.status in TERMINAL_STATUSES:
		frappe.throw(_("This request is already closed."))
	if status == "In Progress" and doc.status != "Open":
		frappe.throw(_("Only open requests can be accepted."))
	if status in ("Completed", "Rejected") and doc.status != "In Progress":
		frappe.throw(_("Only in progress requests can be completed or rejected."))
	doc.status = status
	if status == "In Progress":
		doc.assigned_to = frappe.session.user
	if status in ("Completed", "Rejected"):
		doc.feedback = (feedback or "").strip()
	doc.save(ignore_permissions=True)
	return {"name": doc.name, "status": doc.status}
