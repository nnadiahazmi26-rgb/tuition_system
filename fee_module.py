SUBJECT_FEES = {
    "English": 50,
    "Bahasa Melayu": 40,
    "Mathematics": 60,
    "Science": 60,
    "History": 50,
    "Add Maths": 70,
}

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


# FUNCTIONS
def calculate_subject_total(subjects):
    """Calculation: adds up the monthly fee of all chosen subjects."""
    total = 0
    for subject in subjects:
        total += SUBJECT_FEES[subject]
    return total


def calculate_balance(total_fee, amount_paid):
    """Calculation: returns balance left to pay."""
    return total_fee - amount_paid


def get_status(total_fee, balance):
    """Decision-making: returns payment status."""
    if balance <= 0:
        return "Fully Paid"
    elif balance < total_fee:
        return "Partially Paid"
    else:
        return "Unpaid"


# PARENT CLASS 
class Student:
    def __init__(self, name, student_id, subjects, months):
        self.name = name               
        self.student_id = student_id  
        self.subjects = subjects       
        self.months = months            

    def calculate_total_fee(self):
        """Processing method: monthly subject total x number of months."""
        monthly_fee = calculate_subject_total(self.subjects)
        return monthly_fee * len(self.months)

    def get_info(self):
        return f"{self.name} ({self.student_id})"


# SUBCLASS (inheritance)
class ScholarshipStudent(Student):
    def __init__(self, name, student_id, subjects, months, discount):
        super().__init__(name, student_id, subjects, months)
        self.discount = discount        # new attribute

    def calculate_total_fee(self):
        """Modified feature: total fee after scholarship discount."""
        full_fee = super().calculate_total_fee()   # inherited method reused
        return full_fee - (full_fee * self.discount / 100)