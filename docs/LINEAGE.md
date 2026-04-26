# BakeOps Intelligence - Data Lineage

## Purpose

This document explains how data moves through BakeOps Intelligence V2.

It is designed for reviewers who want to understand where the metrics come from, which models support each analytics page, and how the dashboard connects to the BI export pack.

---

## End-to-End Lineage

```text
Seeded demo data
-> operational bakery records
-> build_bakery_metrics command
-> gold-layer metric snapshots
-> trusted analytics pages
-> BI-ready CSV exports