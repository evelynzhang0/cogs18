"""A collection of test function for my project."""
import pytest
import os
import pandas as pd
from functions import * 



file = pd.read_csv('ed_sheeran_spotify.csv')

data = data_processing(file)


def test_data_processing():
    

    
    assert callable(data_processing)
    assert isinstance(data, pd.DataFrame)
    assert ('id' in data.columns) == False
    assert ('uri' in data.columns) == False
    assert ('Unnamed: 0' in data.columns)  == False
    assert ('Magical' in data.index) == True
    assert (len(data.index.unique())) == 183

    


def test_best_album():
    assert callable(best_album)
    assert isinstance(best_album(data,'loudness'), str)
    assert best_album(data,'loudness') == '2step (The Remixes)'
    assert best_album(data,'popularity') == '÷ (Deluxe)'
    assert best_album(data,'tempo') == '- (Deluxe)'
    
def test_song_recommender():
    assert callable(song_recommender)
    assert isinstance(song_recommender('Magical', data, ['loudness','popularity']), str)
    assert song_recommender('Magical', data, ['loudness','popularity']) == 'One Life'
    assert song_recommender('Amazing', data, ['energy','tempo'])== 'Sunburn'
    assert song_recommender('Page', data, ['liveness','speechiness']) == 'Supermarket Flowers'

    
def test_best_season():
    assert callable(best_season)
    assert isinstance(best_season(data, 'energy'), str)
    assert best_season(data, 'energy') == 'summer'
    assert best_season(data, 'valence')== 'summer'
    assert best_season(data, 'loudness')== 'spring'
                            
                            
                            
    
def test_relation_graph():
    assert callable(relation_graph)


                                