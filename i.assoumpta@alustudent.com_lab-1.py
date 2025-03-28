#!/usr/bin/env python3
"""
ALU Grade Calculator - Ready for Terminal Use
Student: [Your Name]
Email: [Your Email]@alustudent.com
"""

class GradeCalculator:
    def __init__(self):
        self.assignments = []
        self.formative_total = 0.0
        self.summative_total = 0.0
        self.total_weight = 0.0
        self.PASS_THRESHOLD = 50.0  # Minimum % required in each category

    def clear_screen(self):
        """Clear terminal for better readability"""
        print("\033c", end="")  # ANSI escape code to clear screen

    def show_header(self):
        """Display program header"""
        self.clear_screen()
        print("="*50)
        print("ALU GRADE CALCULATOR".center(50))
        print("="*50)
        print(f"Passing requires ≥{self.PASS_THRESHOLD}% in both categories\n")

    def get_valid_number(self, prompt, min_val=0.0, max_val=100.0):
        """Get validated numeric input"""
        while True:
            try:
                value = float(input(prompt))
                if min_val <= value <= max_val:
                    return value
                print(f"Error: Must be between {min_val} and {max_val}")
            except ValueError:
                print("Invalid number. Please try again.")

    def add_assignment(self):
        """Add a new assignment with validation"""
        print("\n" + "-"*50)
        print("ADD NEW ASSIGNMENT (type 'back' to return)")
        print("-"*50)
        
        # Get assignment name
        name = input("Assignment name: ").strip()
        if name.lower() == 'back':
            return False

        # Get category
        while True:
            category = input("Category (Formative/Summative): ").lower()
            if category in ('formative', 'summative'):
                break
            elif category == 'back':
                return False
            print("Error: Must be 'Formative' or 'Summative'")

        # Get weight
        remaining_weight = 100 - self.total_weight
        weight_prompt = f"Weight (% of total grade, max {remaining_weight:.1f}%): "
        weight = self.get_valid_number(weight_prompt, max_val=remaining_weight)
        if weight is None:
            return False

        # Get grade
        grade = self.get_valid_number("Grade obtained (0-100%): ")
        if grade is None:
            return False

        # Store assignment
        self.assignments.append({
            'name': name,
            'category': category,
            'weight': weight,
            'grade': grade
        })

        # Update totals
        weighted_grade = (grade * weight) / 100
        if category == 'formative':
            self.formative_total += weighted_grade
        else:
            self.summative_total += weighted_grade
        self.total_weight += weight

        print(f"\n✅ Added: {name} ({category.title()}, {weight}%, Grade: {grade}%)")
        print(f"Current totals: Formative={self.formative_total:.1f}%, Summative={self.summative_total:.1f}%")
        return True

    def calculate_results(self):
        """Calculate final grades and status"""
        total_grade = self.formative_total + self.summative_total
        gpa = (total_grade / 100) * 5  # Convert to 5.0 scale
        
        passed = (self.formative_total >= self.PASS_THRESHOLD and 
                 self.summative_total >= self.PASS_THRESHOLD)
        
        return {
            'formative': self.formative_total,
            'summative': self.summative_total,
            'total': total_grade,
            'gpa': gpa,
            'status': "PASS" if passed else "FAIL (Must repeat course)"
        }

    def show_results(self, results):
        """Display final results"""
        self.clear_screen()
        print("="*50)
        print("FINAL RESULTS".center(50))
        print("="*50)
        print(f"{'Formative Total:':<20}{results['formative']:>10.2f}%")
        print(f"{'Summative Total:':<20}{results['summative']:>10.2f}%")
        print("-"*50)
        print(f"{'COURSE TOTAL:':<20}{results['total']:>10.2f}%")
        print(f"{'GPA:':<20}{results['gpa']:>10.2f}/5.0")
        print("="*50)
        print(f"STATUS: {results['status']}")
        print("="*50)

        # Show assignment details
        print("\nASSIGNMENT DETAILS:")
        for idx, assignment in enumerate(self.assignments, 1):
            print(f"{idx}. {assignment['name']}:")
            print(f"   - Category: {assignment['category'].title()}")
            print(f"   - Weight: {assignment['weight']}%")
            print(f"   - Grade: {assignment['grade']}%")

    def run(self):
        """Main program loop"""
        self.show_header()
        
        # Assignment entry loop
        while self.total_weight < 100:
            choice = input("\nAdd new assignment? (yes/no/exit): ").lower()
            
            if choice == 'no':
                break
            elif choice == 'exit':
                print("\nExiting program...")
                return
            elif choice != 'yes':
                print("Please enter 'yes', 'no', or 'exit'")
                continue
                
            self.add_assignment()

        # Calculate and show results
        if not self.assignments:
            print("\nNo assignments entered. Exiting.")
            return
            
        results = self.calculate_results()
        self.show_results(results)

if __name__ == "__main__":
    try:
        calculator = GradeCalculator()
        calculator.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")