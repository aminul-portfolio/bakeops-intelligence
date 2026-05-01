# Milestone 3A — Contrast Notes

## Purpose

This document records the intended contrast requirements for the BakeOps analytics design-token layer.

Milestone 3A introduces shared tokens before page-level template refactoring.

---

## WCAG Targets

| Token Pair Type | Required Ratio |
|---|---:|
| Body text on background | 4.5:1 or higher |
| Large text on background | 3:1 or higher |
| UI components / graphical objects | 3:1 or higher |

---

## Token Pairs to Verify

| Usage | Foreground | Background | Target |
|---|---|---|---:|
| Primary body text | `--bo-text` | `--bo-page-bg` | 4.5:1 |
| Soft body text | `--bo-text-soft` | `--bo-page-bg` | 4.5:1 |
| Muted label text | `--bo-text-muted` | `--bo-surface` | 4.5:1 |
| Accent text/borders | `--bo-accent` | `--bo-page-bg` | 3:1 |
| Info status | `--bo-info` | `--bo-info-soft` / `--bo-page-bg` | 3:1 |
| Success status | `--bo-success` | `--bo-success-soft` / `--bo-page-bg` | 3:1 |
| Warning status | `--bo-warning` | `--bo-warning-soft` / `--bo-page-bg` | 3:1 |
| Danger status | `--bo-danger` | `--bo-danger-soft` / `--bo-page-bg` | 3:1 |
| Focus ring | `--bo-focus-ring` | dark surfaces | visible |

---

## Current Status

```text
Initial token layer created.
Measured contrast ratios should be added during the next 3A refinement pass.
```

---

## Notes

- Accessibility token work starts in 3A, not at final QA.
- Final verification should happen before the 3.5 GO/NO-GO review.
- If a token pair does not meet the required ratio, adjust the token rather than overriding individual pages.
- Keep token-level accessibility decisions documented here so future visual changes remain reviewable.
