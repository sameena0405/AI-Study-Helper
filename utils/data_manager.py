import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

NOTES_DIR = BASE_DIR / "data" / "notes"
PROGRESS_DIR = BASE_DIR / "data" / "progress"

QUIZ_FILE = PROGRESS_DIR / "quiz_results.json"
STUDY_FILE = PROGRESS_DIR / "study_hours.json"


# Create folders if they don't exist
NOTES_DIR.mkdir(parents=True, exist_ok=True)
PROGRESS_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# QUIZ RESULTS
# ==========================================

def save_quiz_result(score, total, accuracy):

    results = []

    if QUIZ_FILE.exists():

        try:
            with open(
                QUIZ_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    results = data

        except Exception:
            results = []

    results.append({
        "score": score,
        "total": total,
        "accuracy": accuracy
    })

    with open(
        QUIZ_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


# ==========================================
# GET QUIZ RESULTS
# ==========================================

def get_quiz_results():

    if not QUIZ_FILE.exists():
        return []

    try:

        with open(
            QUIZ_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            results = json.load(file)

        if isinstance(results, list):
            return results

        return []

    except Exception:
        return []


# ==========================================
# GET QUIZ STATISTICS
# ==========================================

def get_quiz_stats():

    results = get_quiz_results()

    if len(results) == 0:

        return {
            "quiz_count": 0,
            "accuracy": 0
        }

    accuracies = []

    for result in results:

        if "accuracy" in result:

            try:
                accuracies.append(
                    float(result["accuracy"])
                )
            except Exception:
                pass

    average_accuracy = (
        sum(accuracies) / len(accuracies)
        if accuracies
        else 0
    )

    return {
        "quiz_count": len(results),
        "accuracy": average_accuracy
    }


# ==========================================
# NOTES COUNT
# ==========================================

def get_notes_count():

    if not NOTES_DIR.exists():
        return 0

    files = [
        file
        for file in NOTES_DIR.iterdir()
        if file.is_file()
    ]

    return len(files)


# ==========================================
# STUDY HOURS
# ==========================================

def get_study_hours():

    if not STUDY_FILE.exists():
        return 0

    try:

        with open(
            STUDY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):

            return float(
                data.get("hours", 0)
            )

        return 0

    except Exception:

        return 0


# ==========================================
# SAVE STUDY HOURS
# ==========================================

def save_study_hours(hours):

    with open(
        STUDY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "hours": hours
            },
            file,
            indent=4
        )


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def get_dashboard_stats():

    quiz_stats = get_quiz_stats()

    return {
        "notes": get_notes_count(),
        "quizzes": quiz_stats["quiz_count"],
        "accuracy": quiz_stats["accuracy"],
        "study_hours": get_study_hours()
    }