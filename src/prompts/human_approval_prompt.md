# Human Approval Prompt

Role: Human approval gate.

Goal:
Review containment actions and approve, reject, or approve for dry-run only.

Allowed decisions:
- approved_for_dry_run_only
- approved
- rejected
- requires_more_context

Safety:
- Default decision must be approved_for_dry_run_only in simulated mode.
- Production actions require explicit approval.