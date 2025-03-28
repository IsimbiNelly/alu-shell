#!/usr/bin/env python3
"""
ALU Grade Calculator - Final Production Version
Student: Isimbi Nelly Assoumpta
Email: i.assoumpta@alustudent.com

Key Features:
- Complete implementation of all requirements
- Robust input validation
- Clear category-wise breakdown
- Accurate GPA calculation
- Comprehensive pass/fail decision
"""

class GradeCalculator:
    def __init__(self):
        self.assignments = []
        self.formative_total = 0.0
        self.summative_total = 0.0
        self.total_weight = 0.0
        self.PASS_THRESHOLD = 50.0  # Minimum required in each category

    def clear_screen(self):
        """Clears terminal for better readability"""
        print("\033c", end="")

    def show_header(self):
        """Displays program header"""
        self.clear_screen()
        print("="*50)
        print("ALU GRADE CALCULATOR".center(50))
        print("="*50)
        print(f"Passing requires ≥{self.PASS_THRESHOLD}% in both categories\n")

    def get_valid_input(self, prompt, input_type=float, min_val=0.0, max_val=100.0):
        """Validates user input with clear error messages"""
        while True:
            user_input = input(prompt)
            if user_input.lower() == 'exit':
                return None
            try:
                value = input_type(user_input)
                if min_val <= value <= max_val:
                    return value
                print(f"Error: Value must be between {min_val} and {max_val}")
            except ValueError:
                print(f"Invalid input. Please enter a {'number' if input_type==float else 'valid choice'}")

    def add_assignment(self):
        """Handles assignment entry with real-time validation"""
        print("\n" + "-"*50)
        print("NEW ASSIGNMENT ENTRY (type 'exit' to cancel)")
        print("-"*50)
        
        # Get and validate assignment name
        name = input("Assignment name: ").strip()
        if not name:
            print("Error: Name cannot be empty")
            return False

        # Get and validate category
        while True:
            category = input("Category (Formative/Summative): ").lower()
            if category in ('formative', 'summative'):
                break
            print("Error: Must be 'Formative' or 'Summative'")

        # Get and validate weight
        remaining_weight = 100 - self.total_weight
        weight = self.get_valid_input(
            f"Weight (% of total grade, max {remaining_weight}%): ",
            max_val=remaining_weight
        )
        if weight is None:
            return False

        # Get and validate grade
        grade = self.get_valid_input("Grade obtained (0-100%): ")
        if grade is None:
            return False

        # Store assignment and update totals
        self.assignments.append({
            'name': name,
            'category': category,
            'weight': weight,
            'grade': grade
        })

        weighted_grade = (grade * weight) / 100
        if category == 'formative':
            self.formative_total += weighted_grade
        else:
            self.summative_total += weighted_grade
        self.total_weight += weight

        print(f"\n✅ Added '{name}' ({category.title()}, {weight}%, Grade: {grade}%)")
        print(f"Current totals: Formative={self.formative_total:.1f}%, Summative={self.summative_total:.1f}%")
        return True

    def calculate_gpa(self, total_grade):
        """Converts percentage grade to 5.0 scale"""
        return (total_grade / 100) * 5

    def determine_status(self):
        """Implements pass/fail decision logic"""
        formative_pass = self.formative_total >= self.PASS_THRESHOLD
        summative_pass = self.summative_total >= self.PASS_THRESHOLD
        
        if formative_pass and summative_pass:
            return "PASS", ""
        else:
            reasons = []
            if not formative_pass:
                reasons.append(f"Formative grade ({self.formative_total:.1f}% < {self.PASS_THRESHOLD}%)")
            if not summative_pass:
                reasons.append(f"Summative grade ({self.summative_total:.1f}% < {self.PASS_THRESHOLD}%)")
            return "FAIL (Must repeat course)", " | ".join(reasons)

    def show_results(self):
        """Displays comprehensive results"""
        self.clear_screen()
        total_grade = self.formative_total + self.summative_total
        gpa = self.calculate_gpa(total_grade)
        status, reasons = self.determine_status()

        print("="*50)
        print("FINAL GRADE REPORT".center(50))
        print("="*50)
        print(f"{'Formative Total:':<20}{self.formative_total:>10.2f}%")
        print(f"{'Summative Total:':<20}{self.summative_total:>10.2f}%")
        print("-"*50)
        print(f"{'COURSE TOTAL:':<20}{total_grade:>10.2f}%")
        print(f"{'GPA:':<20}{gpa:>10.2f}/5.0")
        print("="*50)
        print(f"STATUS: {status}")
        if reasons:
            print(f"REASON: {reasons}")
        print("="*50)

        # Detailed assignment breakdown
        print("\nASSIGNMENT DETAILS:")
        for idx, assignment in enumerate(self.assignments, 1):
            print(f"{idx}. {assignment['name']}:")
            print(f"   - Category: {assignment['category'].title()}")
            print(f"   - Weight: {assignment['weight']}%")
            print(f"   - Grade: {assignment['grade']}%")
            print(f"   - Contribution: {(assignment['grade'] * assignment['weight'])/100:.2f}%")

    def run(self):
        """Main program execution flow"""
        self.show_header()
        
        while self.total_weight < 100:
            choice = input("\nAdd new assignment? (yes/no/exit): ").lower()
            
            if choice == 'no':
                break
            if choice == 'exit':
                print("\nExiting program...")
                return
            if choice != 'yes':
                print("Please enter 'yes', 'no', or 'exit'")
                continue
                
            self.add_assignment()

        if not self.assignments:
            print("\nNo assignments entered. Exiting.")
            return
            
        self.show_results()

if __name__ == "__main__":
    try:
        calculator = GradeCalculator()
        calculator.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")