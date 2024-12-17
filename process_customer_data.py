import pandas as pd

def clean_email(email):
    """Clean and validate email address"""
    if not isinstance(email, str):
        return None
    email = email.strip()
    return email if email and email != " " else None

def get_first_name(full_name):
    """Extract first name from full name"""
    if not isinstance(full_name, str):
        return None
    
    # Handle special cases like "Alliance Bernstein (Amber Fleck)"
    if "(" in full_name:
        start = full_name.find("(") + 1
        end = full_name.find(")")
        if start > 0 and end > start:
            full_name = full_name[start:end]
    
    # Remove any "here" or "test" entries
    if full_name.lower() in ["here", "test"]:
        return None
        
    parts = full_name.strip().split()
    return parts[0] if parts else None

def process_line(line):
    """Process a single line of data"""
    if "\t" not in line:
        return None
    
    parts = line.split("\t")
    if len(parts) < 2:
        return None
        
    name = parts[0].strip()
    email = clean_email(parts[1].strip())
    
    if not name or name.lower() in ["name", "customer"]:
        return None
    
    if email:  # Only include entries with valid emails
        first_name = get_first_name(name)
        if first_name:  # Only include if we can get a valid first name
            return {
                "First Name": first_name,
                "Email": email,
                "Birthday": None
            }
    return None

# Process all lines from new_customer_data.txt
data = []
with open("new_customer_data.txt", "r") as f:
    for line in f:
        result = process_line(line.strip())
        if result:
            data.append(result)

# Create DataFrame
df = pd.DataFrame(data)

# Remove duplicate emails
df = df.drop_duplicates(subset=["Email"])

# Save to CSV
df.to_csv("customer_data.csv", index=False)
print(f"Processed {len(data)} records.")
print(f"After removing duplicates: {len(df)} records.")
print("Spreadsheet has been created as customer_data.csv") 