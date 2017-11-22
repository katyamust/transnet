import pandas as pd

agent_history_straddle_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/agenthistory_straddle_flat.csv"
df_agent_history_straddle = pd.read_csv(agent_history_straddle_csv_fname)

print(df_agent_history_straddle.shape)
#print(df_agent_history_straddle.head())
print(df_agent_history_straddle.columns.tolist())

def get_straddle_features(df,IoT_param_name):

    # get a day from entry time
    df["EntryTimeNew"] = df["EntryTime"].apply(lambda x: x[0:9])
    grouped = df.groupby(df["EntryTimeNew"])

    features = [str("TODAY_0_" + IoT_param_name + "_MEAN" ),
                str("TODAY_0_" + IoT_param_name + "_STDDEV" ),
                str("TODAY_0_" + IoT_param_name + "_MAX"),

                str("TODAY_1_" + IoT_param_name + "_MEAN"),
                str("TODAY_1_" + IoT_param_name + "_STDDEV"),
                str("TODAY_1_" + IoT_param_name + "_MAX"),

                str("TODAY_2_" + IoT_param_name + "_MEAN"),
                str("TODAY_2_" + IoT_param_name + "_STDDEV"),
                str("TODAY_2_" + IoT_param_name + "_MAX"),

                str("TODAY_3_" + IoT_param_name + "_MEAN"),
                str("TODAY_3_" + IoT_param_name + "_STDDEV"),
                str("TODAY_3_" + IoT_param_name + "_MAX")

                ]
    print(features)

    #IoT_param_mean =
    #IoT_param_stddev =
    #IoT_param_max =

    #VIB_1_LIV_mean = grouped["VIB.1.LIV"].to_list().mean()

    #df_new = pd.DataFrame(features)

    #print(df.head())

    return df


def create_lagging_features(df):

    grouped = df.groupby(df["KEY"])

    df_dict = grouped.groups
    d = dict.fromkeys(df_dict.keys())
    keys = df_dict.keys()
    print(df_dict.keys())

    for key in keys:
        df_straddle = df[df["KEY"] == key]
        print(key)

        get_straddle_features(df_straddle,"VIB.1.LIV")
       #both_df = merged[merged['_merge'] == 'both']
       # merged['_merge'] == 'both'
        #print(df_straddle.head())


    #print(df_dict.values())
    #print(df_dict['AFRICA.ZAF.KZN.DBN.TPT.POD.STRADDLE.2'])
    #print(grouped.shape())
    #print(grouped.head())

create_lagging_features(df_agent_history_straddle)

features = ["VIB.1.LIV_MEAN_TODAY","VIB.1.LIV_STDDEV_TODAY","VIB.1.LIV_MAX_TODAY",
           "VIB.1.LIV_MEAN_TODAY", "VIB.1.LIV_STDDEV_TODAY","VIB.1.LIV_MAX_TODAY1",
           "VIB.1.LIV_MEAN_TODAY", "VIB.1.LIV_STDDEV_TODAY","VIB.1.LIV_MAX_TODAY2",
           "VIB.1.LIV_MEAN_TODAY", "VIB.1.LIV_STDDEV_TODAY","VIB.1.LIV_MAX_TODAY3",
           "VIB.1.LIV_MEAN_TODAY", "VIB.1.LIV_STDDEV_TODAY","VIB.1.LIV_MAX_TODAY4",

           "ENG.1.OILPRS_MEAN_TODAY", "ENG.1.OILPRS_STDDEV_TODAY", "ENG.1.OILPRS_MAX_TODAY",
           "ENG.1.OILPRS_MEAN_TODAY", "ENG.1.OILPRS_STDDEV_TODAY", "ENG.1.OILPRS_MAX_TODAY1",
           "ENG.1.OILPRS_MEAN_TODAY", "ENG.1.OILPRS_STDDEV_TODAY", "ENG.1.OILPRS_MAX_TODAY2",
           "ENG.1.OILPRS_MEAN_TODAY", "ENG.1.OILPRS_STDDEV_TODAY", "ENG.1.OILPRS_MAX_TODAY3",
           "ENG.1.OILPRS_MEAN_TODAY", "ENG.1.OILPRS_STDDEV_TODAY", "ENG.1.OILPRS_MAX_TODAY4",

           "Breakdown"
           ]
