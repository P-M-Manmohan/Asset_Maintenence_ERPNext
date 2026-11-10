### Asset Maintenence

Employees can post requests for asset maintenence

### Maintenance request workspace

After installing or migrating the app, open **`/maintenance-requests`**. This is a website page and asks guests to sign in before viewing or submitting requests. Assign the **Maintenance User** role to employees who submit requests and the **Maintenance Worker** role to the maintenance team. Each employee's Frappe User account must be linked in the Employee record's **User ID** field and the Employee record must be Active.

Employees can create requests, view and filter their own requests, edit open requests, and cancel open requests. Maintenance workers can filter the shared queue, accept open requests, and complete or reject in-progress work with feedback. Access is checked on the server as well as in the page.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app asset_maintenence
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/asset_maintenence
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
