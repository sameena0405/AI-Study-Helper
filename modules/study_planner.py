from datetime import datetime, timedelta


def create_study_plan(
    subjects,
    start_date,
    days,
    daily_hours
):
    """
    Create a personalized study schedule.
    """

    plan = []

    # Calculate total available hours
    total_hours = daily_hours * days

    # Priority weights
    priority_weights = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    # Calculate total weight
    total_weight = sum(
        priority_weights.get(
            subject["priority"],
            1
        )
        for subject in subjects
    )

    # Allocate hours according to priority
    allocations = []

    for subject in subjects:

        weight = priority_weights.get(
            subject["priority"],
            1
        )

        hours = (
            total_hours
            * weight
            / total_weight
        )

        allocations.append({
            "name": subject["name"],
            "priority": subject["priority"],
            "hours": hours
        })

    # Create daily schedule
    remaining = {
        item["name"]: item["hours"]
        for item in allocations
    }

    priorities = {
        item["name"]: item["priority"]
        for item in allocations
    }

    for day_number in range(days):

        current_date = (
            start_date
            + timedelta(days=day_number)
        )

        sessions = []
        hours_left = daily_hours

        while hours_left > 0.01:

            available = [
                name
                for name, hours in remaining.items()
                if hours > 0.01
            ]

            if not available:
                break

            # Select subject with highest priority
            available.sort(
                key=lambda name: (
                    priority_weights.get(
                        priorities[name],
                        1
                    ),
                    remaining[name]
                ),
                reverse=True
            )

            subject = available[0]

            session_hours = min(
                1.0,
                hours_left,
                remaining[subject]
            )

            sessions.append({
                "subject": subject,
                "hours": round(
                    session_hours,
                    1
                ),
                "priority": priorities[subject]
            })

            remaining[subject] -= session_hours
            hours_left -= session_hours

        plan.append({
            "date": current_date,
            "day": day_number + 1,
            "sessions": sessions,
            "total_hours": round(
                sum(
                    session["hours"]
                    for session in sessions
                ),
                1
            )
        })

    return plan