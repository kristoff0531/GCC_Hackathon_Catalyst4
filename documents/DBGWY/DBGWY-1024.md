---
mnemonic: DBGWY
application_name: Digital Banking Gateway
owning_team: Digital Banking Engineering
tier: Tier 1
severity: High
issue_id: DBGWY-1024
---

# DBGWY-1024 — Transaction Gateway Timeout

## Symptom

Digital banking transactions remain pending and fail after the gateway timeout period.

## Root Cause

The downstream payment gateway is slow or unavailable.

## Fix

1. Check the payment gateway health dashboard.
2. Verify gateway connectivity and response status.
3. Review DBGWY transaction logs for timeout errors.
4. Escalate to Digital Banking Engineering if the gateway remains unavailable.
5. Retry the transaction only according to the approved runbook.

## Do NOT

Do NOT manually mark a transaction as successful when the downstream gateway has not confirmed the transaction.

## Escalation

Digital Banking Engineering