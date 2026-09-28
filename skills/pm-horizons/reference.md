## AI Capability Horizons (full reference)

AI capabilities are improving on a roughly 4–6.5 month doubling rate for task complexity at 50% autonomous reliability. Use the reference tasks and decision framework below to calibrate plan ambition, sequencing, and deferral decisions.

**Current Frontier (February 2026):**

| Domain | Current 50% Autonomous Frontier | Doubling Rate |
|--------|--------------------------------|---------------|
| SWE (best measured) | ~14.5h tasks (Opus 4.6), ~6.5h (GPT-5.3) | 4–6.5 months |
| Writing/Content | 2–4hr tasks | Tracks SWE closely |
| Data/Analytics | 1–4hr tasks (mechanical parts track SWE, judgment slower) | ~SWE for mechanical |
| Operations/Admin | Data entry strong; GUI automation growing | ~SWE for automation |
| Design/Creative | Image gen fast; GUI automation 40–100x behind SWE | Uneven |
| Sales/Marketing | Writing+research strong; market judgment weak | Mixed |
| Strategy/Management | World-modeling, multi-stakeholder judgment | Slower than SWE |
| Robotic manipulation | 4–20 second tasks; 3–10x slower than humans | No reliable measurement |

**Key modifiers:**
- Human-in-the-loop extends capability ~5x (disappears once AI is superhuman at the subtask)
- Many "physical" tasks have large digital components (CAD, planning, simulation) that track closer to SWE rates
- "Sludge factor": messy real-world context adds +1 to +3 seniority levels to the effective difficulty

**Reference Task Set (131 tasks, human-rated horizons):**
Format: `aggressive estimate – conservative estimate` for when AI reaches 50% autonomous reliability.

*Software Engineering:*
- REST API with CRUD, auth, tests, deploy: now–now
- Production bug root-caused, fixed, deployed with regression test: now–now
- Legacy module (5K LOC) framework migration with feature parity: now–now
- CI/CD pipeline (build, test, lint, deploy, rollback): 6mo–6mo
- Performance bottleneck identified and resolved (p95 -50%): 6mo–12mo
- Existing e-commerce site scaled 100→1000 orders/day: 6mo–18mo
- Monolith decomposed into 3–5 services, zero-downtime migration: 6mo–24mo
- Platform migration (on-prem→cloud) for 50-person org: 12mo–30mo
- Engineering org (50 people) monthly→daily deploys: 12mo–24mo

*Data / ML / Analytics:*
- Exploratory analysis of messy dataset, findings for stakeholders: now–now
- SQL dashboard, 5 business questions, daily refresh + alerting: now–6mo
- Churn prediction model, no existing ML infra, API + drift monitoring: now–12mo
- A/B test end-to-end (with existing infra): 6mo–12mo
- Rec engine (no existing personalization), 10%+ engagement lift: 6mo–18mo
- Fraud detection system upgraded with ML (<0.1% FN): 6mo–30mo
- Data governance retro-fitted across ungoverned org: 18mo–>36mo
- ML platform (consolidating ad-hoc workflows): 6mo–36mo
- Supply chain optimization replacing spreadsheets, -15% inventory costs: 12mo–24mo

*Writing / Communications:*
- Technical blog post (1500 words, researched): now–now
- Internal policy document (compliance, 10+ pages): now–now
- Grant proposal ($50K–$500K, with budget): now–6mo
- Thought leadership series (6 articles, cohesive narrative): now–6mo
- 200-page technical manual with diagrams: 6mo–12mo

*Operations / Admin:*
- Employee onboarding automated (manual→triggered): 6mo–12mo
- Vendor evaluation (3+ options, scored, recommended): now–6mo
- Office relocation (50 people, full project managed): 6mo–24mo
- Procurement systematized (ad-hoc→structured): 6mo–18mo

*Design / Creative:*
- Wireframes/prototype for 5-screen mobile flow: now–6mo
- Icon set (40+ icons, consistent style): 6mo–12mo
- Existing product's ad-hoc UI formalized into design system: 6mo–24mo
- Established product (100+ screens) UX overhauled, +25% satisfaction: 12mo–>36mo

*Sales / Marketing:*
- Competitive analysis (5 competitors, positioning map): now–now
- Content marketing pipeline (4 posts/month, 3 months): now–6mo
- Lead scoring model (no existing scoring): 6mo–18mo
- GTM launch for B2B SaaS ($500–$5K), first 100 customers: 6mo–30mo

*Strategy / Management:*
- OKRs drafted for a team (quarterly, measurable): now–6mo
- Post-mortem on a failed project (root causes, recommendations): now–6mo
- Cost reduction program (never optimized, -20%): 6mo–24mo
- Strategic plan for new market entry: 6mo–30mo
- M&A due diligence (technical + financial): 12mo–>36mo

*Physical / Hardware:*
- 3D-printed prototype of mechanical part: now–6mo
- PCB designed, fabricated, assembled, tested: 6mo–18mo
- IKEA furniture assembled from box: >36mo–>36mo
- CNC production run (new material, 50+ parts): >36mo–>36mo
- Consumer electronics product manufactured at scale: 18mo–>36mo

*Customer Support / Success:*
- Support triage system (shared inbox→helpdesk): 6mo–12mo
- Customer health scoring (no existing metrics): 6mo–24mo
- Self-service knowledge base (50+ articles, analytics): 6mo–12mo

*Finance / Accounting:*
- Monthly close systematized (startup chaos→structured): 6mo–18mo
- Annual budget + quarterly reforecast (first formal budgeting): 6mo–18mo
- Series A fundraise orchestrated: 12mo–>36mo

*Legal / Privacy / Security:*
- Standard contracts reviewed and summarized: now–6mo
- Privacy program built from scratch: 6mo–24mo
- Security audit scoped and executed: 6mo–24mo

**Horizon-Aware Planning Decision Framework:**
For each step in the plan, apply this 4-question filter:

1. **Where is this task relative to the autonomous horizon?**
   - Well within (task << current horizon): **Automate now** — use AI for this step
   - Near the boundary (task ≈ current horizon): **Automate with human review**
   - Beyond the boundary (task >> current horizon): **Human-led, AI-accelerated**

2. **When will the autonomous horizon reach this task?**
   - If the aggressive estimate is < 6 months away: **strongly consider deferring** (document the spec, revisit later)
   - If the conservative estimate is < 12 months: **invest minimally now**, plan to revisit with better tools

3. **Is this task building a durable asset or doing automatable work?**
   - Durable assets: relationships, proprietary data, domain expertise, regulatory approvals, validated customer demand, capital
   - Automatable work: infrastructure migration, boilerplate code, data entry, format conversion, documentation, standard analytics
   - **Invest in assets; defer automatable work when the horizon is close**

4. **What's the cost of waiting?**
   - Some tasks can't be deferred (regulatory deadlines, customer-facing, blocking other work)
   - Factor in the cost of *not* doing it vs the savings from AI doing it later
   - "Is this also the work of making it automatable?" — if yes, it's a dual-purpose investment worth doing now

**How to apply in the plan:**
- For each major step, briefly note whether it's "automate now," "invest minimally," "defer," or "do now (durable asset)"
- When a step involves automatable work with a near horizon, suggest documenting the spec now and scheduling a revisit
- When a step could aim higher because capabilities are rapidly improving, say so — "by the time you reach this step in month 6, AI will likely handle X, so plan for the more ambitious version"
- Sequence durable-asset work (relationships, data collection, regulatory) early; push automatable work later
- Be specific about WHICH reference tasks are analogous to each plan step

**Look for AI-aware vertical integration — route around hard steps.**
When a plan step has a high horizon (AI can't do it well), ask: is there an alternative path that uses AI-strong capabilities to make this step unnecessary? The pattern: identify steps that are hard for AI (relationship-building, physical presence, political navigation, taste/judgment) and look for restructured workflows where AI-cheap capabilities (content generation, data analysis, automation, monitoring) substitute for the hard step entirely.

Examples:
- Instead of hiring a sales team for outbound (high horizon): build an inbound content engine + automated lead scoring + self-serve onboarding
- Instead of manual QA across a large test surface: invest in automated test generation + continuous monitoring
- Instead of extensive user research via interviews (high horizon): combine analytics-driven behavior analysis + AI-generated survey instruments + rapid prototype testing

AI doesn't just accelerate existing plans — it changes the *shape* of the optimal plan. Look for substitutions where the traditional step has a high horizon and the AI-native alternative has a low one.

**Expand what's feasible for the team size and budget.**
Because AI is cheap at many tasks, capabilities that previously required dedicated headcount are now available to small teams. Look for places where adding an AI-powered capability is now worth including even though it would have been out of scope before:
- Real-time analytics dashboards, automated email sequences, customer health scoring — previously required a data/ops team
- Parallel experiments (A/B tests, competitive analysis, market research) — previously too expensive to staff
- Monitoring, alerting, and triage workflows from day 1 — previously "we'll add observability later"
- Documentation, onboarding materials, knowledge bases generated alongside the work — previously a separate project

