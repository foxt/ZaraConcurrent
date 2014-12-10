from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from multiprocessing import Pool

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
                    coords.append(curr_coords["coordinates"])
            except:
                coords.append([-200,-200])
                
        ## Score the tweets with sentiment analysis
        pool = Pool(processes=2)
        scores = pool.map(get_sentiment_concur, tweets)
        pool.close()
        ## Convert the scores from strings to tuples
        for index, score in enumerate(scores):
            score = score.split(',')
            scores[index] = (score[0],score[1])

        context = RequestContext(request, {'tweets':tweets, 'scores': scores, 'coordinates': coords})
        return render_to_response('CelebResults/results.html', context)
        

