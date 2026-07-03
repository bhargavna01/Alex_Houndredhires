# Alex_Houndred_hires
Alex Houndred_hires repository

---

## 🎯 Selected Research Topic: **`AI-powered SEO content production`**

### Why this topic was chosen:
Traditional SEO is undergoing a massive shift due to the introduction of AI-powered search engines (e.g., Google's AI Overviews, Search Generative Experience, and Generative Engine Optimization). To succeed in this new landscape, businesses must pivot from manual search tactics to automated, semantic, and high-quality content production. 

This topic was chosen to design and build a pipeline that:
1. **Identifies Real-World Experts**: Curation of a database of SEO practitioners who actively run data experiments on AI-SEO campaigns rather than just theoretical strategy.
2. **Automates Content Sourcing**: Building python utilities to retrieve and clean LinkedIn posts and YouTube transcripts from leading SEO minds.
3. **Implements Programmatic Scaling**: Researching modern automation tools (such as n8n, Topical Authority Maps, and NLP-based optimization) to scale high-quality organic content creation.

---

# Project Setup and Environment Configuration

This repository contains the documentation for the initial development environment setup, including the tools installed, configuration steps completed, and troubleshooting for the IDE user interface.

---

## 🛠️ Tools Installed

The following tools and extensions were installed to establish the development environment:

* **Cursor IDE:** The primary AI-powered development environment (installed via the official website).
* **Extensions & Add-ons:**
    * **GitHub:** For repository management, version control, and seamless remote tracking.
    * **Google Cloud Code (claudecode):** For cloud platform integration and deployment workflows.
    * **Codex:** For AI-assisted code completion and contextual development support.
    * **Cline (Automation):** An advanced AI agent framework configured directly within the IDE environment to handle complex, multi-step automation tasks and autonomous file changes.
    * **Commit Sage:** Utilized for advanced, AI-powered commit message generation and robust management of LLM model API keys (ensuring encrypted, centralized credential mapping).

---

## 📋 Steps Completed

1.  **Repository Creation:** Initialized this GitHub repository to host and track project files.
2.  **IDE Installation:** Downloaded and installed the latest version of the Cursor IDE from the official website.
3.  **UI Troubleshooting & Reconfiguration:** Identified and resolved UI layout changes to restore standard sidebar and extension controls (detailed below).
4.  **Extension Deployment:** Navigated to the marketplace/extensions view and successfully installed the **GitHub**, **Cloud Code**, **Codex**, **Cline**, and **Commit Sage** extensions.
5.  **Authentication & Extension Onboarding:** Authenticated and logged into all installed extensions to ensure API keys, cloud profiles, and repository access tokens were properly synced.
6.  **Documentation:** Created this `README.md` file to log the setup process for client transparency.

---

## 🔍 Issues Encountered & Resolutions

### The "Missing" Extensions Icon / Agentic UI Confusion

* **Issue:** Upon launching the newly installed Cursor IDE, the interface looked entirely different from previous standard VS Code setups from a few months ago. The traditional sidebar,
* along with the Extensions/Add-ons icon, was missing. The IDE defaulted to a highly streamlined, **"Agentic" UI layout**.
* **Resolution:** 
    1. Took a screenshot of the unfamiliar interface and utilized Gemini AI to identify where the layout controls were mapped.
    2. Discovered that Cursor's modern layout hides traditional panels by default to prioritize agentic workflows.
    3. Navigated to the editor settings window and switched the UI preference from the **Modern layout** back to the **Classic/Older layout**. 
    4. This instantly restored the familiar activity bar, allowing access to the Extensions marketplace to finish installing the required tools and successfully executing the login/auth procedures for each.

---

## 🔄 Development Transition & LLM Tooling Journey

This project was built using a hybrid model approach across different development tools and Large Language Models (LLMs) to ensure completion under constraints:

1. **Initial Phase (Cursor & Claude Code)**: The first half of the project was developed using Claude Code within the Cursor IDE. Due to token limitations on Cursor's free tier, a transition was made to Antigravity (Gemini-powered IDE) to fulfill all project requirements on time.
2. **Data Sourcing (Perplexity & Comet Browser Assistant)**: To scrape, scrub, and compile the expert profile data, we utilized Perplexity AI in combination with the Comet browser assistant.
3. **Multi-Model Orchestration**: Throughout the project, various LLM models and token allocations were strategically managed and combined to optimize context limits and build the current pipelines.

---

## 📊 Profile Selection & Expert Filtering

The expert research database was curated using a multi-stage selection process:

1. **Initial Selection (35+ Candidates)**: The complete initial screening pool of candidates is cataloged in the external spreadsheet:
   - **Google Sheet Link**: [Alex Houndred Hires Selected Profiles Spreadsheet](https://docs.google.com/spreadsheets/d/1ONKwwYx_QyoVWoaVE_3k3k5iGHVGVENPDcjz4HLSxa8/edit?gid=1999288685#gid=1999288685)
2. **Filtering Criteria & Methodology**: The initial pool of profiles was filtered down to the **Top 10 Selected Experts** and **Honorable Mentions** based on specific criteria documented in [sources.md](file:///Users/bhargavnayak/.gemini/antigravity-ide/scratch/Alex_Houndredhires/research/sources.md). These criteria are:
   - **Relevance Filter**: The candidate must directly address and specialize in AI-powered SEO content production.
   - **Practitioner Test**: The candidate must demonstrate hands-on experience by building or running actual AI content systems, publishing real data experiments rather than just theoretical strategy.
   - **Platform Diversity**: Curation of a balanced mix of creators across YouTube, LinkedIn, podcasts, and blogs.
   - **Content Freshness**: Active engagement in 2025–2026 with recent insights.
   - **Unique Angle**: Each expert must bring a distinct perspective (e.g., semantic SEO, n8n automations, GEO/AEO optimization).
   - **Actionability**: Content must provide replicable systems, prompts, or workflows.
3. **Final Selection**: The resulting profiles, details, and platform links for the selected experts are stored in [sources.md](file:///Users/bhargavnayak/.gemini/antigravity-ide/scratch/Alex_Houndredhires/research/sources.md).

---

## 🚀 Version Control

To save these changes and sync them with the remote repository, execute the following commands in your terminal:

```bash
git add README.MD
git commit -m "docs: add environment setup, automation extensions, UI troubleshooting, transition details, and selected profiles to README"
git push origin main
```
