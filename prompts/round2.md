# Project Requirements: Kids Bank Static Site

## Project Goal

To create a simple, view-only static website, deployed on Vercel, that displays a list of transactions and the current balance for a child's "bank account". Data updates are performed offline using a Python command-line tool that modifies a **JSON file** stored in the project's Git repository. Pushing the updated JSON triggers an automatic rebuild and deployment on Vercel via Hugo.

## Core Workflow

1.  **Initialization:** A Hugo project is set up with a specific data file (`data/transactions.json`) and a layout template designed to display its contents. The project is hosted in a Git repository (e.g., GitHub).
2.  **Data Update:** The parent runs a Python script (`manage_bank.py`) locally, providing transaction details (amount, description) via command-line arguments.
3.  **Script Execution:** The Python script reads the current `data/transactions.json`, parses the JSON array, calculates the new running balance based on the *last entry* in the array, creates a new transaction object (dictionary), appends it to the list, and writes the *entire updated list* back to `data/transactions.json`, overwriting the file.
4.  **Commit & Push:** The parent commits the modified `data/transactions.json` file to the Git repository and pushes it to the main branch.
5.  **Vercel Trigger:** Vercel automatically detects the push to the connected Git repository branch.
6.  **Vercel Build:** Vercel checks out the latest code and runs the Hugo build process (`hugo` command).
7.  **Hugo Processing:** Hugo automatically identifies and parses `data/transactions.json` within its `data` directory, making the data available via `site.Data.transactions`.
8.  **Template Rendering:** The predefined Hugo layout (`layouts/_default/list.html`) accesses this data using `site.Data.transactions`. Hugo's templating engine iterates through the transaction objects (likely sorted chronologically) and renders an HTML page displaying the transaction history and the final balance.
9.  **Vercel Deployment:** Vercel deploys the generated static HTML, CSS, and (if any) JavaScript files to its global CDN.
10. **Viewing:** The child (or parent) navigates to the Vercel URL (e.g., `https://kids-bank.[your-vercel-domain].app/transactions/`) to view the up-to-date transaction list and balance.

## Technology Stack

* **Static Site Generator:** Hugo (latest stable version recommended)
* **Data Storage:** JSON file (`data/transactions.json`)
* **Update Tool:** Python 3 (using only standard libraries: `json`, `datetime`, `argparse`, `os`, `sys`)
* **Version Control:** Git
* **Hosting/Deployment:** Vercel (Free Tier)

## Key Requirements & Constraints

* **Purely Static Site:** The live website must consist only of static HTML/CSS/JS files served directly from Vercel's CDN. No server-side rendering or runtime database lookups on the live site. Data is baked in at build time.
* **Offline Updates Only:** Data modification happens exclusively through the local Python CLI tool (`manage_bank.py`) and subsequent Git commits/pushes.
* **Data Storage (`data/transactions.json`):**
    * Must be located at `data/transactions.json` within the Hugo project root.
    * Must be a valid JSON file containing a single array `[]`.
    * The array contains zero or more transaction objects.
    * Each transaction object must have the following keys:
        * `timestamp`: String, ISO 8601 format, UTC recommended (e.g., `"2025-03-26T16:00:00Z"`).
        * `description`: String (e.g., `"Allowance"`).
        * `amount`: Number (float or integer, e.g., `10.50`, `-5`).
        * `balance`: Number (float or integer), representing the running balance *after* this transaction occurred.
* **Python Script (`manage_bank.py`):**
    * Must be located at the project root.
    * Must use only Python 3 standard libraries. No external packages required (simplifies setup).
    * Accepts command-line arguments: `amount` (positional, string convertible to float) and `-d`/`--description` (required string).
    * Reads the existing `data/transactions.json` file using the `json` module.
    * Handles file not found, empty file, or invalid JSON gracefully (e.g., by starting with an empty list `[]` or assuming a starting balance of 0).
    * Calculates the new running balance based on the `balance` value of the *last* object in the JSON array (if the array is not empty, otherwise starts from 0).
    * Creates a new Python dictionary representing the transaction with `timestamp`, `description`, `amount` (numeric), and calculated `balance` (numeric).
    * Appends this new dictionary to the list read from the JSON file.
    * Writes the **entire modified list** back to `data/transactions.json` using `json.dump`, overwriting the file (`'w'` mode). Use indentation (`indent=2` or `indent=4`) for human readability.
* **Hugo Setup:**
    * Utilizes the data from `data/transactions.json` made available automatically by Hugo as `site.Data.transactions`.
    * A layout template (e.g., `layouts/_default/list.html`) renders the data, triggered by a content file like `content/transactions/_index.md`.
    * Displays transactions chronologically, preferably newest first (e.g., using `range sort .Site.Data.transactions "timestamp" "desc"`).
    * Each displayed transaction must show timestamp, description, amount, and the running balance after that transaction. Format numeric values clearly (e.g., two decimal places for currency).
    * Clearly display the final, current balance (obtained from the `balance` field of the last transaction object in the `site.Data.transactions` data).
    * Gracefully handle the case where `site.Data.transactions` is null, empty, or doesn't contain valid data.
* **Deployment:** Deployed on Vercel via Git integration. Automatic builds triggered on push to the designated production branch (e.g., `main`). Vercel's Hugo framework preset should be used.
* **Authorization:** Implicit authorization model based solely on write access (commit/push permissions) to the project's Git repository.
* **Simplicity:** Minimize complex configurations, external dependencies, and build steps. Avoid JavaScript for core data display functionality; rely on Hugo's templating.

## Notes & Pitfalls Avoided (Guidance for Future Iteration)

* **Data Format Choice:** JSON stored in `data/transactions.json` was chosen for its robustness and native handling by Hugo's data loading mechanism (`site.Data.transactions`). This proved much more reliable than initial attempts with CSV.
* **Avoid CSV in `/data` for Structured Access:** Do not place CSV files in Hugo's `/data` directory if you expect Hugo to automatically parse them into structured data using the header row. Hugo often treats these as raw `[][]string` arrays, leading to errors when trying to access data by field name (e.g., `.timestamp`). This was a major pitfall encountered during development.
* **CSV Processing in `/assets`:** If CSV *must* be used, place it in `/assets` and process using `resources.Get | transform.Unmarshal`. However, be aware that this approach is highly sensitive to CSV formatting errors, including missing headers, incorrect delimiters, non-standard quoting, invisible characters, and missing final newline characters. Debugging these issues can be time-consuming. Explicitly setting the `delimiter` and potentially `headers` in the `Unmarshal` options can help but won't fix a fundamentally malformed file.
* **JSON File Structure:** The Python script must read the *entire* JSON array, append the new transaction *object* to the Python list, and then write the *entire modified list* back to the file, overwriting it. Do not attempt to append raw JSON text to the file.
* **File Integrity:** Ensure text-based data files like JSON always use consistent encoding (UTF-8 without BOM recommended) and that the last line ends with a newline character. While JSON parsers might be more forgiving than some CSV parsers regarding the final newline, it's best practice. Tools like `cat -A` can help diagnose invisible characters or line ending issues.
* **Hugo Data Loading:** Leverage Hugo's automatic parsing of JSON/YAML/TOML files in the `/data` directory. It simplifies template code significantly compared to manual resource fetching and unmarshalling.