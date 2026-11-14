# Velcoris Industries — Website & Digital Infrastructure Review

**Role:** Digital Infrastructure & Backend-IT Fellowship  
**Deliverable:** Round 1 — Test by Fire Assignment  
**Prepared as:** Candidate working report / prototype documentation  
**Review date:** 14 November 2026

## Executive summary

The public website positions Velcoris Industries as an Indian industrial graphene manufacturer. Its messaging focuses on Few-Layer Graphene (FLG), Graphene Oxide (GO), domestic production, closed-loop processing, quality characterisation and industrial supply partnerships. The redesign prototype retains that materials-led positioning and gives prospective customers a clearer path from understanding materials to submitting an enquiry.

The accompanying Flask application demonstrates an end-to-end enquiry workflow: a visitor submits a form, the server validates the fields, the enquiry is stored in SQLite, and an authenticated administrator can review the record and update its status. The implementation is deliberately small enough to inspect and run locally. It is a proof of concept, not a claim about Velcoris's current private systems.

## Task 1 — Existing website analysis and redesign

### 1.1 Publicly observable website content

The following are observations from the public pages reviewed:

- **Homepage:** Positions Velcoris as an Indian industrial graphene manufacturer and communicates a cost, scale and sustainability proposition. It presents graphene science, industrial opportunity, recognition, and a sample-to-supply engagement path.
- **Technology page:** Describes a closed-loop carbon conversion platform, FLG and GO outputs, a six-stage manufacturing overview, technical specification categories and batch characterisation methods including Raman spectroscopy, XRD and particle-size analysis.
- **Company page:** Explains the company's mission, founder's note, leadership and operating-team information.
- **Contact page:** Invites sample, technical-datasheet and supply-partnership enquiries and gives contact channels and a stated response expectation.

These are descriptions of claims and content on the public website; this report does not independently validate the scientific, commercial or manufacturing claims.

### 1.2 UX review and opportunities

| Area | Review / opportunity | Proposed response in prototype |
|---|---|---|
| Positioning | Strong graphene/manufacturing story; visitors should quickly understand material options and next step | Hero explains advanced materials and provides clear sample/contact CTA |
| Navigation | Multiple information needs: materials, process, applications, company and contact | Short anchor navigation with visible sample CTA |
| Information hierarchy | Technical detail can be dense for first-time industrial buyers | Separate material cards, process stages and application list |
| Enquiry journey | Different intents (sample, technical discussion, partnership) benefit from structured capture | Enquiry type selector and concise form |
| Mobile usability | Must be verified on actual device widths and browsers | Responsive breakpoints, collapsible navigation and stacked sections |
| Accessibility | Ensure keyboard access, labels, status feedback and readable contrast | Semantic sections, explicit labels, focus styles and live form status |
| Trust and technical evidence | Technical claims should be paired with current, downloadable evidence where available | Prototype points visitors toward technical conversation; production site can link approved datasheets/COAs |

No unsupported assertion is made that the current live website is broken or non-responsive. Mobile behaviour, performance, accessibility and form handling should be tested in a browser with representative devices and assistive technology before being reported as defects.

### 1.3 Proposed information architecture

1. **Home:** Value proposition and primary call to action.
2. **Materials:** FLG and GO overview, with approved specifications and datasheet requests.
3. **Technology:** High-level process explanation, quality gates and evidence.
4. **Applications:** Use-case areas, clearly marked as potential areas subject to validation.
5. **Company:** Mission, team, facility and company information.
6. **Contact:** Sample, technical consultation, partnership and general enquiry paths.

### 1.4 Design rationale

The prototype uses a restrained dark-green/charcoal palette with a lime accent, technical typography, grid details and abstract layered-carbon artwork. This is intended to signal industrial precision and advanced materials without distracting from product information. High-contrast calls to action, concise section labels and repeatable content patterns support scanning. The layout collapses to a single-column mobile view and includes a mobile navigation toggle.

The design is a proposed concept, not official brand artwork. Before production use, Velcoris should approve brand colours, logo assets, imagery, technical wording and all performance claims. The prototype uses CSS-generated abstract visuals and does not reproduce proprietary facility imagery.

### 1.5 Prototype features

- Responsive landing page and navigation.
- Materials, technology, applications, company and contact sections.
- Enquiry form with required fields and clear confirmation/error feedback.
- Form fields for name, work email, organisation, enquiry type, subject and message.
- Hidden honeypot field as a basic anti-bot measure.

## Task 2 — Backend and IT infrastructure analysis

### 2.1 Existing technical setup: evidence and unknowns

The public website exposes rendered pages and browser-facing assets, but the reviewed public content does not establish the complete origin hosting provider, application framework, private API architecture, database, email platform or internal IT systems. These should be confirmed through authorised access or a technical handover from the organisation. A public frontend fingerprint or page appearance alone cannot prove a private backend stack.

| Area | Finding | Confidence |
|---|---|---|
| Public website | Public homepage and company, technology and contact pages are accessible | Observed |
| Content and positioning | Graphene manufacturing, FLG/GO, technology, quality and enquiry content are visible | Observed |
| Hosting provider | Not established from the reviewed public content | Unknown |
| Backend framework | Not established from the reviewed public content | Unknown |
| Database | Not publicly established | Unknown |
| Internal email/workflow tools | Not publicly established | Unknown |

### 2.2 Recommended target architecture

**Prototype:** Browser → Flask application → SQLite database → authenticated admin dashboard.

**Production direction:** Browser → HTTPS edge/CDN and web application firewall → application/API service → managed PostgreSQL database. Integrate a business email provider for enquiry notifications and a workflow automation platform for routing, assignment and service-level reminders. Keep secrets in a managed secret store and logs free of unnecessary personal data.

### 2.3 Backend and database improvements

- Use a documented API contract and server-side validation for all user-submitted fields.
- Store enquiries with a unique ID, received timestamp, contact details, enquiry category, message and lifecycle status.
- Use parameterised queries or an ORM to avoid SQL injection.
- Use PostgreSQL for a production deployment with concurrent users, migrations, managed backups and point-in-time recovery.
- Define retention, deletion, export and access policies for enquiry data.
- Add pagination, search, assignment and audit history if enquiry volume requires them.

### 2.4 Security improvements

- HTTPS everywhere; secure, HTTP-only and SameSite cookies.
- Strong individual accounts, multi-factor authentication and role-based access.
- CSRF protection on browser-authenticated state-changing actions.
- Login rate limiting, bot controls, request-size limits and abuse monitoring.
- Input validation, output encoding, parameterised SQL and security headers.
- Centralised secrets management; never commit passwords, API keys or SMTP credentials.
- Regular dependency updates, vulnerability scanning, backups and incident response procedures.
- Minimise collected personal information and publish an appropriate privacy notice and retention policy.

The prototype includes input validation, parameterised SQL, session-based admin gating, a honeypot, request-size cap and several security headers. It does not yet implement MFA, individual accounts, CSRF tokens, rate limiting, email verification or production-grade audit logging. Those are explicit production gaps, not hidden claims.

### 2.5 Internal IT, business email and automation recommendations

| Need | Suggested category / example | Reason |
|---|---|---|
| Business email and calendar | Google Workspace or Microsoft 365 | Managed business identities, mail, calendars and collaboration |
| Identity and access | Microsoft Entra ID or Google identity controls | Centralised access, MFA and offboarding |
| Device and endpoint management | Microsoft Intune or an equivalent MDM/endpoint platform | Inventory, configuration and device security |
| Workflow automation | Microsoft Power Automate, Make or n8n | Route website enquiries, notify owners and create follow-up tasks |
| Support and IT requests | Jira Service Management or Freshservice | Track incidents, requests and asset-related work |
| Source control and delivery | GitHub with protected branches and CI checks | Version history, review and repeatable releases |
| Monitoring | Managed uptime, application error and infrastructure monitoring | Detect failures and support operational response |

Selection should be based on existing licences, staff familiarity, security requirements, data residency, integration needs and total cost. These are recommendations, not claims about tools currently used by Velcoris.

### 2.6 Practical task — enquiry management

The working prototype implements:

1. **Environment & Database Configuration (`python-dotenv`):**
   - The application automatically loads `.env` using `python-dotenv`.
   - `DATABASE_PATH` points directly to the SQLite database storage (`instance/velcoris.db`).
   - `SECRET_KEY`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` are managed securely via `.env`.
2. **Form Submission:** Visitor submits the contact form (`#contact`).
3. **Data Handling:** Browser sends form data asynchronously via JavaScript to `POST /api/enquiries`.
4. **Server Validation:** Flask validates input lengths, email pattern, and allowed enquiry categories.
5. **Validation Handling:** Invalid inputs yield HTTP 400 with specific field error details.
6. **Data Persistence:** Valid enquiries are stored into SQLite via parameterised queries to prevent SQL injection.
7. **Client Feedback:** The user immediately receives an HTTP 201 JSON response with inline confirmation without full page reload.
8. **Demonstrated Query Viewing & Access:**
   - **Method A (Web Admin Dashboard):** Authenticated session at `http://127.0.0.1:5000/admin` displaying full query lists, submission timestamps, contact details, status badges, and interactive status updater (`New` → `In Progress` → `Responded` → `Closed`).
   - **Method B (CLI / Python Access):** Evaluators or administrators can run `python view_enquiries.py` or `flask --app run.py view-enquiries` to query and inspect stored database records directly from terminal.


### 2.7 Implementation roadmap

| Priority | Phase | Work | Indicative timing | Acceptance evidence |
|---|---|---|---|---|
| P0 | Discovery | Confirm current hosting, CMS/framework, form destinations, mail provider, DNS, access owners and data flows | Week 1 | Approved current-state architecture and asset inventory |
| P0 | Security baseline | Enforce HTTPS, MFA, least privilege, backups, secret rotation and dependency review | Weeks 1–2 | Security checklist and recovery test |
| P1 | Enquiry workflow | Production API, managed database, notification, assignment and status tracking | Weeks 2–4 | End-to-end enquiry test and audit trail |
| P1 | Website UX | Validate redesigned IA, mobile/accessibility and approved content with stakeholders | Weeks 2–4 | Stakeholder sign-off and responsive QA |
| P2 | Operations | Monitoring, alerting, incident/request workflows and device inventory | Weeks 4–6 | Operational dashboards and runbooks |
| P2 | Optimisation | Performance, SEO, analytics with consent, reporting and continuous improvement | Weeks 6–8 | Baseline and post-release measurements |

Timelines are planning estimates and depend on access, procurement, approvals and the state of existing systems.

## Assumptions and limitations

- This is a candidate-created prototype for evaluation, not a production replacement for the current website.
- No access to Velcoris's private source code, hosting console, DNS account, database, mail tenant or internal network was provided.
- The report does not claim to have penetration-tested the live site or measured its real-world performance.
- Public website statements are attributed to the public pages and are not independently verified technical certifications.
- The demo stores enquiry data locally in SQLite and does not send email or connect to the organisation's systems.
- Sample records should be synthetic and must not contain real customer personal information during testing.

## Public references

1. Velcoris Industries homepage — https://velcorisindustries.com/
2. Velcoris Industries technology page — https://velcorisindustries.com/technology
3. Velcoris Industries company page — https://velcorisindustries.com/company
4. Velcoris Industries contact page — https://velcorisindustries.com/contact
5. Flask documentation — https://flask.palletsprojects.com/
6. SQLite documentation — https://www.sqlite.org/docs.html
7. OWASP Cheat Sheet Series — https://cheatsheetseries.owasp.org/
8. MDN Web Docs: Responsive design — https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design

## Candidate verification statement

Before submission, the candidate should run the project locally, submit a test enquiry, confirm it is persisted, sign into the admin dashboard, update its status, test the layout at mobile and desktop widths, and replace any assumptions or proposed wording that are not personally verified. Only claim these checks as completed after performing them.
