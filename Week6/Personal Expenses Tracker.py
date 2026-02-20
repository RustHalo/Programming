import json
import os
from datetime import datetime


expense_records= [] #List of tuples: (category, amount, date)
category_totals= {}
unique_categories= set()
DATA_FILE= "expenses.json"

def validate_date(date_text):
    """Extension: Validates date format YYY-MM-DD"""
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

#Extension: Save date to JSON for presistance
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(expense_records, f)

#Extension: Load existing data if file exists
def load_data():
    global expense_records
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            expense_records= json.load(f)
            expense_records= [tuple(x) for x in expense_records]

#Performs analysis and prints the report
def generate_report(records_to_analyze):
    if not records_to_analyze:
        print("\nNO records found to analyze.")
        return
    
    #categorize and sum expenses
    local_totals= {}
    local_uniques= set()
    amounts= []
    for cat, amt, date in records_to_analyze:
        local_uniques.add(cat)
        amounts.append(amt)
        local_totals[cat]= local_totals.get(cat, 0) + amt

    #calculate overall statistics
    total_spending= sum(amounts)
    avg_expenses= total_spending/len(amounts)

    highest= max(records_to_analyze, key=lambda x: x[1])
    lowest= min(records_to_analyze, key=lambda x: x[1])

    #printing the report
    print("\n" + "="*30)
    print("---> OVERALL SPENDING SUMMARY <---")
    print(f"Total Spending: ${total_spending:.2f}")
    print(f"Average Expenses: ${avg_expenses:.2f}")
    print(f"Highest Expense: ${highest[1]:.2f} (Category: {highest[0]}, Date: {highest[2]})")
    print(f"Lowest Expense: ${lowest[1]:.2f} (Category: {lowest[0]}, Date: {lowest[2]})")

    print("\n---> SPENDING BY CATEGORY <---")
    for cat, total in local_totals.items():
        bar= "#" * int(total/10)
        print(f"{cat:15}: ${total:8.2f} {bar}")
    print("="*30)


#main program flow:
def main():
    load_data()
    print("---> PERSONAL EXPENSE TRACKER <---")
    
    #Collect data loop
    count = 1
    target_entries = 6
    
    while len(expense_records) < target_entries:
        print(f"\nEnter expense {len(expense_records) + 1}:")
        
        cat = input("Category (e.g., Food, Transport): ").strip().capitalize()
        
        #Extension: Robust Amount Validation
        while True:
            try:
                amt = float(input("Amount: "))
                if amt < 0: raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a positive number.")
        
        #Extension: Robust Date Validation
        while True:
            date = input("Date (YYYY-MM-DD): ")
            if validate_date(date):
                break
            print("Invalid format. Please use YYYY-MM-DD.")

        expense_records.append((cat, amt, date))
        save_data()

    #Generate the standard report
    generate_report(expense_records)

    #Extension: Filter feature
    choice = input("\nWould you like to filter by category? (y/n): ").lower()
    if choice == 'y':
        filter_cat = input("Enter category to filter: ").capitalize()
        filtered = [r for r in expense_records if r[0] == filter_cat]
        generate_report(filtered)

if __name__ == "__main__":
    main()