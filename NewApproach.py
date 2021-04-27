import pandas as pd
import copy
import re
from DataAssembly import create_dob_column
from DataAssembly import get_distinct_nationalities
from DataAssembly import create_participants_dictionary


"""Make sure to change the path to the files"""
"""Note that this approach scales well and works for ANY year. To change the year simply change the files we are inputing.That is
in the case we want to do for 2012 we would use fifa12 dataset and participants12 dataset """

participants16=pd.read_csv('/Users/david/DataSets/international-uefa-euro-championship-players-2016-to-2016-stats.csv')
fifa16=pd.read_csv('/Users/david/DataSets/Fifa/fifa16.csv',sep=';')



def modify_dob_participants(participants):
    """Changes the dob of the participants dataframe from year/month/day to day/month/year
    Args:
        input --> participants df
        output --> participants df with new column
    """
    participants['dob_modified']=0*len(participants)
    for i in range(len(participants)):
        year=participants.loc[i,'dob'][0:4]
        month=participants.loc[i,'dob'][5:7]
        day=participants16.loc[i,'dob'][8:11]
        participants.loc[i,'dob_modified']=day+'/'+month+'/'+year

    return participants





def match(participants,fifa,participants_dict):
    """Matches the players that we want to select and also creates a new column nationality in the fifa dataset
    Args:
        * input --> participants (our participants df), fifa(our fifa df) and the participants_dictionary
        * output --> df (dataframe with selected players),original_dict(the dictionary that we had)"""
    container=[]
    fifa=fifa.sort_values(by='Fullname')
    fifa['nationality']=0*len(fifa)
    for i in range(len(participants)):
        name=participants.loc[i,'full_name'].split()
        nationality=participants.loc[i,'nationality']
        for j in range(len(fifa)):
            if (re.findall(name[0],fifa.loc[j,'Fullname']) or re.findall(name[0],fifa.loc[j,'Fullname'])) and participants.loc[i,'dob_modified']==fifa.loc[j,'birth_date']:
                fifa.loc[j,'nationality']=participants.loc[i,'nationality']
                container.append(fifa.loc[j,:])
                try:
                    participants_dict[nationality].remove(' '.join(name))
                except ValueError:
                    pass

    df = pd.concat(container, axis=1)
    df = df.transpose()
    return df, participants_dict


def create_dataset(participants,fifa):
    """Merges everything together
    Input --> participants dataframe and fifa dataset
    Out---> df (dataframe with selected players),original_dict(the dictionary that we had)
        participants_left(dicitionary with participants still to match)"""
    participants_df=modify_dob_participants(participants)
    original_participants=create_participants_dictionary(participants)
    df,participants_left=match(participants,fifa,original_participants)
    return df, original_participants, participants_left









participants16=create_dob_column(participants16)
nationalities=get_distinct_nationalities(participants16)
players, original_participants, participants_left=create_dataset(participants16,fifa16)
print(participants_left)



"""IT TAKES A WHILE !!!!! and forget about the warning. Players is the dataframe with the players that we matched and participants left is the dictionary with the players
that we still need to include. We matched 458 but there are 95 missing"""
