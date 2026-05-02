# BakeOps Intelligence — Milestone 4 SaaS Layout Plan

## Document Purpose

This document defines the full Milestone 4 plan for **BakeOps Intelligence**, a Django-based bakery operations intelligence platform.

Milestone 4 focuses on turning the existing trusted analytics evidence into a unified, premium SaaS-style product experience. The goal is not to rebuild the platform or add unsupported SaaS capabilities. The goal is to make the existing seeded/demo data, metric outputs, BI exports, trust surfaces, and analytics pages feel like one polished, commercial-grade analytics product.

---

## Current Project Context

```text
Project: BakeOps Intelligence
Framework: Django
Purpose: Bakery operations intelligence and analytics demo
Career target: Data Analyst / Data Engineer / Analytics Engineer roles
Current milestone: Milestone 4 — Premium SaaS Layout and Visual Analytics Upgrade
```

### Version ladder

```text
V1 = Works
V2 = Trusted
V3 = Commercial foundation
Milestone 3 = Final UI/trust polish and reviewer-ready QA
Milestone 4 = Premium SaaS layout and visual analytics upgrade
```

### Current evidence already protected

```text
37 tests passed
BI exports generate 11 files
Total exported rows: 52
Case study is shipped and linked
README is refreshed
Final Milestone 3 screenshots are captured
Main branch was clean before Milestone 4
```

---

## Milestone 4 Premium Benchmark Goal

The latest BakeOps Intelligence version should set a new benchmark for portfolio-quality SaaS-style analytics projects by delivering a unified, premium, reviewer-ready product experience.

The objective is not to add fake SaaS capabilities or rebuild the platform. The objective is to make the existing trusted evidence, seeded data, BI exports, metric outputs, and analytics pages feel like one polished commercial-grade product.

By the end of Milestone 4, the platform should require no obvious visual, layout, navigation, or reviewer-experience refinement before career packaging and job-market preparation.

---

## Final Quality Definition

BakeOps Intelligence should be considered Milestone 4 complete only when:

```markdown
- [ ] All 8 analytics pages feel like one connected SaaS product
- [ ] The same sidebar, topbar, spacing, card system, typography, and colour logic are used everywhere
- [ ] The dashboard works as a true command centre
- [ ] Each deep-dive page has a clear visual analytics layer
- [ ] Evidence tables remain visible and reviewer-friendly
- [ ] The protected proof remains intact: `Birthday Classic 1 4 review`
- [ ] The platform looks premium without making unsupported SaaS claims
- [ ] No page feels unfinished, inconsistent, or visually weaker than the others
- [ ] Final screenshots are strong enough for GitHub, LinkedIn, portfolio, and recruiter review
```

---

## Protected Proof / Signature Insight

Birthday Classic is the highest-revenue product in the seeded demo data, ranking #1 by revenue. However, after waste-adjusted margin is considered, it falls to rank #4 and receives a `Review` action flag.

This proves that BakeOps Intelligence does more than report sales — it helps reveal when a best-selling product may require operational review because of waste and margin pressure.

### Protected proof statement

```text
Birthday Classic → Revenue rank #1 → Waste-adjusted margin rank #4 → Review
```

### Protected terminal check

```powershell
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
```

Expected output:

```text
Birthday Classic 1 4 review
```

### Protected proof rules

```markdown
- [ ] Do not change the metric logic behind this proof
- [ ] Do not change seeded data in a way that breaks this proof
- [ ] Do not hide this proof from the Product Profitability page
- [ ] Re-check this proof after every major Milestone 4 phase
- [ ] Keep the proof evidence-based and tied to seeded/demo data
```

---

## Critical Boundaries

Milestone 4 must remain honest and evidence-based.

Do not suggest, implement, or claim:

```markdown
- [ ] Live POS integration
- [ ] Real customer data
- [ ] Billing
- [ ] Subscriptions
- [ ] Production SaaS deployment
- [ ] Automated BI sync
- [ ] Shopify integration
- [ ] Square integration
- [ ] Real customer usage
- [ ] Fake live monitoring
- [ ] Fake background jobs
- [ ] Fake loading states that imply automation
```

### Technical boundaries

```markdown
- [ ] Do not change metric logic unless clearly approved
- [ ] Do not casually change models
- [ ] Do not create migrations unless absolutely necessary
- [ ] Do not change the protected proof
- [ ] Do not remove evidence tables
- [ ] Do not replace evidence with unsupported visuals
```

---

## Current Analytics Pages

```markdown
1. Dashboard — `/analytics/`
2. Product Profitability — `/analytics/products/`
3. Ingredient Risk — `/analytics/ingredients/`
4. Waste Analysis — `/analytics/waste/`
5. Occasion Analytics — `/analytics/occasions/`
6. Customer Analytics — `/analytics/customers/`
7. Data Quality Review — `/analytics/data-quality/`
8. Export Centre — `/analytics/exports/`
```

---

## Page-by-Page Target Ratings

| Page | Current Level Before Milestone 4 | Target Level | Main Upgrade |
|---|---:|---:|---|
| Dashboard | 8.8/10 | 9.4/10 | Command-centre polish and cross-page previews |
| Product Profitability | 9.0/10 | 9.5/10 | Visual proof for rank inversion and protected insight |
| Ingredient Risk | 8.1/10 | 9.2/10 | Stock vs reorder visual layer and stronger risk hierarchy |
| Waste Analysis | 8.2/10 | 9.2/10 | Waste by reason/product visual story |
| Occasion Analytics | 8.0/10 | 9.0/10 | Demand comparison and delivery pressure visuals |
| Customer Analytics | 8.0/10 | 9.0/10 | Customer value/concentration and repeat behaviour visuals |
| Data Quality Review | 8.7/10 | 9.3/10 | Enterprise trust-surface summary and density polish |
| Export Centre | 8.7/10 | 9.3/10 | BI export contract grouping and workflow clarity |

---

## Shared Page Anatomy

Every analytics page should follow a consistent structure:

```markdown
- [ ] Shared SaaS app shell
- [ ] Left sidebar navigation
- [ ] Top utility bar
- [ ] Page title / subtitle
- [ ] Evidence or demo-data context
- [ ] KPI strip
- [ ] Signature insight or key proof area
- [ ] Main visual analytics block
- [ ] Evidence table or reviewer detail section
- [ ] Action / definition / explanation cards where relevant
- [ ] Footer or trust note where useful
```

### Shared anatomy rules

```markdown
- [ ] Use the same section spacing across all pages
- [ ] Use consistent card padding and border radius
- [ ] Use consistent section headings
- [ ] Use consistent evidence badges
- [ ] Use consistent action button treatment
- [ ] Use consistent chart-card layout
- [ ] Use consistent table-card layout
```

---

## Design System / Visual Consistency Rules

### Shared product shell

```markdown
- [ ] Persistent left sidebar
- [ ] Shared topbar
- [ ] Active page state
- [ ] Workspace context
- [ ] Demo/evidence badge
- [ ] Export Centre link/action
- [ ] Reviewer/demo mode indicator
```

### Shared card system

```markdown
- [ ] KPI cards
- [ ] Chart cards
- [ ] Insight cards
- [ ] Action cards
- [ ] Table cards
- [ ] Definition/glossary cards
- [ ] Evidence cards
- [ ] Workflow cards
```

### Typography

```markdown
- [ ] Page title style
- [ ] Section title style
- [ ] KPI value style
- [ ] Helper text style
- [ ] Badge text style
- [ ] Table header style
- [ ] Numeric value style with tabular numerals where useful
```

### Colour logic

Use colour by meaning, not decoration:

```markdown
- [ ] Green = positive / promote / stable success
- [ ] Amber/orange = review / warning / attention
- [ ] Red = critical / high-risk / reduce
- [ ] Blue/purple = analysis / neutral intelligence / data layer
- [ ] Muted grey = secondary evidence / inactive / supporting detail
```

---

## Suggested App-Shell Structure

```text
bakeops/templates/bakeops/
├── base_analytics.html
├── partials/
│   ├── _analytics_sidebar.html
│   └── _analytics_topbar.html
├── analytics_dashboard.html
├── product_profitability.html
├── ingredient_risk.html
├── waste_analysis.html
├── occasion_analytics.html
├── customer_analytics.html
├── data_quality_review.html
└── export_centre.html
```

Recommended CSS:

```text
bakeops/static/bakeops/css/analytics-shell.css
```

---

## Exact Reusable Components Needed

```markdown
- [x] Shared analytics base template
- [x] Shared analytics sidebar
- [x] Shared analytics topbar
- [x] Shared shell CSS
- [ ] Shared KPI card pattern
- [ ] Shared chart-card pattern
- [ ] Shared insight-card pattern
- [ ] Shared action-card pattern
- [ ] Shared table-card pattern
- [ ] Shared badge/pill pattern
- [ ] Shared empty-state pattern
- [ ] Shared warning/trust note pattern
- [ ] Shared section-header pattern
- [ ] Shared workflow-strip pattern
```

---

## Milestone 4 Status Tracker

```markdown
- [x] 4.0 — Product UI Audit and Final Scope Lock
- [x] 4A — Unified SaaS App Shell
- [x] 4B — Product Profitability Visual Proof
- [ ] 4C — Waste Analysis Visual Layer
- [ ] 4D — Ingredient Risk Visual Layer
- [ ] 4E — Dashboard Final Command-Centre Polish
- [ ] 4F — Occasion and Customer Analytics Visual Upgrade
- [ ] 4G — Trust Surfaces Enterprise Polish
- [ ] 4H — Empty, Error, and Stale States
- [ ] 4I — Responsive and Density Hardening
- [ ] 4J — Final QA, Screenshots, Documentation, and Merge
```

---

# 4.0 — Product UI Audit and Final Scope Lock

Status: Complete

```markdown
- [x] Confirm current screenshots for all 8 pages
- [x] Rate each page: current level / target level
- [x] Identify which pages need visual analytics
- [x] Identify which pages only need layout/density polish
- [x] Confirm shared app-shell strategy
- [x] Define reusable components
- [x] Define what will not be changed
- [x] Create/update `docs/MILESTONE_4_SAAS_LAYOUT_PLAN.md`
```

---

# 4A — Unified SaaS App Shell

Status: Complete

Commit:

```text
ce36201 Milestone 4A: add unified SaaS analytics shell
```

## Objective

Create one shared premium SaaS analytics shell across all 8 analytics pages.

## Completed checklist

```markdown
- [x] Create shared analytics base template
- [x] Add persistent left sidebar navigation
- [x] Add active page state
- [x] Add shared topbar
- [x] Add workspace/demo evidence context
- [x] Add Export Centre link/action
- [x] Add consistent app-shell layout wrapper
- [x] Add shared shell CSS
- [x] Update all 8 analytics pages to extend the shared shell
- [x] Preserve existing page content
- [x] Avoid model changes
- [x] Avoid migration changes
- [x] Avoid metric logic changes
- [x] Confirm protected proof remains intact
```

## Files created

```text
bakeops/templates/bakeops/base_analytics.html
bakeops/templates/bakeops/partials/_analytics_sidebar.html
bakeops/templates/bakeops/partials/_analytics_topbar.html
bakeops/static/bakeops/css/analytics-shell.css
```

## Files updated

```text
bakeops/templates/bakeops/analytics_dashboard.html
bakeops/templates/bakeops/product_profitability.html
bakeops/templates/bakeops/ingredient_risk.html
bakeops/templates/bakeops/waste_analysis.html
bakeops/templates/bakeops/occasion_analytics.html
bakeops/templates/bakeops/customer_analytics.html
bakeops/templates/bakeops/data_quality_review.html
bakeops/templates/bakeops/export_centre.html
```

## 4A Safety Gate Result

```markdown
- [x] `python manage.py check` passed
- [x] `python manage.py makemigrations --check --dry-run` returned `No changes detected`
- [x] 37 tests passed
- [x] Seed demo data passed
- [x] Metric build passed
- [x] BI export generated 11 files / 52 rows
- [x] Protected proof returned `Birthday Classic 1 4 review`
```

---

# 4B — Product Profitability Visual Proof

Status: Complete

Commit:

```text
be41cee Milestone 4B: add product profitability visual proof
```

## Objective

Make the Product Profitability page visually prove the protected insight:

```text
Birthday Classic → Revenue rank #1 → Waste-adjusted margin rank #4 → Review
```

## Completed checklist

```markdown
- [x] Add visual proof section
- [x] Add revenue-rank vs waste-adjusted-margin-rank comparison
- [x] Highlight Birthday Classic dynamically
- [x] Show rank movement clearly
- [x] Keep protected proof visible
- [x] Keep existing signature insight section
- [x] Keep evidence table as the supporting layer
- [x] Keep action flag definitions
- [x] Avoid metric logic changes
- [x] Avoid model changes
- [x] Avoid migration changes
- [x] Confirm protected proof remains intact
```

## 4B Safety Gate Result

```markdown
- [x] `python manage.py check` passed
- [x] `python manage.py makemigrations --check --dry-run` returned `No changes detected`
- [x] 37 tests passed
- [x] Seed demo data passed
- [x] Metric build passed
- [x] BI export generated 11 files / 52 rows
- [x] Protected proof returned `Birthday Classic 1 4 review`
```

---

# 4C — Waste Analysis Visual Layer

Status: Not started

## Objective

Make the Waste Analysis page tell a stronger visual story about where waste cost comes from and how it affects margin.

## Checklist

```markdown
- [ ] Create branch for 4C
- [ ] Add waste-cost breakdown visual
- [ ] Add waste-by-reason visual
- [ ] Add waste-by-product visual where supported
- [ ] Make Birthday Classic waste impact easier to see
- [ ] Keep waste event table as supporting evidence
- [ ] Keep product waste impact table visible
- [ ] Keep ingredient-linked waste evidence visible
- [ ] Avoid unsupported forecasting/prediction claims
- [ ] Avoid metric logic changes
- [ ] Avoid model changes
- [ ] Avoid migrations
```

## Expected visual outcome

The page should clearly answer:

```markdown
- [ ] What is the total waste cost?
- [ ] Which reason causes the most waste?
- [ ] Which product is most affected by waste?
- [ ] How does waste reduce margin?
- [ ] Which waste events support the conclusion?
```

---

# 4D — Ingredient Risk Visual Layer

Status: Not started

## Objective

Make Ingredient Risk easier to understand visually by showing stock position, reorder pressure, and high-risk ingredients.

## Checklist

```markdown
- [ ] Create branch for 4D
- [ ] Add stock vs reorder-level visual
- [ ] Highlight low-stock ingredients
- [ ] Highlight near-expiry / expiry risk where supported
- [ ] Add top ingredient risk card
- [ ] Improve risk/action hierarchy
- [ ] Tighten table density
- [ ] Keep recommendations evidence-based
- [ ] Keep deep-dive evidence table visible
- [ ] Avoid metric logic changes
- [ ] Avoid model changes
- [ ] Avoid migrations
```

## Expected visual outcome

The page should clearly answer:

```markdown
- [ ] Which ingredients are below reorder level?
- [ ] Which ingredients are highest risk?
- [ ] What is the gap between current stock and reorder level?
- [ ] What action should be reviewed first?
```

---

# 4E — Dashboard Final Command-Centre Polish

Status: Not started

## Objective

Turn the dashboard into the command centre of the product.

## Checklist

```markdown
- [ ] Create branch for 4E
- [ ] Align dashboard with the unified shell
- [ ] Keep signature insight visible above the fold
- [ ] Add clearer what-needs-attention area
- [ ] Surface Product Profitability visual proof
- [ ] Surface Waste Analysis preview
- [ ] Surface Ingredient Risk preview
- [ ] Surface Occasion Analytics preview
- [ ] Surface Customer Analytics preview
- [ ] Surface Data Quality trust status
- [ ] Surface Export Centre readiness
- [ ] Link clearly into all deep-dive pages
- [ ] Avoid fake live status
- [ ] Avoid fake automation
- [ ] Avoid unsupported monitoring claims
```

## Expected visual outcome

The dashboard should act as the main product hub:

```markdown
- [ ] Executive KPI overview
- [ ] Signature insight
- [ ] Recommended actions
- [ ] Deep-dive page previews
- [ ] Trust/export readiness signals
```

---

# 4F — Occasion and Customer Analytics Visual Upgrade

Status: Not started

## Objective

Upgrade Occasion Analytics and Customer Analytics with clear visual analytics while keeping evidence tables intact.

## Occasion Analytics checklist

```markdown
- [ ] Add occasion demand comparison visual
- [ ] Show revenue by occasion
- [ ] Show order count / upcoming demand clearly
- [ ] Improve delivery-pressure hierarchy
- [ ] Add top occasion insight card
- [ ] Keep demand deep-dive table visible
- [ ] Avoid unsupported forecasting claims
```

## Customer Analytics checklist

```markdown
- [ ] Add customer value/concentration visual
- [ ] Show repeat vs one-time behaviour
- [ ] Improve top-customer value section
- [ ] Add customer revenue concentration card
- [ ] Keep loyalty deep-dive table visible
- [ ] Avoid CRM or real-customer overclaims
```

---

# 4G — Trust Surfaces Enterprise Polish

Status: Not started

## Objective

Make Data Quality Review and Export Centre feel like enterprise-grade trust surfaces.

## Data Quality Review checklist

```markdown
- [ ] Add issue severity/status summary visual if supported
- [ ] Improve issue-register density
- [ ] Make highest-priority issue stand out
- [ ] Keep trust-impact and review-action columns readable
- [ ] Keep issue evidence visible
- [ ] Avoid hiding quality problems
```

## Export Centre checklist

```markdown
- [ ] Improve 11-file export contract presentation
- [ ] Make fact/dimension/gold groups visually distinct
- [ ] Keep command workflow visible
- [ ] Keep file contract cards readable
- [ ] Keep output evidence visible
- [ ] Avoid live BI sync claims
```

---

# 4H — Empty, Error, and Stale States

Status: Not started

## Objective

Improve user/reviewer confidence when data is missing, sparse, or not yet generated.

## Checklist

```markdown
- [ ] Improve missing-data messages
- [ ] Add clear command guidance where metric data is missing
- [ ] Add export-missing guidance where export data is unavailable
- [ ] Add stale snapshot warning only if supported by existing data
- [ ] Avoid fake loading states
- [ ] Avoid fake background jobs
- [ ] Avoid unsupported automation claims
- [ ] Keep messages plain-English and reviewer-friendly
```

---

# 4I — Responsive and Density Hardening

Status: Not started

## Objective

Ensure the platform remains usable and credible across desktop, laptop, tablet, and mobile widths.

## Checklist

```markdown
- [ ] Test at 1440px desktop
- [ ] Test at 1280px laptop
- [ ] Test at 768px tablet
- [ ] Test at 390px mobile
- [ ] Ensure sidebar collapses/stacks cleanly
- [ ] Ensure topbar wraps cleanly
- [ ] Ensure KPI cards stack properly
- [ ] Ensure tables scroll horizontally
- [ ] Use tabular numerals for metric-heavy UI
- [ ] Tighten spacing without making pages cramped
- [ ] Confirm no page has broken overflow
```

---

# 4J — Final QA, Screenshots, Documentation, and Merge

Status: Not started

## Objective

Complete Milestone 4 with verified screenshots, documentation, and clean Git history.

## Checklist

```markdown
- [ ] Capture final screenshots of all 8 analytics pages
- [ ] Confirm all screenshots show the unified product shell
- [ ] Confirm Product Profitability includes protected proof
- [ ] Confirm Waste Analysis visual story is clear
- [ ] Confirm Ingredient Risk visual story is clear
- [ ] Confirm Occasion and Customer pages have visual upgrades
- [ ] Confirm Data Quality and Export Centre remain honest trust surfaces
- [ ] Update README if visual/product scope changed
- [ ] Keep `docs/CASE_STUDY.md` as analytical source of truth
- [ ] Update reviewer walkthrough if workflow/routes changed
- [ ] Run full safety gate
- [ ] Confirm GitHub Actions green
- [ ] Merge to `main`
```

---

## Full Safety Gate

Run after every major gate:

```powershell
git status
python -m ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
git diff --stat
```

Expected:

```text
No changes detected
37 tests passed
Files generated: 11
Total rows exported: 52
Birthday Classic 1 4 review
```

---

## Cross-Page Consistency QA

```markdown
- [ ] Same left sidebar appears on all 8 pages
- [ ] Same topbar appears on all 8 pages
- [ ] Correct active navigation state appears on each page
- [ ] Page titles and subtitles follow one pattern
- [ ] KPI strip styling is consistent across all 8 pages
- [ ] Section spacing is consistent across all 8 pages
- [ ] Table styling is consistent across all 8 pages
- [ ] Chart styling is consistent across all visual pages
- [ ] “View more / view full analysis” links use one pattern
- [ ] Action buttons use one pattern
- [ ] Colours map consistently to meaning across pages
- [ ] The whole platform feels like one product, not 8 separate screens
```

---

## Premium Benchmark QA

```markdown
- [ ] Does the project look like one complete SaaS product rather than separate Django pages?
- [ ] Does the first dashboard screen create a strong commercial/product impression?
- [ ] Can a recruiter immediately understand the platform’s purpose?
- [ ] Can a data/analytics reviewer see the evidence path from seeded records to metrics to exports?
- [ ] Are all 8 pages visually consistent?
- [ ] Are the weakest pages upgraded to match the strongest pages?
- [ ] Are charts and tables balanced properly?
- [ ] Are action cards and insight cards clear without exaggeration?
- [ ] Are all claims evidence-based?
- [ ] Would these screenshots improve GitHub, LinkedIn, portfolio, and recruiter credibility?
```

---

## Anti-Scope-Creep Rules

```markdown
- [ ] Do not add fake SaaS features
- [ ] Do not claim live POS integration
- [ ] Do not claim real customer data
- [ ] Do not add billing or subscriptions
- [ ] Do not claim production SaaS deployment
- [ ] Do not add fake automated BI sync
- [ ] Do not change metric logic casually
- [ ] Do not create migrations unless absolutely necessary
- [ ] Do not hide evidence tables
- [ ] Do not break the Birthday Classic proof
- [ ] Do not copy mockup numbers literally if they are not supported by seeded/demo data
- [ ] Use visual references as layout direction only, not as data sources
```

---

## One-Phase-at-a-Time Workflow

Milestone 4 must continue one phase at a time:

```text
Build → Safety Gate → Screenshots → Review → Celebrate → Confirm → Next Phase
```

Rules:

```markdown
- [ ] Do not start the next phase until the current phase is verified
- [ ] Do not combine multiple phases in one commit unless explicitly approved
- [ ] Celebrate each completed milestone before moving forward
- [ ] Keep each branch focused and reviewable
```

---

## Final Scope Note

Milestone 4 is the final major presentation and product-experience upgrade for BakeOps Intelligence.

The finished version should visually communicate the quality of a serious SaaS analytics product while staying fully honest about its evidence base: seeded demo data, trusted metric outputs, BI export files, and reviewer-visible operational analytics.

The project should not need another UI polish milestone after this. Any future work should be optional career packaging, deployment preparation, or product expansion — not repair of visual inconsistency, weak layout, unclear evidence, or unfinished reviewer experience.