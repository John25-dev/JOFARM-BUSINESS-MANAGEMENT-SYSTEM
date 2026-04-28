# JOFARM Business Management System

A high-security, production-ready management system for monitoring daily operations, stock balancing, employee tracking, and veterinary client records.

## 🔐 Security Features
- **Tiered Access Control:** Role-based logic (Admin, Manager, Employee).
- **Password Encryption:** Uses Bcrypt for secure credential storage.
- **Reverse Proxy Protection:** Configured for Apache and Cloudflare WAF.
- **Database Safety:** D1/SQLite files are protected from public access.

## 📁 Project Structure
- `app.py`: Backend API with security gatekeepers.
- `index.html`: Adaptive frontend that hides features based on user rights.
- `apache_vhost.conf`: Server-level security and traffic routing.
- `.gitignore`: Prevents sensitive and temporary files from leaking.

## 🚀 Deployment Instructions
1. **GitHub:** Push these files to your repository (ensure no `.txt` extensions).
2. **Cloudflare:** - Connect your GitHub repo to a Cloudflare Worker/Page.
   - Create a D1 Database named `jofarm_records`.
   - Add a **D1 Binding** in settings with the Variable name `DB`.
3. **Environment:**
   - Ensure `requirements.txt` is processed during build.

## 🛠 Tech Stack
- **Frontend:** Tailwind CSS
- **Backend:** Flask (Python)
- **Database:** Cloudflare D1 (SQL)
- **Security:** Flask-Bcrypt & Cloudflare WAF