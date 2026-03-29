# main.py
# Main module with menu to select tasks

from utils import input_int
import task1_series
import task2_loop
import task3_string
import task4_text
import task5_list

def main():
    """Main program loop."""
    while True:
        print("\n" + "="*50)
        print("LABORATORY WORK No. 3 (Variant 13)")
        print("="*50)
        print("1 - Task 1: ln(1+x) series expansion")
        print("2 - Task 2: count natural numbers")
        print("3 - Task 3: check octal string")
        print("4 - Task 4: analyze fixed text")
        print("5 - Task 5: process a list")
        print("0 - Exit")
        print("-"*50)

        choice = input_int("Select an option: ")

        if choice == 1:
            task1_series.run_task1()
        elif choice == 2:
            task2_loop.run_task2()
        elif choice == 3:
            task3_string.run_task3()
        elif choice == 4:
            task4_text.run_task4()
        elif choice == 5:
            task5_list.run_task5()
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 5.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()