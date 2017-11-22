import pandas as pd
import os

bdown_table_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/bdown_tbl.csv"
df_bdown_table = pd.read_csv(bdown_table_csv_fname, encoding="UTF-8")

equipmentmappings_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/equipmentmappings.csv"
df_ioxnxt_equipment_mapping = pd.read_csv(equipmentmappings_csv_fname)

print(df_bdown_table.shape)
print(df_bdown_table.head())

#print(df_ioxnxt_equipment_mapping.shape)
#print(df_ioxnxt_equipment_mapping.head())



def replace_id_mapping ():
    # replace equipmentmapping Straddle ID to new with SC222 -> 222
    df_ioxnxt_equipment_mapping["n_id"] = pd.Series()
    df_ioxnxt_equipment_mapping["n_id"] = df_ioxnxt_equipment_mapping["s_id"].apply(lambda x: x[2:5])

    print(df_ioxnxt_equipment_mapping.columns.tolist())
    print(df_ioxnxt_equipment_mapping[["s_id","n_id","key"]] )

    dict = df_ioxnxt_equipment_mapping.set_index('key').to_dict()
   # gby = df_ioxnxt_equipment_mapping.groupby("key").to_dict()
    print(dict.keys)

replace_id_mapping()

def merge_tables():
    agent_history_straddle_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/assethistory_november.csv"
    df_agent_history_straddle = pd.read_csv(agent_history_straddle_csv_fname)

    print(df_agent_history_straddle.shape)
    print(df_agent_history_straddle.head())
    print(df_agent_history_straddle["IGN.1.ON"]).unique()
    #print(df_agent_history_straddle["KEY"].ix[1:10])

    #create new id column
    #df_agent_history_straddle["n_id"] = pd.Series(df_ioxnxt_equipment_mapping["n_id"].apply(lambda x: x[2:5]))
    #df_agent_history_straddle["KEY"] = df_ioxnxt_equipment_mapping
    #df_ioxnxt_equipment_mapping["s_id"]
    return

#merge_tables()

print("Success")