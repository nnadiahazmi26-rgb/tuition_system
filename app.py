import streamlit as st
from fee_module import Student, ScholarshipStudent
from fee_module import SUBJECT_FEES, MONTHS
from fee_module import calculate_subject_total, calculate_balance, get_status

PLACEHOLDER = "-- Select a subject --"

st.title("Tuition Fee Management System")

# Keep data between reruns
if "subjects" not in st.session_state:
    st.session_state.subjects = []
if "add_error" not in st.session_state:
    st.session_state.add_error = ""


# BUTTON ACTIONS (run before the page redraws)
def add_subject():
    choice = st.session_state.subject_choice
    if choice == PLACEHOLDER:
        st.session_state.add_error = "Please select a subject first."
    else:
        st.session_state.subjects.append(choice)
        st.session_state.subject_choice = PLACEHOLDER  # reset dropdown for next subject
        st.session_state.add_error = ""


def clear_subjects():
    st.session_state.subjects = []
    st.session_state.subject_choice = PLACEHOLDER
    st.session_state.add_error = ""


# STUDENT DETAILS 
name = st.text_input("Student Name")
student_id = st.text_input("Student ID")

# ADD SUBJECTS ONE BY ONE
st.subheader("Subjects")
subjects = st.session_state.subjects

# Only show subjects that are not added yet
remaining = [s for s in SUBJECT_FEES if s not in subjects]

if remaining:
    chosen = st.selectbox("Select Subject", [PLACEHOLDER] + remaining,
                          key="subject_choice")
    if chosen != PLACEHOLDER:
        st.info(f"{chosen} fee: RM {SUBJECT_FEES[chosen]:.2f} per month")
else:
    st.info("All subjects have been added.")

col1, col2 = st.columns(2)
col1.button("Add Subject", on_click=add_subject)
col2.button("Clear Subjects", on_click=clear_subjects)

if st.session_state.add_error:
    st.error(st.session_state.add_error)

# Show subjects added so far
if subjects:
    st.write("**Subjects added:**")
    for subject in subjects:
        st.write(f"- {subject}: RM {SUBJECT_FEES[subject]:.2f} per month")
    st.success(f"Total per month: RM {calculate_subject_total(subjects):.2f}")
else:
    st.write("No subjects added yet.")

# MONTHS, SCHOLARSHIP, PAYMENT 
st.subheader("Payment")
months = st.multiselect("Months Paying For", MONTHS)

has_scholarship = st.checkbox("Scholarship holder?")
discount = 0
if has_scholarship:
    discount = st.selectbox("Scholarship discount (%)", list(range(5, 105, 5)))

amount_text = st.text_input("Amount Paid (RM)")

# PROCESS BUTTON 
if st.button("Process Payment"):
    try:
        # Empty field checks
        if name.strip() == "" or student_id.strip() == "" or amount_text.strip() == "":
            st.error("Please fill in all fields.")
        elif len(subjects) == 0:
            st.error("Please add at least one subject.")
        elif len(months) == 0:
            st.error("Please choose at least one month.")
        else:
            amount_paid = float(amount_text)  # error if not a number

            # Create object
            if has_scholarship:
                student = ScholarshipStudent(name, student_id, subjects, months, discount)
            else:
                student = Student(name, student_id, subjects, months)

            total_fee = student.calculate_total_fee()

            if amount_paid < 0:
                st.error("Amount cannot be negative.")
            elif amount_paid > total_fee:
                st.error("Amount is more than the total fee.")
            else:
                balance = calculate_balance(total_fee, amount_paid)
                status = get_status(total_fee, balance)

                # ---------- OUTPUT ----------
                st.subheader("Result")
                st.write(student.get_info())
                st.write("**Subjects:**")
                for subject in subjects:
                    st.write(f"- {subject}: RM {SUBJECT_FEES[subject]:.2f} per month")
                st.write(f"**Months:** {', '.join(months)}")
                full_fee = calculate_subject_total(subjects) * len(months)
                if has_scholarship:
                    st.write(f"Total Fee (before discount): RM {full_fee:.2f}")
                    st.write(f"Scholarship discount: {discount}% (- RM {full_fee - total_fee:.2f})")
                    st.write(f"Total Fee (after discount): RM {total_fee:.2f}")
                else:
                    st.write(f"Total Fee: RM {total_fee:.2f}")
                st.write(f"Amount Paid: RM {amount_paid:.2f}")
                st.write(f"Balance: RM {balance:.2f}")
                if status == "Fully Paid":
                    st.success(status)
                else:
                    st.warning(status)

    except ValueError:
        st.error("Amount Paid must be a number.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")