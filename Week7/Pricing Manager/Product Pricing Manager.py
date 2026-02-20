import os


script_dir= os.path.dirname(os.path.abspath(__file__))
input_file= os.path.join(script_dir, 'products.txt')
output_file= os.path.join(script_dir, 'pricing_report.txt')

def process_pricing():
    category_discounts = {'Electronics': 0.10, 'Clothing': 0.15, 'Books': 0.05, 'Home': 0.12}
    tier_discounts = {'Premium': 0.05, 'Standard': 0.00, 'Budget': 0.02}
    
    total_products = 0
    total_discount_pct_sum = 0.0
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            
            outfile.write(f"{'Product Name':<25} | {'Base Price':<10} | {'Discount %':<10} | {'Discount Amt':<12} | {'Final Price':<10}\n")
            outfile.write("-" * 79 + "\n")

            for line in infile:
                try:
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        raise ValueError("Incorrect number of data fields.")
                    
                    name = parts[0].strip()
                    base_price = float(parts[1].strip())
                    category = parts[2].strip()
                    tier = parts[3].strip()

                    cat_disc = category_discounts.get(category, 0.0)
                    tier_disc = tier_discounts.get(tier, 0.0)
                    total_disc_pct = cat_disc + tier_disc

                    disc_amt = base_price * total_disc_pct
                    final_price = base_price - disc_amt

                    outfile.write(f"{name:<25} | ${base_price:<9.2f} | {total_disc_pct*100:<9.0f}% | ${disc_amt:<11.2f} | ${final_price:<9.2f}\n")

                    total_products += 1
                    total_discount_pct_sum += total_disc_pct

                except ValueError as ve:
                    print(f"Warning: Skipping invalid line '{line.strip()}' - {ve}")

        if total_products > 0:
            avg_discount = (total_discount_pct_sum / total_products) * 100
            print(f"Processing Complete.")
            print(f"Total products processed: {total_products}")
            print(f"Average discount applied: {avg_discount:.2f}%")
        else:
            print("No valid products were processed.")

    except FileNotFoundError:
        print("Error: The file 'products.txt' was not found. Please ensure it exists in the directory.")
    except PermissionError:
        print("Error: Write permission denied for 'pricing_report.txt'.")

if __name__ == "__main__":
    process_pricing()

