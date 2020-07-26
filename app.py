import flask
from flask import request, jsonify

import numpy as np
import pandas as pd


app = flask.Flask(__name__)


def city_data(city):
    '''This function takes in the city and returns it df.
    '''
    cities = ['aurangabad', 'agra', 'delhi', 'goa', 'jaipur']
    if city in cities:
        df = pd.read_csv('./data/csv/' + city + '.csv')
        return df
    else:
        print(f'The city is not in list: {cities}')
        return None

    
def location_data_sorted(city):
    df = city_data(city)
    df['tourist'] = df[df['tag']=='tourist_attraction']['types'].apply(\
        lambda x: \
                True if(('travel_agency' not in x) and ('car_rental' not in \
                        x) and ('taxi_stand' not in x) and ('political' not \
                        in x) and ('lodging' not in x)) else False)
    df['n_type'] = df['name'].apply(lambda x: True if(('tours' not in \
                        x.lower()) and ('rental' not in x.lower()) and \
                        ('taxi' not in x.lower())) else False)
    req_df = df[(df['tourist']==True) & (df['n_type']==True)]
    tour = req_df.sort_values(by=['rating', 'user_ratings_total'], 
                             ascending=[False, False])[['name', 'rating']]
    df['rel']=df['types'].apply(lambda x: True if('place_of_worship' in x)\
                        else False)
    rel = df[df['rel']==True].sort_values(by=['rating', 'user_ratings_total'],
                              ascending=[False, False])[['name', 'rating']]
    df['rest'] = df['types'].apply(lambda x: True if('restaurant' in x) else\
                            False)
    rest=df[df['rest']==True].sort_values(by=['rating', 'user_ratings_total'],
                              ascending=[False, False])[['name', 'rating']]
    req_df = df[df['tag']=='lodging']
    lod = req_df.sort_values(by=['rating', 'user_ratings_total'],
                              ascending=[False, False])[['name', 'rating']]
    df['park'] = df['types'].apply(lambda x: True if('campground' in x) or 
                            ('amusement_park' in x) or ('zoo' in x) else False)
    park = df[df['park']==True].sort_values(by=['rating','user_ratings_total'],
                            ascending=[False, False])[['name', 'rating']]
    
    x = pd.DataFrame()
    x['tourist_attraction'] = tour['name'][:10].values
    x['religious'] = rel['name'][:10].values
    x['restaurant'] = rest['name'][:10].values
    x['lodging'] = lod['name'][:10].values
    x['parks'] = park['name'][:10].values
    x = x.to_json()
    return x


@app.route("/", methods=['GET'])
def get_data():
    if 'city' in request.args:
        city = request.args['city']
        data = location_data_sorted(city.lower())
        return data
    else:
        return "Error: Please enter the following cities - ['aurangabad', 'agra', 'goa', 'delhi', 'jaipur']."
    
if __name__ == '__main__':
    app.run(port=5000, debug=False)