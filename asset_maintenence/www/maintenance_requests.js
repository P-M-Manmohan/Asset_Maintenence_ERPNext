frappe.ready(function () {
	const root = document.querySelector(".maintenance-portal");
	if (!root || root.dataset.authenticated !== "1") return;
	const canManage = root.dataset.canManage === "1";
	let view = canManage ? "worker" : "employee";
	let hideClosed = false;
	let assets = [];

	function call(method, args, done) {
		frappe.call({ method, args, callback: (response) => { if (response.message && done) done(response.message); } });
	}

	function load() {
		call("asset_maintenence.api.get_dashboard_data", {
			view,
			status: document.getElementById("status-filter").value,
			priority: document.getElementById("priority-filter").value,
			from_date: document.getElementById("from-filter").value,
			to_date: document.getElementById("to-filter").value,
			hide_closed: hideClosed ? 1 : 0,
		}, (data) => { assets = data.assets || []; render(data.requests || []); });
	}

	function render(requests) {
		const target = document.getElementById("request-list");
		if (!requests.length) {
			target.innerHTML = '<p class="text-muted text-center" style="padding:36px">No maintenance requests found.</p>';
			return;
		}
		target.innerHTML = requests.map((request) => {
			const statusClass = `status-${slug(request.status)}`;
			const priorityClass = `priority-${slug(request.priority)}`;
			let actions = "";
			if (view === "employee" && request.status === "Open") actions = `<button class="btn btn-xs btn-default" data-action="edit" data-name="${esc(request.name)}">Edit</button> <button class="btn btn-xs btn-default" data-action="cancel" data-name="${esc(request.name)}">Cancel</button>`;
			if (view === "worker" && request.status === "Open") actions = `<button class="btn btn-xs btn-primary" data-action="accept" data-name="${esc(request.name)}">Accept</button>`;
			if (view === "worker" && request.status === "In Progress") actions = `<button class="btn btn-xs btn-primary" data-action="complete" data-name="${esc(request.name)}">Complete</button> <button class="btn btn-xs btn-default" data-action="reject" data-name="${esc(request.name)}">Reject</button>`;
			return `<article class="request-card ${priorityClass}"><div class="request-card-head"><div><strong>${esc(request.name)}</strong> · ${esc(request.asset)}<span class="request-status ${statusClass}">${esc(request.status)}</span></div><div class="request-card-actions">${actions}</div></div><p style="margin-top:10px">${esc(request.issue_description)}</p><div class="request-meta">Employee: ${esc(request.employee)} · Requested: ${esc(request.request_date)} · Priority: <span class="request-priority ${priorityClass}">${esc(request.priority)}</span> · Assigned to: ${esc(request.assigned_to || "Unassigned")}</div>${request.feedback ? `<div class="request-feedback"><strong>Update:</strong> ${esc(request.feedback)}</div>` : ""}</article>`;
		}).join("");
	}

	function slug(value) {
		return String(value || "").toLowerCase().replace(/\s+/g, "-").replace(/[^a-z-]/g, "");
	}

	function esc(value) {
		const element = document.createElement("span");
		element.textContent = value || "";
		return element.innerHTML;
	}

	function openRequest(request) {
		const assetSelect = document.getElementById("request-asset");
		assetSelect.innerHTML = assets.map((asset) => `<option value="${esc(asset.name)}">${esc(asset.asset_name || asset.name)} (${esc(asset.name)})</option>`).join("");
		document.getElementById("request-description").value = request ? request.issue_description : "";
		document.getElementById("request-priority").value = request ? request.priority : "Medium";
		if (request) assetSelect.value = request.asset;
		document.getElementById("request-modal-title").textContent = request ? "Edit Request" : "New Maintenance Request";
		document.getElementById("save-request").textContent = request ? "Save" : "Submit request";
		$("#request-modal").modal("show");
		document.getElementById("save-request").onclick = function () {
			const values = { asset: assetSelect.value, priority: document.getElementById("request-priority").value, issue_description: document.getElementById("request-description").value.trim() };
		if (!values.asset || !values.issue_description) return frappe.msgprint("Choose an asset and describe the issue.");
			call(request ? "asset_maintenence.api.edit_request" : "asset_maintenence.api.create_request", request ? { name: request.name, ...values } : values, () => { $("#request-modal").modal("hide"); load(); });
		};
	}

	document.getElementById("filter-requests").addEventListener("click", load);
	document.getElementById("toggle-closed-requests")?.addEventListener("click", (event) => {
		hideClosed = !hideClosed;
		event.currentTarget.textContent = hideClosed ? "Show completed & rejected" : "Hide completed & rejected";
		load();
	});
	document.getElementById("new-request")?.addEventListener("click", () => openRequest());
	document.getElementById("request-list").addEventListener("click", (event) => {
		const button = event.target.closest("[data-action]");
		if (!button) return;
		const { action, name } = button.dataset;
		if (action === "edit") return call("asset_maintenence.api.get_request", { name }, openRequest);
		if (action === "cancel") return frappe.confirm("Cancel this open request?", () => call("asset_maintenence.api.cancel_request", { name }, load));
		if (action === "accept") return call("asset_maintenence.api.update_request", { name, status: "In Progress" }, load);
		const status = action === "complete" ? "Completed" : "Rejected";
		const feedback = window.prompt(`Add feedback for the employee before marking this ${status.toLowerCase()}.`);
		if (feedback && feedback.trim()) call("asset_maintenence.api.update_request", { name, status, feedback: feedback.trim() }, load);
	});

	load();
});
