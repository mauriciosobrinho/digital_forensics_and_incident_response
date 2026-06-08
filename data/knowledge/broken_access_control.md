# Broken Access Control Notes

Broken access control includes missing authorization checks, IDOR, privilege escalation, and improper object-level authorization.

For invoice endpoints, server-side ownership checks are mandatory.

Mitigation:
- Enforce object-level authorization.
- Avoid trusting client-provided identifiers.
- Monitor enumeration behavior.
- Add rate limiting.
- Log denied access attempts.