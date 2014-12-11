from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from multiprocessing import Pool
from geopy.geocoders import Nominatim

from CelebResults.models import Clips_Adaptor, Mongo_Service


def index(request):
    '''
    Renders the main search page
    '''
    context = RequestContext(request,{
        })
    return render_to_response('CelebResults/index.html', context)

def get_sentiment_concur(tweet):
    clips = Clips_Adaptor()
    return clips.get_sentiment_concur(tweet)

def results(request):
    '''
    Renders the results page
    '''
    if request.method == "GET":
        clips = Clips_Adaptor()
        mongodb = Mongo_Service()
        geolocator = Nominatim()
        name = request.GET.__getitem__("artistname")

        ## If no input given, stay on search page
        if name == "":
            context = RequestContext(request,{
            })
            return render_to_response('CelebResults/index.html', context)

        ## Search tweets in mongo
        tweets = mongodb.search_tweets(name)

        ## If none found, search twitter
        convert = False
        if len(tweets) == 0:
            tweets = clips.search_tweets(name)
            convert = True

        coords = []
        countries = {}
        for index, tweet in enumerate(tweets):
            ## if the tweets came directly from clips, convert the unicode 
            ## to a dictionary
            if (convert):
                tweets[index] = {'text': tweet['text']}

            tweet["text"]=tweet["text"].encode('ascii','ignore')
            tweet["text"]=tweet["text"].replace('"','')
            try:
                curr_coords = tweet["coordinates"]
                if curr_coords["type"] == 'Point':
                    curr_coords = "{0}, {1}".format(curr_coords["coordinates"][1],curr_coords["coordinates"][0])
                    location = geolocator.reverse(curr_coords)
                    try:
                        country = location.raw['address']['country']
                    except:
                        country = None
                        
                    if country != None:
                        if country == "United States of America":
                            country = "United States"
                        if country == "Deutschland":
                            country = "Germany"
                       
                        if country in countries:
                            countries[country] = countries[country] + 1
                        else:
                            countries[country] = 1
                    
                    coords.append(curr_coords)
            except:
                coords.append([-200,-200])
        
        country_list = []
        for country in countries:
            country_list.append([str(country), countries[country]])

        ## Score the tweets with sentiment analysis
        pool = Pool(processes=5)
        scores = pool.map(get_sentiment_concur, tweets)
        pool.close()
        ## Convert the scores from strings to tuples
        for index, score in enumerate(scores):
            score = score.split(',')
            scores[index] = (score[0],score[1])

        context = RequestContext(request, {'tweets':tweets, 'scores': scores, 'country_list': country_list})
        return render_to_response('CelebResults/results.html', context)
        

