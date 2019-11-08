import urllib.request, json, tweepy, time, schedule, sched, config
from datetime import datetime, timedelta
# API Keys
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret
#Authentication
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

user = api.me()

print(user.name)

#api.update_status('Testi testi')

def tweet(enemy,league,startTime,bestof):

    enemy = enemy
    league = league
    startTime = startTime
    bestof = bestof
    status = 'TPJ vs ' + enemy + ' alkaa 10 minuutin kuluttua! Ottelua voit seurata Twitch kanavallamme www.twitch.tv/tpjcommunity #esportsfi #' + league + ' #csgofi'
    api.update_status(status)
    #print(status)
    #print('Tweeted Succesfully')


def checkNextMatch():
    #Get JSON data of the matches
    url = "https://api.tpj.fi/api/data/upcoming"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    #Store the data of the next match
    if data:
        nextMatch = data[-1]
    else:
        print("ei matseja")
        return

    #extract key points of the match
    enemy = nextMatch["upcoming_enemy"]
    league = nextMatch["upcoming_league"]
    startDate = nextMatch["upcoming_match_day"]
    startTime = nextMatch["upcoming_startTime"]
    bestof = nextMatch["upcoming_bestOf"]

    #create a date object
    startDateAndTime = startDate + " " + startTime + ":00"
    print(startDateAndTime)
    matchStartTime = datetime.strptime(startDateAndTime, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    hourbefore = matchStartTime - timedelta(hours=1)
    print("MatchStartTime=", matchStartTime)
    print("Hourbefore =", hourbefore)
    print("Present =", now)
    print("StartTime =", startTime)

    #startTimeObject = datetime.strptime(startTime , "%H:%M")
    tweetTime = matchStartTime - timedelta(minutes=10)
    #tweetTime = tweetTime.time()


    print("if lauseen ulkopuolella")

    if hourbefore < now and now < tweetTime:
        print("if lause laukesi")
        year = tweetTime.year
        month = tweetTime.month
        day = tweetTime.day
        hour = tweetTime.hour
        min = tweetTime.minute
        sec = tweetTime.second

        # Set up scheduler
        s = sched.scheduler(time.time, time.sleep)
        s.enterabs(datetime(year,month,day,hour,min,sec).timestamp(), 0, tweet, argument=(enemy,league,startTime,bestof),)
        s.run()




schedule.every().minute.at(":45").do(checkNextMatch)

while True:
    schedule.run_pending()
    time.sleep(1)

print("TPJ stream going live in 10minutes as TPJ will be playing against " + enemy + " in " + league + " league at " + startTime + "EST!" )
#print(type(data[0]))
