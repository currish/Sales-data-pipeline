import pandas as pd

def clean_data(path):

    print("\nReading CSV Data")
    # Defined Path to read assignment_dataset.csv
    df = pd.read_csv(path)


    print("\nChecking Duplicate Rows")
    # Checking Duplicate Rows
    duplicate_rows = df.duplicated().sum()
    print("Total exact duplicate rows:", duplicate_rows)


    print("\nChecking Null Counts")
    # Checking null counts for each columns of the dataset
    null_counts = df.isnull().sum()
    print("Total number of null countts are:",null_counts)


    print("\nCategory Mapping")
    # Created a category map dictionary
    category_map = {
        "Laptop": "Electronics",
        "TV": "Electronics",
        "Phone": "Electronics",
        "Chair": "Furniture",
        "Table": "Furniture"
    }

    # Fill only missing category values with mapping based on item_name above
    df.loc[df["category"].isna(), "category"] = df["item_name"].map(category_map)

    null_counts = df.isnull().sum()
    print("\nTotal Null counts are:",null_counts)

    print(df['category'])


    print("\nFilling Discount Nulls")
    # replacing Null values in discount with 0
    df["discount"] = df["discount"].fillna(0)

    null_counts = df.isnull().sum()
    print("\nTotal Null counts are:",null_counts)


    print("\nStandardizing Category")
    # replacing lowercase letters like electronics with Electronics to make data structured
    df["category"] = df["category"].str.strip().str.title()

    print("\nUNIQUE VALUES IN CATEGORY")
    print(df["category"].unique())


    print("\nFixing Negative Quantity")
    '''Replacing negative values in quantity with 0. If 1 was chosen instead of 0, then new revenues would have been created, 
    which would make the dataset incorrect'''
    df["quantity"] = df["quantity"].clip(lower=0)
    print(df["quantity"])


    print("\nCorrecting Total Amount")
    # negative values of total_amount_corrected are replaced with 0
    df["total_amount_corrected"] = (df["quantity"] * df["unit_price"] -df["discount"]).clip(lower=0)


    print("\nCalculating Gross Revenue")
    # Calculated gross Revenue based on Unit Price and Quantity
    df["gross_revenue"] = df["unit_price"] * df["quantity"]


    print("\nFinal Data Preview")
    # Showcased the final data as output
    print(df.head(500))


    print("\nFinal Null Counts")
    # final null counts 
    print(df.isnull().sum())


    print("\nBilling Date Data Type Before")
    # Check incorrect Date format
    print(df["billing_date"].dtype)


    print("\nData Types Before Conversion")
    # Checking datatypes of each column in the dataset
    print(df.dtypes)


    print("\nConverting Billing Date")
    # Converted Datatype of billing_date from string to Date
    df["billing_date"] = pd.to_datetime(df["billing_date"],
    dayfirst = True)


    print("\nData Types After Conversion")
    # Checking datatypes of each column in the dataset
    print(df.dtypes)

    return df


if __name__ == "__main__":
    path = "data/assignment_dataset.csv"
    df = clean_data(path)