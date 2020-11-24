import pandas as pd
import snscrape.modules.twitter as sntwitter
import csv
#----------------------------------------------------------------------------------------
# scrape tweets of the governor of US states and territories & P/VP candidates of 2020.
def scrape():
    # get twitter_handle of politicians
    gov_data = pd.read_csv('Governors-Twitter-Handles-2020.csv')
    twitter_handle_list=gov_data['Twitter Handle'].to_list()
    twitter_state=gov_data['State'].to_list()
    twitter_party=gov_data['Party'].to_list()

    # scrape using snscrape module (https://github.com/JustAnotherArchivist/snscrape/blob/master/snscrape/modules/twitter.py)
    maxTweets = 3000000
    csvFile = open('twitter_dataset.csv', 'a', newline='', encoding='utf8')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['tweet_id','party','state','username','date','tweet'])

    for j in range(len(gov_data)):
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:{} + since:2019-11-17 until:2020-11-17-filter:links -filter:replies'.format(twitter_handle_list[j])).get_items()):
            if i > maxTweets :
                break
            csvWriter.writerow([tweet.id,twitter_party[j],twitter_state[j],twitter_handle_list[j],tweet.date, tweet.content])
    csvFile.close()

#----------------------------------------------------------------------------------------
# quick process of the data

# filter through chosen COVID related keywords
def filter(dataset):
    key_word_list = ['covid','covid-19','covid19','corona','coronavirus','pandemic','sars-cov-2','2019-nCoV','virus','epidemic','flu','influenza','cold']
    key_word = ''

    for kw in range(len(key_word_list)):
        if (kw == 0):
            key_word+='('
        key_word+=key_word_list[kw]
        if (kw!=len(key_word_list)-1):
            key_word+='|'
        else:
            key_word+=')'
#     print(key_word)
    COVID_data=dataset[dataset['tweet'].str.lower().str.contains(key_word, regex=True)]
#     print(len(COVID_data))
    return COVID_data

# get rid of hyperlinks
def hyperlink_handling(dataset):
    tweet = dataset['tweet'].tolist()
    cleaned_tweet_list = []
    for tw in tweet:
        tw_tok = tw.split()
        tw_str = ''
        for t in tw_tok:
            if 'http' not in t:
                tw_str += '{} '.format(t)
        cleaned_tweet_list.append(tw_str)

    dataset['tweet_cleaned'] = cleaned_tweet_list
#     print(len(dataset))
    return dataset

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# call functions

# scrape data
scrape()

# quick process of the data
twitter_data = pd.read_csv('twitter_dataset.csv')
raw_COVID_data = filter(twitter_data)
COVID_data = hyperlink_handling(raw_COVID_data)

#export this COVID dataframe to a csv file
COVID_data.to_csv('COVID_data.csv')
# print(len(COVID_data))
