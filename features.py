import pandas as pd
from datetime import timedelta
import datetime

#CONFIG
FEATURES_TO_INCLUDE = ["VIB.1.LIV","ENG.1.OILPRS","ENG.1.OILLVL","ENG.1.BAT","GPS.1.GNDSPD","SPRDR.1.SPD","FUEL.1.TNK2LVL","SPRDR.1.MOVEMENT","ENG.1.OILTEMP","BRAKE.1","RUNHRS.1"]
PATH_TO_DATA_FOLDER = r"C:\Users\jterh\Microsoft\OneDrive - Microsoft\_DX era\Hackathons\Machine Learning Hackfest South Africa\data"

if 0:
    agent_history_straddle_csv_fname = PATH_TO_DATA_FOLDER+r"\agenthistory_straddle_flat_filtered.csv"
else:
    agent_history_straddle_csv_fname = "C:/Users/kamustaf/Documents/transnet_data/agenthistory_straddle_flat_filtered.csv"
    features_file = "C:/Users/kamustaf/Documents/transnet_data/features.csv"

df_agent_history_straddle = pd.read_csv(agent_history_straddle_csv_fname)

#print(df_agent_history_straddle.shape)
#print(df_agent_history_straddle.head())

#add a new column containing just the EntryDate, not the Entry date and Time.
df_agent_history_straddle["EntryDate"] = pd.to_datetime(df_agent_history_straddle["EntryTime"]).dt.date

#print(df_agent_history_straddle.columns.tolist())

def get_features_for_day_and_param(df,param_name,date, date_name):
    #print("get_features_for_day_and_param")
    features = [str(date_name+"_"+param_name+"_MEAN"),str(date_name+"_"+param_name+"_STDDEV"),str(date_name+"_"+param_name+"_MAX")]
    if any(df.EntryDate == date) :
        v = df[df["EntryDate"] == date][param_name]
        v_mean = v.mean()
        v_stddev = v.std()
        v_max = v.max()
        d = {features[0]: [v_mean], features[1]: [v_stddev], features[2]: [v_max]}
        resultdf = pd.DataFrame(data = d)
        return resultdf

#print(get_features_for_day_and_param(df_agent_history_straddle,'VIB.1.LIV','1/8/2017','TODAY'))

def get_features_for_param(df,param_name, date,numdaysinhistory):
    #print("get_features_for_param")
    feature_names = ["TODAY"]
    for i in range(1,numdaysinhistory+1):
        feature_names.append(str(feature_names[0]+"-"+str(i)))
    resultdf = pd.DataFrame()
    for i in range(0,numdaysinhistory+1):
        datenew = date - timedelta(days=i)
        if any(df.EntryDate == datenew):
            r = get_features_for_day_and_param(df,param_name,datenew,feature_names[i])
            resultdf = pd.concat([resultdf,r],axis=1)
    return resultdf

#testdate = datetime.datetime.strptime('21/11/2017', "%d/%m/%Y").date()
#print(get_features_for_param(df_agent_history_straddle,'VIB.1.LIV', testdate,4))

def get_features(df,date,numdaysinhistory):
    print("get features")
    
    resultdf = pd.DataFrame()
    for f in FEATURES_TO_INCLUDE:
        r = get_features_for_param(df,f,date,numdaysinhistory)
        resultdf = pd.concat([resultdf,r],axis=1)
    return resultdf


def get_label(df, day):
    label = pd.DataFrame(data=[0],columns=["label"])
    if any(df[df.EntryDate == day].IncidentID.notna()):
        label = pd.DataFrame(data=[1])
    return label


def get_straddle_features_alldates(df):
    print("get_straddle_features_alldates")

    straddle_features = pd.DataFrame()

    days = df["EntryDate"].unique()
    print(days)

    for day in days:
        features_df = get_features(df,day,4)
        label_df = get_label(df,day)

        #concat with features_ df horisontally:
        features_df = pd.concat([features_df,label_df],axis=1)

        straddle_features = pd.concat([straddle_features,features_df],ignore_index=True)

        #print(features_df.shape)
        #print(straddle_features.shape)

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

    df_all_features = pd.DataFrame()
    for straddle in straddles:
        print(straddle)
        df_straddle = df[df["KEY"] == straddle]
        straddle_features = get_straddle_features_alldates(df_straddle)

        #concat all straddles
        df_all_features = pd.concat([df_all_features, straddle_features], ignore_index=True)

    return df_all_features

all_features = create_lagging_features(df_agent_history_straddle)
print(all_features.shape)

all_features.to_csv(features_file)

print("Done.")