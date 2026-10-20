import json
import os

DATA_FILE = "students.json"


class Student:
    """A single student record."""

    def __init__(self, student_id, name, gender, dob, year, address, age, nationality):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.gender = str(gender).strip().upper()
        self.dob = str(dob).strip().upper()
        self.year = str(year).strip().upper()
        self.address = str(address).strip().upper()
        self.age = str(age).strip().upper()
        self.nationality = str(nationality).strip().upper()  

    def to_dict(self):
        return {"id": self.student_id, "name": self.name, "gender": self.gender, "dob": self.dob, "year": self.year, "address": self.address, "age": self.age, "nationality": self.nationality}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["gender"], data["dob"], data["year"], data["address"], data["age"], data["nationality"])

    def __str__(self):
        return f"{self.student_id:<12}{self.name:<28}{self.gender:<8}{self.dob:<20}{self.year:<10}{self.address:<30}{self.nationality:<15}{self.age:<8}"


class StudentManager:
    """Handles all operations on student records and file persistence."""

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.students = {}  # id -> Student (fast lookup + unique IDs)
        self.load()

    # ---------- persistence ----------
    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                student = Student.from_dict(item)
                self.students[student.student_id] = student
        except (json.JSONDecodeError, KeyError, OSError) as err:
            print(f"Warning: could not read {self.filename} ({err}). Starting empty.")
            self.students = {}

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students.values()], f, indent=4)

    # ---------- operations ----------
    def add_student(self, student_id, name, gender, dob, year, address, nationality, age=""):
        student_id, name, gender, dob, year, address, nationality, age = student_id.strip(), name.strip(), gender.strip(), dob.strip(), year.strip(), address.strip(), nationality.strip(), age.strip()
        if not student_id or not name or not gender or not dob or not year or not address or not nationality:
            return False, "ID, name and gender cannot be empty."
        if student_id in self.students:
            return False, f"A student with ID '{student_id}' already exists."
        self.students[student_id] = Student(student_id, name, gender, dob, year, address, age, nationality)
        self.save()
        return True, "Student added successfully."

    def update_student(self, student_id, name=None, gender=None, dob=None, year=None, address=None, nationality=None, age=None):
        student = self.students.get(student_id.strip())
        if student is None:
            return False, f"No student found with ID '{student_id}'."
        if name and name.strip():
            student.name = name.strip()
        if gender and gender.strip():
            student.gender = gender.strip().upper()
        if dob and dob.strip():
            student.dob = dob.strip().upper()
        if year and year.strip():
            student.year = year.strip().upper()
        if address and address.strip():
            student.address = address.strip().upper()
        if nationality and nationality.strip():
            student.nationality = nationality.strip().upper()
        if age and age.strip():
            student.age = age.strip().upper()
        self.save()
        return True, "Student updated successfully."

    def delete_student(self, student_id):
        if self.students.pop(student_id.strip(), None) is None:
            return False, f"No student found with ID '{student_id}'."
        self.save()
        return True, "Student deleted successfully."

    def list_students(self):
        if not self.students:
            print("\nNo student records yet.")
            return
        headers = ("ID", "Name", "Gender", "DOB", "Year", "Address", "Nationality", "Age")
        students = sorted(self.students.values(), key=lambda student: student.student_id)
        rows = [
            (student.student_id, student.name, student.gender, student.dob,
             student.year, student.address, student.nationality, student.age)
            for student in students
        ]
        widths = [
            max(len(headers[index]), *(len(row[index]) for row in rows))
            for index in range(len(headers))
        ]

        def format_row(values):
            return "  ".join(f"{value:<{width}}" for value, width in zip(values, widths))

        header = format_row(headers)
        print("\n" + header)
        print("-" * len(header))
        for row in rows:
            print(format_row(row))
        print("-" * len(header))
        print(f"Total students: {len(self.students)}")


def show_menu():
    print("\n===== Student Management System =====")
    print("1. Add student")
    print("2. Update student")
    print("3. Delete student")
    print("4. List students")
    print("5. Exit")


def main():
    manager = StudentManager()
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            sid = input("Student ID: ")
            name = input("Name: ")
            gender = input("gender: ")
            dob = input("dob: ")
            year = input("year: ")
            address = input("address: ")
            nationality = input("nationality: ")
            age = input("age: ")
            print(manager.add_student(sid, name, gender, dob, year, address, nationality, age=age)[1])
            break
        elif choice == "2":
            sid = input("Student ID to update: ")
            name = input("New name (leave blank to keep): ")
            gender = input("New gender (leave blank to keep): ")
            dob = input("New dob (leave blank to keep): ")
            year = input("New year (leave blank to keep): ")
            address = input("New address (leave blank to keep): ")
            nationality = input("New nationality (leave blank to keep): ")
            age = input("New age (leave blank to keep): ")
            print(manager.update_student(sid, name, gender, dob, year, address, nationality, age=age)[1])
            break
        elif choice == "3":
            sid = input("Student ID to delete: ")
            print(manager.delete_student(sid)[1])
            break
        elif choice == "4":
            manager.list_students()
            break
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
