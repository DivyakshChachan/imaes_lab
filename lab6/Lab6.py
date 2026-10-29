# Experiment 6: Fuzzy Logic and Constraint Satisfaction
# ---------- FUZZY LOGIC ----------
def fuzzy_membership(value, low_range, medium_range, high_range):
    """
    Calculates membership values for Low, Medium and High.
    """

    low = 0
    medium = 0
    high = 0

    # Low membership
    if value <= low_range[0]:
        low = 1
    elif value < low_range[1]:
        low = (low_range[1] - value) / (low_range[1] - low_range[0])

    # Medium membership
    if medium_range[0] <= value <= medium_range[1]:
        if value <= (medium_range[0] + medium_range[1]) / 2:
            medium = (value - medium_range[0]) / (
                (medium_range[1] - medium_range[0]) / 2
            )
        else:
            medium = (medium_range[1] - value) / (
                (medium_range[1] - medium_range[0]) / 2
            )

    # High membership
    if value >= high_range[1]:
        high = 1
    elif value > high_range[0]:
        high = (value - high_range[0]) / (high_range[1] - high_range[0])

    return {
        "Low": max(0, low),
        "Medium": max(0, medium),
        "High": max(0, high)
    }

def student_performance(attendance, marks):

    attendance_fuzzy = fuzzy_membership(
        attendance,
        (50, 70),
        (50, 90),
        (70, 90)
    )

    marks_fuzzy = fuzzy_membership(
        marks,
        (40, 60),
        (40, 80),
        (60, 80)
    )

    # Rules
    poor = max(
        min(attendance_fuzzy["Low"], marks_fuzzy["Low"]),
        min(attendance_fuzzy["Low"], marks_fuzzy["Medium"])
    )

    average = max(
        min(attendance_fuzzy["Low"], marks_fuzzy["High"]),
        min(attendance_fuzzy["Medium"], marks_fuzzy["Low"]),
        min(attendance_fuzzy["Medium"], marks_fuzzy["Medium"]),
        min(attendance_fuzzy["High"], marks_fuzzy["Low"])
    )

    good = max(
        min(attendance_fuzzy["Medium"], marks_fuzzy["High"]),
        min(attendance_fuzzy["High"], marks_fuzzy["Medium"]),
        min(attendance_fuzzy["High"], marks_fuzzy["High"])
    )

    # Defuzzification using weighted average
    output = (
        poor * 30 +
        average * 60 +
        good * 90
    )

    total = poor + average + good

    if total != 0:
        output = output / total

    if output < 45:
        performance = "Poor"
    elif output < 75:
        performance = "Average"
    else:
        performance = "Good"

    return output, performance


# Test cases
print("FUZZY LOGIC RESULTS")

attendance = 85
marks = 75

score, performance = student_performance(attendance, marks)

print("Attendance:", attendance)
print("Marks:", marks)
print("Performance Score:", round(score, 2))
print("Performance:", performance)


# ---------- CONSTRAINT SATISFACTION ----------

subjects = ["AI", "DBMS", "OS", "CN"]

time_slots = [9, 10, 11]

def is_valid(timetable):
    # Constraint 1:
    # AI and DBMS cannot have the same time
    if timetable["AI"] == timetable["DBMS"]:
        return False

    # Constraint 2:
    # OS and CN cannot have the same time
    if timetable["OS"] == timetable["CN"]:
        return False

    # Constraint 3:
    # AI must be before OS
    if timetable["AI"] >= timetable["OS"]:
        return False

    return True


def solve_timetable():
    timetable = {}

    for ai in time_slots:
        timetable["AI"] = ai

        for dbms in time_slots:
            timetable["DBMS"] = dbms

            for os in time_slots:
                timetable["OS"] = os

                for cn in time_slots:
                    timetable["CN"] = cn

                    if is_valid(timetable):
                        return timetable.copy()

    return None


solution = solve_timetable()

print("\nCONSTRAINT SATISFACTION RESULT")

if solution:
    for subject, time in solution.items():
        print(subject, "->", str(time) + ":00 AM")
else:
    print("No valid timetable found.")