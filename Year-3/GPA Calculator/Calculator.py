class GPA:
    @staticmethod
    def calculate(grades: list[tuple[int, float, float]], return_hours: bool = False) -> float: # (Hours, Grade, Max_Grade)
        total_grades = total_hours = 0
        for subject_hours, student_grade, subject_grade in grades:
            total_grades += (student_grade / subject_grade) * 4.0 * subject_hours
            total_hours  += subject_hours
        gpa = round(total_grades / total_hours, 2)
        return (gpa, total_hours) if return_hours else gpa

    @staticmethod
    def update(*gpa_hours_pairs: tuple[float, int]) -> float: # (GPA, Hours)
        total_grades = total_hours = 0
        for gpa, hours in gpa_hours_pairs:
            total_grades += gpa * hours
            total_hours += hours
        return round(total_grades / total_hours, 2)

    @staticmethod
    def required_for_desired(current_gpa: float, spent_hours: int, desired_gpa: float, within_hours: int) -> float:
        required_gpa = (desired_gpa * (spent_hours + within_hours) - current_gpa * spent_hours) / within_hours
        return round(required_gpa, 2)

def classify(value: float) -> str:
    if 0.95 <= value <= 1.0:
        return 'A+'
    elif 0.90 <= value < 0.95:
        return 'A'
    elif 0.85 <= value < 0.90:
        return 'A-'
    elif 0.80 <= value < 0.85:
        return 'B+'
    elif 0.75 <= value < 0.80:
        return 'B'
    elif 0.70 <= value < 0.75:
        return 'B-'
    elif 0.65 <= value < 0.70:
        return 'C+'
    elif 0.60 <= value < 0.65:
        return 'C'
    elif 0.55 <= value < 0.60:
        return 'D+'
    elif 0.525 <= value < 0.55:
        return 'D'
    elif 0.50 <= value < 0.525:
        return 'D-'
    else:
        return 'F'

def colorize(value: float) -> str:
    value = max(0.0, min(1.0, value))

    if value < 0.5:
        return '#FF0000'

    elif value >= 0.75:
        t = (value - 0.75) / 0.25
        r = int(255 * (1 - t))
        g = 255
        b = 0
    else:
        t = (value - 0.5) / 0.25
        r = 255
        g = int(255 * t)
        b = 0

    return f'#{r:02X}{g:02X}{b:02X}'
