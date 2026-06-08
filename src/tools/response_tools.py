from datetime import datetime, timezone


def simulate_block_ip(
    ip: str,
    dry_run: bool = True,
) -> dict:
    return {
        "action": "block_ip",
        "target": ip,
        "dry_run": dry_run,
        "executed": False,
        "status": "simulated" if dry_run else "requires_real_executor",
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }


def simulate_rate_limit(
    endpoint: str,
    dry_run: bool = True,
) -> dict:
    return {
        "action": "rate_limit_endpoint",
        "target": endpoint,
        "dry_run": dry_run,
        "executed": False,
        "status": "simulated" if dry_run else "requires_real_executor",
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }