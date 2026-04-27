# BakeOps Intelligence — V3 Deployment Readiness Checklist

## Purpose

This document defines what must be checked before BakeOps Intelligence can be considered deployment-ready.

Deployment-ready does not mean the app is already deployed.

It means the project has a clear checklist for safely moving from local demo to a hosted environment later.

---

## Current Deployment Status

Current status:

```text
Production deployment: not claimed yet.
```

BakeOps should not claim production deployment until hosting, environment variables, database setup, static files, security settings, and verification checks are completed and documented.

---

## Deployment Readiness Principle

BakeOps should separate:

```text
local demo readiness
```

from:

```text
production deployment readiness
```

The current V3 project is strong as a local commercial-readiness demo.

Production deployment requires additional checks.

---

## Deployment Categories

### 1. Environment Configuration

```markdown
- [ ] `.env.example` is present
- [ ] real `.env` is not committed
- [ ] `SECRET_KEY` comes from environment
- [ ] `DEBUG=False` can be used in production
- [ ] `ALLOWED_HOSTS` is configured for deployment host
- [ ] database URL/configuration is environment-based
- [ ] sensitive credentials are not hard-coded
```

### 2. Database Readiness

```markdown
- [ ] production database target is selected
- [ ] migrations run successfully
- [ ] local `db.sqlite3` is not committed
- [ ] seed data command is clearly marked as demo-only
- [ ] backup/restore process is documented before real customer data
- [ ] data retention policy is defined before real customer data
```

### 3. Static Files

```markdown
- [ ] static files can be collected
- [ ] static serving strategy is defined
- [ ] production static configuration is tested
- [ ] missing static file errors are checked
```

Recommended command:

```powershell
python manage.py collectstatic --dry-run --noinput
```

### 4. Security

```markdown
- [ ] `DEBUG=False` tested
- [ ] `SECRET_KEY` not exposed
- [ ] admin URL and admin access reviewed
- [ ] CSRF settings reviewed
- [ ] allowed hosts reviewed
- [ ] HTTPS requirement defined
- [ ] security headers reviewed
- [ ] user data handling documented before real customer use
```

Recommended command:

```powershell
python manage.py check --deploy
```

Important: `check --deploy` may produce warnings in local development. Those warnings should be reviewed before any production claim.

### 5. Application Verification

Before deployment claim:

```markdown
- [ ] `python manage.py check` passes
- [ ] `python manage.py test bakeops` passes
- [ ] `python manage.py migrate` works
- [ ] `python manage.py seed_demo_data --reset` works for demo environment
- [ ] `python manage.py build_bakery_metrics` works
- [ ] `python manage.py export_bi_csv` works
- [ ] Signature insight verifies
```

Signature command:

```powershell
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
```

Expected:

```text
Birthday Classic 1 4 review
```

### 6. Route Verification

The following routes should return HTTP 200 before deployment is claimed:

```text
/analytics/
/analytics/products/
/analytics/ingredients/
/analytics/waste/
/analytics/occasions/
/analytics/customers/
/analytics/data-quality/
/analytics/exports/
```

### 7. Export Behaviour

```markdown
- [ ] export command generates expected files
- [ ] exports are reproducible
- [ ] generated exports are ignored by Git
- [ ] export folder permissions are understood for deployment
- [ ] BI export contract remains documented
```

Expected export evidence:

```text
Files generated: 11
Total rows exported: 52
```

### 8. Observability and Operations

Before production use:

```markdown
- [ ] logging strategy is defined
- [ ] error reporting strategy is defined
- [ ] uptime/health check approach is defined
- [ ] database backup approach is defined
- [ ] rollback approach is defined
- [ ] manual recovery steps are documented
```

### 9. Customer Data Readiness

Before handling real customer data:

```markdown
- [ ] data import workflow is implemented and tested
- [ ] rejected-row reporting is implemented
- [ ] customer data handling policy is defined
- [ ] privacy/security expectations are reviewed
- [ ] backup and deletion process is defined
- [ ] access control is reviewed
```

Current status:

```text
Not implemented yet.
```

---

## Deployment Claims Allowed

Safe wording:

```text
Deployment readiness checklist documented.
```

```text
Prepared for future deployment review.
```

```text
Local demo and verification workflow available.
```

```text
Production deployment not claimed yet.
```

---

## Deployment Claims Not Allowed

Do not claim:

```text
Production deployed.
```

```text
Live SaaS platform.
```

```text
Real customer environment.
```

```text
Production-ready for customer data.
```

```text
Secure for live customer data.
```

unless the required deployment, security, backup, and data handling checks have been completed and evidenced.

---

## Recommended Future Deployment Targets

Possible future deployment options:

| Option | Status | Notes |
|---|---|---|
| Render | Future candidate | Simple for Django demos |
| Railway | Future candidate | Good for quick app/database setup |
| Fly.io | Future candidate | More technical control |
| AWS | Future candidate | Stronger enterprise signal but more setup |
| DigitalOcean | Future candidate | Good VPS/App Platform option |

No deployment target is selected in Sprint 5.

---

## Sprint 5 Acceptance Criteria

Sprint 5 is complete when:

```markdown
- [ ] `docs/V3_BETA_READINESS.md` exists
- [ ] `docs/V3_DEPLOYMENT_READINESS_CHECKLIST.md` exists
- [ ] README references both Sprint 5 documents
- [ ] CHANGELOG records Sprint 5
- [ ] No deployment configuration is changed
- [ ] No production deployment claim is added
- [ ] No model files changed
- [ ] No migrations added
- [ ] `python manage.py check` passes
- [ ] `python manage.py test bakeops` passes
- [ ] Signature insight still returns `Birthday Classic 1 4 review`
```

---

## Boundary Confirmation

This document is a deployment readiness checklist.

It does not deploy the app.

It does not configure hosting.

It does not claim production readiness.

It prepares BakeOps for future deployment review.
