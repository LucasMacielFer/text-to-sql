import pandas as pd
from tabulate import tabulate

def create_df(desc, result):
    df = None
    dic = {}
    i = 0
    for column in desc:
        col_data = []

        for row in result:
            col_data.append(row[i])

        dic[column] = col_data[:]
        i+=1

    try:
        df = pd.DataFrame(dic)
    except Exception as e:
        print("Failed to create dataframe.")

    return df

def export_xml(df: pd.DataFrame):
    try:
        df.to_xml('data/your_search.xml', index=False, xml_declaration=False, encoding="utf-8")
    except Exception as e:
        print("Failed to export data to XML file.")

def export_csv(df: pd.DataFrame):
    try:
        df.to_csv('data/your_search.csv', index=False, encoding="utf-8")
    except Exception as e:
        print("Failed to export data to CSV file.")

def export_xlsx(df: pd.DataFrame):
    try:
        df.to_excel('data/your_search.xlsx', sheet_name="DATABASE SEARCH", index=False)
    except Exception as e:
        print("Failed to export data to XLSX file.")

def export_json(df: pd.DataFrame):
    try:
        df.to_json('data/your_search.json', orient='records', indent=2, force_ascii=False)
    except Exception as e:
        print("Failed to export data to JSON file.")

def export(df: pd.DataFrame, format):
    if format == "xml":
        export_xml(df)
    elif format == "csv":
        export_csv(df)
    elif format == "xlsx":
        export_xlsx(df)
    elif format == "json":
        export_json(df)
    else:
        print("Invalid format.")

def print_data(df: pd.DataFrame):
    print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex="always"))