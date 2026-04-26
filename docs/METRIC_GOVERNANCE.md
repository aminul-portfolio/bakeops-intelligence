# BakeOps Intelligence — Metric Governance

## Purpose

BakeOps Intelligence V2 adds a trusted decision-support layer on top of the working V1 platform.

This document explains how the metric layer is built, what it depends on, which gold-layer tables it creates, how the build is logged, and how a reviewer can verify that the analytics pages are based on stored metric snapshots rather than hard-coded dashboard values.

---

## Governance Principle

BakeOps separates operational records from reporting metrics.

```text
Operational bakery data
→ metric build command
→ gold-layer metric snapshots
→ analytics pages
→ BI export files