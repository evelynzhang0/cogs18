"""A collection of functions for my project."""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (10, 5)


file = pd.read_csv('ed_sheeran_spotify.csv')



def data_processing(file):
    
    """Read a spotify song csv dataset and drop unnecessary columns,duplicates, and reset the index to song names

    Parameters
    ----------
    file : dataframe
       Dataframe that is not processed yet

    Returns
    -------
    data : dataframe
        Dataframe that is processed by going through the operations
    """


    #drop columns that are unnecessary(containing strings or numbers that won't be used in this project)
    data = file.drop(['id'],axis = 1)
    data = data.drop(['uri'],axis = 1)
    data = data.drop(['Unnamed: 0'],axis = 1)
    #drop potential duplicates
    data = data.drop_duplicates(subset=['name'])
    #reset index to song names
    data = data.set_index('name')
    
    return data



def best_album(data, trait):
    """Read the dataframe and find the album that has the highest value of an input trait(column names)

    Parameters
    ----------
    data : dataframe
        Dataframe that will be analyzed

    Returns
    -------
    result : string
        String that contains the album name
    """
   
    #sort the dataframe based on album name and calculate the mean value of each column/song trait
    album_sorted = data.groupby('album').mean()   
    #sort the dataframe based on mean of the input trait from high to low
    album_sorted = album_sorted.sort_values(by = trait, ascending = False)   
    #check potential duplicated mean value 
    if album_sorted.get(trait).iloc[0] ==  album_sorted.get(trait).iloc[1]:        
        result = "Duplicates found."#print result        
    else:        
        #locate the first album name of from the sorted dataframe
        album_champion = album_sorted.index[0]        
        result = album_champion
     
    return result
   


def song_recommender(song, data, trait):
    """Read the dataframe and recommend a top song that has the most similar trait to the input song's

    Parameters
    ----------
    data : dataframe
        Dataframe that will be analyzed
    song : string
        Song name that will be compared with
    trait : list
        List of song trait(s) that will be calculated based upon

    Returns
    -------
    most_similar_song : string
        String of the song name that is most similar to the input song
    """
    
    #drop the input song's row 
    without_input_song = data.drop(index = song)    
    #most_similar_song = song
    #get the song trait value of the input song
    input_song_info = data.get(trait).loc[song]    
    #create two empty lists for comparing songs and corresponding score
    comparing_song = []    
    comparing_sim_score = []
    #loop through the dataframe without the input song     
    for i in without_input_song.index:
        #append the song names to the list
        comparing_song.append(i)
        #get the song trait value of each comparing song        
        current_song_info = without_input_song.get(trait).loc[i]
        #use Euclidean distance formula to get the distance between two songs
        #the lower the score, the higher the similarity
        current_distance = (((input_song_info - current_song_info)**2).sum())**0.5
        #append the number to the list
        comparing_sim_score.append(current_distance)
        
    #convert lists to numpy array     
    comparing_song = np.array(comparing_song)    
    comparing_sim_score = np.array(comparing_sim_score)

    #create a similarity dataframe
    sim_df = pd.DataFrame()

    #create two columns corresponding to two arrays
    sim_df = sim_df.assign(songlist = comparing_song)
    sim_df = sim_df.assign(similarityscore = comparing_sim_score)
    #sort the dataframe by 'similarityscore' from low to high
    sim_df = sim_df.sort_values(by = ['similarityscore'])
    #get the first song name from the column 'songlist'
    most_similar_song = sim_df['songlist'].iloc[0]

    return most_similar_song


def best_season(data, trait):
    """Read the dataframe and return the season with the highest value of the input song trait

    Parameters
    ----------
    data : dataframe
        Dataframe that will be analyzed

    trait : string
        string of a song trait that will be calculated based upon

    Returns
    -------
    result : string
        String of result indicating the season with the highest value of the input song trait
    """    
    
    #create four lists of months for four seasons
    spring = ['03','04','05']
    summer = ['06','07','08']
    fall = ['09','10','11']
    winter = ['12','01','02']
    
    #create four variables used for recording the values of each season
    spring_val = 0
    summer_val = 0
    fall_val = 0
    winter_val = 0
    #loop through the index(being set to song names) of the data
    for i in data.index:
        #get the month of release for that song
        month_of_release = data.loc[i, 'release_date'][5:7]
        #get the corresponding trait value of that song
        trait_val = data.get(trait).loc[i]
        #check for the corresponding season and add values to the corresponding variable
        if month_of_release in spring:
            spring_wal = spring_val+trait_val
            
        elif month_of_release in summer:
            summer_val = summer_val+trait_val
            
        elif month_of_release in fall:
            fall_win = fall_val+trait_val
            
        else:
            winter_val = winter_val + trait_val
            
    #create numpy array containing season names           
    season_names = np.array(['spring','summer','fall','winter']) 
    #create numpy array containing values for four seasons
    season_values = np.array([spring_val,summer_val,fall_val,winter_val])
    #create dataframe and create two columns for two arrays
    season_data = pd.DataFrame()
    season_data = season_data.assign(names = season_names)
    season_data = season_data.assign(value = season_values)
    #sort the dataframe by values from high to low
    season_data = season_data.sort_values(by =['value'],ascending = False)
    #find the first season under the column 'name'
    best_season = season_data['names'].iloc[0]
    #indicate the finding
    result = best_season
        
    
    return result
    

    
def relation_graph(data, trait1, trait2):
    """Read the dataframe and create a correlation plot of two input traits

    Parameters
    ----------
    data : dataframe
        Dataframe that will be analyzed

    trait1, trait2 : strings
        string of a song trait that will be calculated based upon

    Returns
    -------
    None
       
    """        
    #set the parameters x and y axis to two traits 
    data.plot(kind = 'scatter', x = trait1, y = trait2, title = 'Relationship Between '+ trait1+' and '+trait2)
    #get information of two song traits and create line of best fit
    x = data.get(trait1)
    y = data.get(trait2)    
    a, b = np.polyfit(x, y, 1) 
    #create the plot with line of best fit
    plt.plot(x, a * x + b, label='Line of Best Fit')
    plt.legend()
    plt.show()