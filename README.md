# Family Bank

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, view-only static website that displays a list of transactions and the current balance for a child's "bank account". Data updates are performed offline using a Python command-line tool that modifies a JSON file stored in the project's Git repository. Pushing the updated JSON triggers an automatic rebuild and deployment on Vercel via Hugo.

**Disclaimer:** This app was coded by AI. My intent is to test how fast I can have simple applications built because I want them for personal reasons. My goals are to learn how to work with AI and learning to review code written.

## Features

* **Static Site:** Pure HTML/CSS generated by Hugo. No backend or database needed for viewing.
* **Offline Updates:** Transactions are added via a local Python script.
* **Version Controlled Data:** Transaction history is stored in `data/transactions.json` and tracked via Git.
* **Automatic Deployment:** Pushing changes to Git triggers a redeploy on Vercel.
* **Simple & Clear:** Minimalist design focused on displaying transaction history and current balance.
* **JSON Data Source:** Uses a simple JSON array of objects for robust data handling.

## Tech Stack

* **Static Site Generator:** Hugo (Extended version recommended)
* **Data Storage:** JSON file (`data/transactions.json`)
* **Update Tool:** Python 3 (using only standard libraries: `json`, `datetime`, `argparse`, `os`, `sys`)
* **Version Control:** Git
* **Hosting/Deployment:** Vercel (Free Tier)
* **Development Environment:** Nix Flake, Direnv

## User Guide (Updating the Balance)

This describes how a parent typically adds a transaction.

**Prerequisites:**

* Git
* Nix (with flakes enabled)
* Direnv

**Steps:**

1.  **Clone the Repository (if first time):**
    ```bash
    git clone <your-repository-url.git>
    cd <repository-folder-name>
    ```
2. **Enable Direnv**
    ```bash
    direnv allow
    ```
3.  **Ensure you are on the main branch and up-to-date:**
    ```bash
    git checkout main
    git pull origin main
    ```
4.  **Run the Python script:**
    Open your terminal in the project's root directory.
    * **Add a deposit:**
        ```bash
        python manage_bank.py <positive_amount> -d "<description>"
        # Example:
        python manage_bank.py 10.50 -d "Allowance"
        ```
    * **Add a withdrawal:**
        ```bash
        python manage_bank.py <negative_amount> -d "<description>"
        # Example:
        python manage_bank.py -5.00 -d "Bought book"
        ```
    The script will confirm the transaction details and the new balance. It modifies the `data/transactions.json` file.

5.  **Commit the Change:**
    ```bash
    git add data/transactions.json
    git commit -m "Add transaction: <description>"
    # Example:
    # git commit -m "Add transaction: Allowance"
    ```
6.  **Push the Change:**
    ```bash
    git push origin main
    ```
7.  **Wait for Vercel:** Vercel will automatically detect the push, rebuild the Hugo site with the updated JSON data, and deploy the changes (usually takes under a minute).
8.  **View:** Navigate to your Vercel site URL (e.g., `https://your-vercel-url.vercel.app/transactions/`) to see the updated balance and transaction list.

## Developer Setup

This describes how to set up the environment to run Hugo locally or modify the site/script.

**Prerequisites:**

* Git
* Nix (with flakes enabled)
* Direnv
* Vercel Account (Optional, for deploying your own instance)
* GitHub/GitLab/etc. account for hosting your repository fork/clone.

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url.git>
    cd <repository-folder-name>
    ```
2. **Enable Direnv**
    ```bash
    direnv allow
    ```
3. **Run Hugo Locally:**
    ```bash
    hugo server
    ```
    Hugo will build the site and serve it locally, typically at `http://localhost:1313/`. Open `http://localhost:1313/transactions/` in your browser. The server watches for changes.
4.  **Test Python Script:** You can run `python manage_bank.py ...` as described in the User Guide. When `data/transactions.json` is updated, the running `hugo server` should detect the change and automatically rebuild the site in memory. Refresh your browser to see the updates.
5.  **Deploying Your Own Instance:**
    * Push your cloned/modified repository to your own Git hosting account (e.g., GitHub).
    * Connect your Vercel account to your Git provider.
    * Import the Git repository into Vercel.
    * Vercel should automatically detect it as a Hugo project. Use the default Hugo build settings.
    * Deploy!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
