# BakeOps Intelligence — Data Lineage

## Purpose

This document explains how data moves through BakeOps Intelligence from seeded operational records to trusted analytics pages and BI-ready CSV exports.

It is designed for reviewers who want to understand:

- where the data starts
- how the metric layer is built
- which models support the analytics pages
- how the dashboard connects to exported BI files
- what is implemented now versus planned for future commercial work

---

## End-to-End Lineage

```text
seed_demo_data
-> operational bakery records
-> build_bakery_metrics
-> gold-layer metric snapshots
-> trusted analytics pages
-> export_bi_csv
-> BI-ready CSV files