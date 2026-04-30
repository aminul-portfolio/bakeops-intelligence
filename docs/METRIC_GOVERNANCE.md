# BakeOps Intelligence — Metric Governance

## Purpose

This document explains how BakeOps Intelligence builds, stores, verifies, and protects its analytics metrics.

The goal is to show reviewers that the analytics pages are not hard-coded screenshots or presentation-only values. They are based on operational records, a repeatable metric build command, stored gold-layer snapshots, data quality checks, and exportable BI files.

---

## Governance Principle

BakeOps separates operational data from reporting metrics.

```text
operational bakery records
-> metric build command
-> gold-layer metric snapshots
-> analytics pages
-> BI export files