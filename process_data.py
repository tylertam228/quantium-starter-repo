import pandas as pd
import os

data_folder = "data" #Open File

csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")] #Find all the .csv files
dataframes = []
for file in csv_files:
    file_path = os.path.join(data_folder, file) #Find out the complete path
    df = pd.read_csv(file_path) #Read File
    dataframes.append(df) #Adding Elements

combined_df = pd.concat(dataframes, ignore_index=True) #Combine the data

pink_morsel_df = combined_df[combined_df["product"] == "pink morsel"] #Find product == pink morsel
pink_morsel_df["sales"] = pink_morsel_df["quantity"] * pink_morsel_df["price"] # find the sales of pink morsel

output_df = pink_morsel_df[["sales", "date", "region"]]
output_df.to_csv("output.csv", index=False)
#source venv/bin/activate
print("Done") #run python process_data.py