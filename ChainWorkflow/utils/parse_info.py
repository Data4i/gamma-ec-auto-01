import pandas as pd

def read_file(file_path):
    """
    Reads a JSON, Excel, CSV, Parquet, Feather, or TSV file into a Pandas DataFrame.
    
    Parameters:
        file_path (str): Path to the file.
    
    Returns:
        pd.DataFrame: DataFrame containing the file data.
    """
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            return pd.read_excel(file_path)
        elif file_path.endswith(".parquet"):
            return pd.read_parquet(file_path)
        elif file_path.endswith(".feather"):
            return pd.read_feather(file_path)
        elif file_path.endswith(".tsv"):
            return pd.read_csv(file_path, sep="\t")
        else:
            raise ValueError("Unsupported file format. Please use JSON, Excel, CSV, Parquet, Feather, or TSV.")
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def get_company_info(file_path):
    """
    Extracts company-related information from the given file.
    
    Parameters:
        file_path (str): Path to the file.
    
    Returns:
        tuple: Data for Company Names, Fields, Email, Phone, Preferred Channel, Objections, Engagement Level, and Notes.
    """
    df = read_file(file_path)
    if df is None:
        return None
    
    required_columns = [
        "Company_Names", "Company_Fields", "Email_Address", "Phone_Number", 
        "Preferred_Channel", "Objections", "Engagement_Level", "Company_Notes"
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        print(f"Error: Missing columns {missing_cols}.")
        print("Ensure all required columns are present in the file.")
        return None
    
    return (
        df["Company_Names"].values, df["Company_Fields"].values, df["Email_Address"].values, df["Phone_Number"].values, 
        df["Preferred_Channel"].values, df["Objections"].values, df["Engagement_Level"].values, df["Company_Notes"].values
    )