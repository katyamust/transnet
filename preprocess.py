import pandas as pd
import os

#bdown_table_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/bdown_tbl.csv"
#df_bdown_table = pd.read_csv(bdown_table_csv_fname, encoding="UTF-8")

equipmentmappings_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/equipmentmappings.csv"
df_ioxnxt_equipment_mapping = pd.read_csv(equipmentmappings_csv_fname)

#agent_history_straddle_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/assethistory_november.csv"
#df_agent_history_straddle = pd.read_csv(agent_history_straddle_csv_fname)


#print(df_bdown_table.shape)
#print(df_bdown_table.head())

#print(df_ioxnxt_equipment_mapping.shape)
#print(df_ioxnxt_equipment_mapping.head())

#print(df_agent_history_straddle.shape)
#print(df_agent_history_straddle.head())


def replace_id_mapping ():
    # replace equipmentmapping Straddle ID to new with SC222 -> 222
    df_ioxnxt_equipment_mapping["n_id"] = pd.Series()
    df_ioxnxt_equipment_mapping["n_id"] = df_ioxnxt_equipment_mapping["s_id"].apply(lambda x: x[2:5])

    print(df_ioxnxt_equipment_mapping.columns.tolist())
    print(df_ioxnxt_equipment_mapping["n_id"] )

replace_id_mapping()

print("Success")