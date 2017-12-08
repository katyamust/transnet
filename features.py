import pandas as pd
from datetime import timedelta
#import datetime
import json
import time

#CONFIG

with open('config.json') as json_config_file:
    config = json.load(json_config_file)

FEATURES_TO_INCLUDE = ["VIB.1.LIV","ENG.1.OILPRS","ENG.1.OILLVL","ENG.1.BAT","GPS.1.GNDSPD","SPRDR.1.SPD","FUEL.1.TNK2LVL","SPRDR.1.MOVEMENT","ENG.1.OILTEMP","BRAKE.1","RUNHRS.1"]
PATH_TO_DATA_FOLDER = config["path"]["Katya"]
TEST=1 # run on smaller data set for testing this code

if TEST:
    agent_history_straddle_csv_fname = PATH_TO_DATA_FOLDER + config["files"]["test_dataset"]
    features_file = PATH_TO_DATA_FOLDER + config["files"]["test_featureset"]
else:
    agent_history_straddle_csv_fname = PATH_TO_DATA_FOLDER + config["files"]["dataset"]
    features_file = PATH_TO_DATA_FOLDER + config["files"]["featureset"]

start_time = time.time()
print("loading dataframe ")
df_agent_history_straddle = pd.read_csv(agent_history_straddle_csv_fname)
print("--- %s seconds ---" % (time.time() - start_time))

print(df_agent_history_straddle.shape)
#print(df_agent_history_straddle.head())

#add a new column containing just the EntryDate, not the Entry date and Time.
df_agent_history_straddle["EntryDate"] = pd.to_datetime(df_agent_history_straddle["EntryTime"]).dt.date

#print(df_agent_history_straddle.columns.tolist())

def get_features_for_day_and_param(df_date,param_name,date_name):

    #print("get_features_for_day_and_param")
    features = [str(date_name+"_"+param_name+"_MEAN"),str(date_name+"_"+param_name+"_STDDEV"),str(date_name+"_"+param_name+"_MAX")]

    if not df_date.empty :#any(df.EntryDate == date) :
        v = df_date[param_name]
        v_mean = v.mean()
        v_stddev = v.std()
        v_max = v.max()
        d = {features[0]: [v_mean], features[1]: [v_stddev], features[2]: [v_max]}
    else:
        d = {features[0]: [None], features[1]: [None], features[2]: [None]}
    resultdf = pd.DataFrame(data=d)
    return resultdf

#print(get_features_for_day_and_param(df_agent_history_straddle,'VIB.1.LIV','1/8/2017','TODAY'))

def get_features_for_param(df_straddle,param_name1, date,numdaysinhistory):
    #print("get_features_for_param")
    date_names = ["TODAY"]
    for i in range(1,numdaysinhistory+1):
        date_names.append(str(date_names[0]+"-"+str(i)))

    resultdf_list = []
    for i in range(0,numdaysinhistory+1):
        datenew = date - timedelta(days=i)
        df_date = df_straddle[df_straddle["EntryDate"] == datenew]

        #if df_date.empty:
        #    continue

        params_list_this_date = []
        for param_name in FEATURES_TO_INCLUDE:
            r_df = get_features_for_day_and_param(df_date,param_name,date_names[i])
            params_list_this_date.append(r_df)
        params_df_this_date = pd.concat(params_list_this_date,axis =1)
        resultdf_list.append(params_df_this_date)
    resultdf = pd.concat(resultdf_list, axis=1)
    return resultdf

#testdate = datetime.datetime.strptime('21/11/2017', "%d/%m/%Y").date()
#print(get_features_for_param(df_agent_history_straddle,'VIB.1.LIV', testdate,4))

def get_features(df_straddle,date,numdaysinhistory):
    #print("get features for date")

###########
    param_name_not_used = ""
    r1 = get_features_for_param(df_straddle,param_name_not_used,date,numdaysinhistory)
    return r1
###########

    #start_time = time.time()

    resultdf = pd.DataFrame()

    resultdf_list = []
    #for f in FEATURES_TO_INCLUDE:
    param_name_not_used = ""
    r = get_features_for_param(df_straddle,param_name_not_used,date,numdaysinhistory)
    resultdf_list.append(r)
        #resultdf = pd.concat([resultdf,r],axis=1)
    resultdf = pd.concat(resultdf_list, axis=1)
    #print("--- %s seconds ---" % (time.time() - start_time))

    return resultdf


def get_label(df, day):
    label = pd.DataFrame(data=[0],columns=["label"])
    if any(df[df.EntryDate == day].IncidentID.notna()):
        label = pd.DataFrame(data=[1],columns=["label"])
    return label

def get_straddle_features_alldates(df_straddle):
    print("get_straddle_features_alldates")

    #straddle_features = pd.DataFrame()
    straddle_features_list = []

    days = df_straddle["EntryDate"].unique()
    print(days)

    for day in days:
        features_df = get_features(df_straddle,day,4)
        #print("features_df")
        #print(features_df.shape)
        label_df = get_label(df_straddle,day)

        #concat with features_ df horisontally:
        print("features_df labels df concat")
        start_time = time.time()
        features_df = pd.concat([features_df,label_df],axis=1)

        print(features_df.shape)
        print("--- %s seconds ---" % (time.time() - start_time))

        straddle_features_list.append(features_df)
        #straddle_features = pd.concat([straddle_features,features_df],ignore_index=True)

    straddle_features = pd.concat(straddle_features_list,ignore_index=True)

    return straddle_features

#testdate = datetime.datetime.strptime('21/11/2017', "%d/%m/%Y").date()
#print(get_features(df_agent_history_straddle, testdate,4))

def create_lagging_features(df):

    print("create straddle features")
    grouped = df.groupby(df["KEY"])

    df_dict = grouped.groups
    d = dict.fromkeys(df_dict.keys())
    straddles = df_dict.keys()
    print(straddles)

    #df_all_features = pd.DataFrame()
    df_all_straddles_features_list = []
    for straddle in straddles:
        print(straddle)
        df_straddle = df[df["KEY"] == straddle]
        straddle_features = get_straddle_features_alldates(df_straddle)

        df_all_straddles_features_list.append(straddle_features)

    # concat all straddles
    df_all_straddles_features = pd.concat(df_all_straddles_features_list, ignore_index=True)

    return df_all_straddles_features

start_time = time.time()
all_features = create_lagging_features(df_agent_history_straddle)
print(all_features.shape)

all_features.to_csv(features_file)
print("--- %s seconds ---" % (time.time() - start_time))

print("Done.")