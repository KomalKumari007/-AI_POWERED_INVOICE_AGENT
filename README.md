## 🎯 Project Motive
Manual expense auditing in corporate environments is historically slow, labor-intensive, and highly prone to human error. The motive behind building this platform was to engineer an autonomous, secure, and production-ready system capable of processing complex transactional documents instantly. By shifting from manual validation to an intelligent, agentic workflow, this project demonstrates how modern AI can eliminate operational overhead and enforce corporate compliance flags automatically.

---

## 🛑 The Problem
Corporate compliance teams face two major bottlenecks when managing vendor invoices:
* **Unstructured Data Chaos:** Invoices come in varying layouts, structural formats, and document templates (mostly unsearchable PDFs), making standard rule-based parsing algorithms fail.
* **Compliance Overlook & Double-Billing:** Human auditors frequently miss strict policy breaches (such as single-item meal overages) or subtle vendor double-billing schemes where identical totals are submitted under slightly altered line items.

---

## 💡 The Solution
This platform addresses these issues by combining a robust front-end workstation with an intelligent **Agentic Retrieval-Augmented Generation (RAG)** backend:
* **Autonomous Document Parsing:** The system extracts raw text layout sequences from uploaded files and feeds them directly to an AI agent capable of understanding structural context.
* **Dynamic Policy Enforcement:** Instead of rigid hardcoded scripts, the engine uses structured system instructions to evaluate line items against company guardrails on the fly.
* **Safe State Routing:** The application safely manages dynamic user queries through a specialized configuration layer, executing analytical loops and returning a definitive compliance ruling (**"COMPLIANT / APPROVED"** or **"FLAGGED"**) in seconds.

---

## 🛠️ Tech Stack & Tools Used
* **Python:** The core programming language used to build the backend routing logic, manage environment variable configurations, and handle data layers defensively.
* **Google GenAI SDK (Gemini API):** Utilized to power the central AI auditing agent, leveraging its advanced capability to parse unstructured layouts and execute complex evaluation loops.
* **Streamlit:** Selected to build a highly responsive, clean corporate dashboard, enabling seamless drag-and-drop file operations and real-time query inputs.
* **PyPDF:** Used as a lightweight, reliable extraction tool to cleanly scrape unstructured textual data blocks directly from PDF invoice uploads.
* **Python-Dotenv:** Integrated to securely isolate and handle private environment credentials, keeping enterprise security standards intact by separating code from API validation keys.
