import pandas as pd
import os

PATH_TO_DATA_FOLDER = r"C:\Users\jterh\Microsoft\OneDrive - Microsoft\_DX era\Hackathons\Machine Learning Hackfest South Africa\data"

bdown_table_csv_fname = PATH_TO_DATA_FOLDER+r"\bdown_tbl.csv"
df_bdown_table = pd.read_csv(bdown_table_csv_fname, encoding="UTF-8")

equipmentmappings_csv_fname = PATH_TO_DATA_FOLDER+r"\equipmentmappings.csv"
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

#replace_id_mapping()

def merge_tables():
    agent_history_straddle_csv_fname = PATH_TO_DATA_FOLDER+r"\assethistory_november.csv"
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

#after the merge, taking agenthistory_straddle_flat csv and dropping columns
ahfile = PATH_TO_DATA_FOLDER+r'\agenthistory_straddle_flat_full.csv'
df = pd.read_csv(ahfile, encoding='utf8')

#preprocess: remove columns
def drop_columns(df):
    cols_to_remove = ['ID','VIB.1.MAX','GPS.1.GNDHEAD','GPS.1.ALT','GPS.1.LON','GPS.1.LAT','EntryTime15Mins','CAN.1.READY','PostUtc','FromUtc','GPS.1.SATS','GSM.1.RSSI','GEAR.1','ProcessUtc','GATEWAY.1.MAC','GATEWAY.1.VERSION','DIAG.1.THREAD','DIAG.1.EVENT','DIAG.1.MEM','ENGINE.1.OILLVL','NextBreakdown','Breakdown description','Reported by','Employee No','Description of repair','Shift','Status','Signed back by','Supervisor','OEM','Location']
    df = df.drop(cols_to_remove,axis=1)
    df.to_csv(PATH_TO_DATA_FOLDER+r'\agenthistory_straddle_flat_full_filtered.csv')
    return df

df = drop_columns(df)
print(df.shape)
print("Success")