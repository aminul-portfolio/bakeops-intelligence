# Milestone 3.0 — Pattern Inventory & UI Audit

## Purpose

This document records the current UI/template/CSS state before starting Milestone 3A.

The goal is to formalise existing strong patterns, not redesign from scratch.

---

## 1. Branch Context

Branch:

```text
milestone-3-pattern-inventory-clean
```

Base commit:

```text
c608d71 Align README with trusted-stage reviewer evidence
```

Working state before inventory document:

```text
nothing to commit, working tree clean
```

---

## 2. Template Inventory

The project does not use a root-level `templates/` folder.

Templates are app-level.

### BakeOps analytics templates

| File | Size |
|---|---:|
| `bakeops/templates/bakeops/analytics_dashboard.html` | 45,286 |
| `bakeops/templates/bakeops/customer_analytics.html` | 19,312 |
| `bakeops/templates/bakeops/data_quality_review.html` | 20,526 |
| `bakeops/templates/bakeops/export_centre.html` | 15,819 |
| `bakeops/templates/bakeops/ingredient_risk.html` | 22,480 |
| `bakeops/templates/bakeops/occasion_analytics.html` | 20,106 |
| `bakeops/templates/bakeops/product_profitability.html` | 22,341 |
| `bakeops/templates/bakeops/waste_analysis.html` | 26,477 |

### Cakes catalogue templates

| File |
|---|
| `cakes/templates/cakes/about.html` |
| `cakes/templates/cakes/base.html` |
| `cakes/templates/cakes/cakes.html` |
| `cakes/templates/cakes/cake_detail.html` |
| `cakes/templates/cakes/contact.html` |
| `cakes/templates/cakes/home.html` |
| `cakes/templates/cakes/offers.html` |
| `cakes/templates/cakes/promotion.html` |
| `cakes/templates/cakes/welcome.html` |
| `cakes/templates/cakes/_cake_card.html` |

---

## 3. CSS Inventory

The project does not use a root-level `static/` folder.

CSS files found:

| File | Size |
|---|---:|
| `cakes/static/css/cake.css` | 0 |
| `cakes/static/css/home.css` | 0 |
| `cakes/static/css/style.css` | 30,401 |

Observation:

BakeOps analytics pages likely rely heavily on embedded page-level CSS inside templates. Milestone 3A should introduce or formalise shared BakeOps CSS files such as:

- `tokens.css`
- `app-shell.css`
- `components.css`

Exact paths should be decided after inspecting current template asset loading.

---

## 4. Inline Style Count

| File | Inline Styles |
|---|---:|
| `bakeops/templates/bakeops/analytics_dashboard.html` | 12 |
| `bakeops/templates/bakeops/waste_analysis.html` | 5 |
| `bakeops/templates/bakeops/occasion_analytics.html` | 4 |
| `bakeops/templates/bakeops/product_profitability.html` | 4 |
| `bakeops/templates/bakeops/customer_analytics.html` | 4 |
| `bakeops/templates/bakeops/data_quality_review.html` | 3 |
| `bakeops/templates/bakeops/ingredient_risk.html` | 3 |
| `bakeops/templates/bakeops/export_centre.html` | 1 |
| `cakes/templates/cakes/cakes.html` | 2 |
| `cakes/templates/cakes/offers.html` | 2 |
| `cakes/templates/cakes/promotion.html` | 2 |
| `cakes/templates/cakes/about.html` | 1 |
| `cakes/templates/cakes/_cake_card.html` | 0 |
| `cakes/templates/cakes/welcome.html` | 0 |
| `cakes/templates/cakes/cake_detail.html` | 0 |
| `cakes/templates/cakes/base.html` | 0 |
| `cakes/templates/cakes/home.html` | 0 |
| `cakes/templates/cakes/contact.html` | 0 |

Observation:

Most inline styles are spacing, muted text, or table-width helpers. These are good candidates for shared utility/component classes during 3A/3C.

---

## 5. Top Inline Style Patterns

| Inline Style | Count |
|---|---:|
| `style="margin: 0;"` | 7 |
| `style="margin-top: 18px;"` | 6 |
| `style="margin-top: 8px;"` | 4 |
| `style="margin: 10px 0 0;"` | 4 |
| `style="margin-top: 0;"` | 4 |
| `style="color: var(--muted);"` | 3 |
| `style="min-width: 620px;"` | 3 |
| `style="margin-top: 14px;"` | 2 |
| `style="max-width: 640px; margin: 0 auto;"` | 2 |
| `style="height: 170px; object-fit: cover;"` | 1 |
| `style="height: 170px;"` | 1 |
| `style="border-radius: 1rem;"` | 1 |
| `style="color: var(--muted); font-size: 0.84rem;"` | 1 |
| `style="min-width: 600px;"` | 1 |
| `style="max-width: 640px;"` | 1 |
| `style="margin: 8px 0 0;"` | 1 |

Recommended future replacements:

- spacing utility classes
- muted text class
- responsive table wrapper class
- reusable centred container class
- reusable image/object-fit helper for catalogue pages only if the older `cakes` app is later included

---

## 6. CSS Colour Inventory

The CSS scan found more than 20 distinct colours.

| Colour | Count |
|---|---:|
| `#ffffff` | 17 |
| `#111827` | 11 |
| `#f97316` | 9 |
| `#f9fafb` | 6 |
| `#6b7280` | 6 |
| `#4b5563` | 6 |
| `#ec4899` | 5 |
| `#e5e7eb` | 5 |
| `#fff` | 4 |
| `#fee2e2` | 3 |
| `#fdf2ff` | 3 |
| `#8b5cf6` | 3 |
| `#fefce8` | 2 |
| `#0f172a` | 2 |
| `#9ca3af` | 2 |
| `#facc15` | 2 |
| `#fff7ed` | 2 |
| `#374151` | 2 |
| `#fef2f2` | 2 |
| `#b45309` | 2 |
| `#38bdf8` | 2 |
| `#6b21a8` | 2 |
| `#22c55e` | 1 |
| `#a855f7` | 1 |
| `#dde1e7` | 1 |
| `#7e22ce` | 1 |
| `#fef3c7` | 1 |
| `#fee2ff` | 1 |
| `#4f46e5` | 1 |
| `#b61d88` | 1 |
| `#fdf2f8` | 1 |
| `#ffa75e` | 1 |
| `#ff7f9c` | 1 |
| `#fffdf7` | 1 |
| `#222222` | 1 |
| `#7e0f13` | 1 |
| `#f9a8d4` | 1 |
| `#bfdbfe` | 1 |
| `#000` | 1 |
| `#88d2ff` | 1 |
| `#d1d5db` | 1 |
| `#fde68a` | 1 |

Observation:

This triggers a caution point, but most colours appear to come from the old `cakes/static/css/style.css`.

Milestone 3A should not try to clean the entire old catalogue CSS immediately.

Recommendation:

- create a controlled BakeOps analytics token system
- avoid global colour changes to the old `cakes` catalogue layer unless needed
- document BakeOps token pairs in `docs/3a/CONTRAST.md`

---

## 7. Hardcoded Business-Copy Risks

Hardcoded business-copy scan found several matches.

### Important BakeOps items

- `analytics_dashboard.html` includes hardcoded Birthday Classic signature-insight wording:
  - `Birthday Classic ranks #1 by revenue but falls after waste-adjusted margin analysis.`
- `waste_analysis.html` includes product-specific profitability/waste explanation copy:
  - the scan captured a sentence fragment: `but waste pressure reduces its true profitability.`
- Several templates include action labels such as:
  - `review`
  - `promote`
  - `stable`
  - `reduce`

### Likely safe static copy

- documentation references to reviewer workflow
- route labels such as `Data quality`
- CSS class names such as `.pill.review`, `.pill.promote`, `.pill.stable`, `.pill.reduce`
- explanatory page text that does not depend on a specific product
- general action-label descriptions if they explain the system rather than one specific record

### Likely dynamic copy risk

- specific product names in analytical insight sentences
- product-specific revenue/margin/waste statements
- hardcoded rank or action explanations that could become wrong if seeded data changes
- hardcoded product examples in templates where an equivalent view-context object exists

### Older `cakes` catalogue layer

The `cakes` app also contains hardcoded `Birthday Classic` and review/promote/stable labels. This appears to belong to the older catalogue/demo layer and should be considered out of Milestone 3 scope unless a future milestone explicitly modernises the full site.

Recommendation:

Run a focused Pre-3.0 Content Correctness Sweep before 3A.

---

## 8. Repeated UI Patterns Observed

To inspect manually before 3A:

- page shell
- top navigation / nav pills
- page hero
- proof point panel
- KPI cards
- insight panels
- tables
- badges / pills
- action buttons
- evidence / code blocks

Known repeated classes from scan:

- `pill.review`
- `pill.promote`
- `pill.stable`
- `pill.reduce`
- `nav-pill`
- `button-link`
- `kpi-label`
- `kpi-value`
- `kpi-foot`
- `eyebrow`
- `code`

These are likely candidates for formalisation in 3A.

---

## 9. Safest Files for 3A

Likely safe to inspect/edit after Pre-3.0:

- `bakeops/templates/bakeops/*.html`
- shared style blocks inside `bakeops/templates/bakeops/*.html`
- future shared CSS files for BakeOps analytics, such as:
  - `tokens.css`
  - `app-shell.css`
  - `components.css`

Exact file paths should be confirmed before editing because current CSS appears to live under the `cakes` app only.

Recommended 3A direction:

- create a BakeOps-specific static CSS layer rather than modifying old `cakes/static/css/style.css` globally
- extract common classes from embedded template styles into shared CSS
- avoid changing view context unless required by the Pre-3.0 content correctness sweep

---

## 10. Files Not to Touch in 3A

Do not touch unless explicitly approved:

- `bakeops/models/`
- `bakeops/services/`
- `bakeops/management/commands/`
- migrations
- metric calculation logic
- export generation logic
- seed data logic
- CI workflow

---

## 11. Stop Conditions Triggered

### Triggered

- More than 20 distinct CSS colours found.

### Context

This is likely from old `cakes/static/css/style.css`, not necessarily the BakeOps analytics pages.

### Not triggered yet

- No evidence yet of 3+ competing topbar systems.
- No evidence yet that core page layouts are impossible to unify.
- Hardcoded business-copy risk exists but appears manageable.

---

## 12. 3A Recommendation

Decision:

```text
HOLD
```

Reason:

Before 3A, complete a focused Pre-3.0 Content Correctness Sweep for product-specific analytical copy, especially around Birthday Classic and the waste-analysis explanation.

After that, 3A can begin with shared BakeOps tokens, shell, cards, badges, buttons, evidence blocks, and table baselines.

---

## 13. Next Step

Recommended next gate:

```text
Pre-3.0 — Content Correctness Sweep
```

Goal:

```text
Fix or document hardcoded product-specific analytical copy before design-system work begins.
```

Expected scope:

- inspect `analytics_dashboard.html`
- inspect `waste_analysis.html`
- inspect `product_profitability.html`
- avoid touching models, services, commands, migrations, and metric logic
