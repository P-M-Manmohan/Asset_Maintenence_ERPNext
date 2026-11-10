# Asset Maintenance Requests

Asset Maintenance Requests gives employees and the maintenance team one place to report asset problems and follow the work through to a decision. Employees submit requests against assets; maintenance workers review the shared queue, take ownership, and record the outcome.

## Open the maintenance request page

Sign in to your Frappe site and visit **`/maintenance-requests`**. You must be signed in to view or submit requests.

The page shows requests in a list. Use the status, priority, and date filters to narrow the list, then select **Filter**. Employees see their own requests. Maintenance workers see the shared queue and can choose to hide completed and rejected requests.

## Employee guide

### Submit a request

1. Open **`/maintenance-requests`** and select **New request**.
2. Choose the asset, set a priority, and describe the issue clearly.
3. Select **Submit request**.

The request is dated automatically and starts with **Open** status. Choose the priority that best reflects the urgency: Low, Medium, High, or Urgent.

### Follow up, edit, or cancel

Your requests appear on the page with their current status, assigned worker (when accepted), and any feedback from the maintenance team. You can edit or cancel a request while it is **Open**. Once a worker accepts it, the request can no longer be edited or cancelled by the employee.

## Maintenance team guide

The maintenance queue shows requests from all employees. Open a request card to review its asset, description, priority, and request date.

- Select **Accept** on an **Open** request to take it into **In Progress**. The accepting worker is shown as the assignee.
- For an **In Progress** request, select **Complete** or **Reject** and provide feedback for the employee.
- Completed and rejected requests are closed. They cannot be reopened through this page.

## Request statuses

| Status | Meaning |
| --- | --- |
| **Open** | Submitted and waiting for a maintenance worker. |
| **In Progress** | Accepted by a worker and being handled. |
| **Completed** | Work is complete; the worker has recorded feedback. |
| **Rejected** | The request was not accepted for work; the worker has recorded feedback. |
| **Cancelled** | The employee cancelled the request while it was still open. |

The normal flow is **Open → In Progress → Completed** or **Open → In Progress → Rejected**. An employee may cancel an **Open** request.

## Access and account setup

Ask your Frappe administrator if you cannot access the page or submit a request. The administrator needs to:

- Assign the **Maintenance User** role to employees who submit requests.
- Assign the **Maintenance Worker** role to maintenance team members who manage the queue.
- Link each employee's Frappe user account to their Employee record using **User ID**, and ensure the Employee record is **Active**.
- Ensure assets are available and active for selection in the request form.

Employees can see only requests linked to their own Employee record. Maintenance workers can see and manage the shared queue. System Managers can also manage requests.

## What to include in a request

Select the affected asset and describe the problem with enough detail to help the maintenance team assess it. Include symptoms, when the issue began, and any relevant context. Do not include information unrelated to the asset or repair.
