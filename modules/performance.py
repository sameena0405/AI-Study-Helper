def calculate_accuracy(correct, total):

    if total == 0:
        return 0

    return (correct / total) * 100


def performance_level(accuracy):

    if accuracy >= 80:
        return "Excellent"

    if accuracy >= 60:
        return "Good"

    if accuracy >= 40:
        return "Needs Improvement"

    return "Needs More Practice"