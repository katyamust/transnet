import pandas as pd

agent_history_straddle_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/agenthistory_straddle_flat_filtered.csv"
df_agent_history_straddle = pd.read_csv(agent_history_straddle_csv_fname)

print(df_agent_history_straddle.shape)
#print(df_agent_history_straddle.head())
print(df_agent_history_straddle.columns.tolist())

def get_straddle_features(df,IoT_param_name):
    print("Straddle dataframe")

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

    #print(features)
    df_lagged = pd.DataFrame(columns=features)
    print(df_lagged.columns.tolist())

    # get a day from entry time
    df["EntryTimeNew"] = pd.to_datetime(df["EntryTime"]).dt.date
    #grouped = df.groupby(df["EntryTimeNew"])

    days = df["EntryTimeNew"].unique()
    #print(days)
    mean_series  = pd.Series(days.size)
    std_series = pd.Series(days.size)
    max_series = pd.Series(days.size)

    for day in days:

        IoT_params = df[df["EntryTimeNew"] == day][IoT_param_name]

        IoT_param_mean = IoT_params.mean()
        #mean_series = mean_series.append(pd.Series([IoT_param_mean]))

        IoT_param_stddev = IoT_params.std()
        #std_series = std_series.append(pd.Series([IoT_param_stddev]))

        IoT_param_max = IoT_params.max()
        #max_series = max_series.append(pd.Series([IoT_param_max]))

        #str("TODAY_0_" + IoT_param_name + "_STDDEV")
        #str("TODAY_0_" + IoT_param_name + "_MAX")

    #mean_series = mean_series.append(pd.Series([IoT_param_mean]))

    df_lagged[str("TODAY_0_" + IoT_param_name + "_MEAN")].append(pd.Series([IoT_param_mean]))
        #df_lagged[str("TODAY_0_" + IoT_param_name + "_MEAN")].append(mean_series)

    #print(IoT_param_mean)
    print(df_lagged.head())

   # IoT_param_mean = grouped[IoT_param_name].to_list()

    #IoT_param_stddev =
    #IoT_param_max =

    #VIB_1_LIV_mean = grouped["VIB.1.LIV"].to_list().mean()

    #df_new = pd.DataFrame(features)

    #print(df.head())

    return df_lagged

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
