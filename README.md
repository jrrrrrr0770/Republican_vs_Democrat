### Project 3: Republican vs. Democrat Subbreddit Post Analysis

### Problem Statement
In this era of hyper-partisanship it can be difficult to identify the "news worthiness" of the news.  The responsibility to validate the information we consume falls to the consumer.  This process is difficult when the population is bombarded with a 24/7 news cycle that peddles editorials as news, and chooses what to report and how to report it based on which narritive it supports.  

To this end two political subreddits were chosen, based on their subscriber count and content type, with the goal of producing an algorithm that can determine the source of a post and thus determine its political bias.  The 'democrats' subreddit was chosen to represent the liberal bias and has 435,000 subscribers with news articles accounting for the bulk of the posts.  The 'Republican' subreddit was chosen for the conservative bias and has 189,000 subscibers with posts containing primarily news articles.

### Methodology
A script was created, executable from command line, that would call on the reddit API, request and verify reddit access, scrape two subreddits, drop duplicate rows, append data to a master file then output in terminal the 'after' endpoints which were used for the next scrape.  A total of 1475 unique posts were collected. Data cleaning and EDA was performed on the subreddit dataset preparing it for modeling.  

Six model/transformer combinations, three models (LogisticRegression, MultinomialNB, RandomForest) and two transformers (CountVectorizer, TfidfVectorizer), were used in a pipeline and iterated over, optimizing hyper-parameters, to find the best scoring model/transformer combination.  The two MultinomialNB models scored the highest with identical test scores and nearly identical training scores.  The MultinomialNB CountVectorizer model was chosen for further optimization; utilizing a ColumnTransformer to CountVectorize a second column 'domain'. The CountVectorizer was chosen over the TfidfVectorizer as I believed it would perform better with the relatively small and simple 'domain' dataset.  This optimized production model, MultinomialNB CountVectorizer ColumnTransformer, increased the test accuracy from 74% to 92%.  

### Conclusions/Recommendations
**Conclusions:** Performing EDA on the scraped data confirmed some assumptions I already had.  First, we as as population are heavily divided along partisan lines with only two users in this dataset choosing to explore the 'other side'.  Second, media outlets tend to cater to one side of the political spectrum or the other with zero overlap between Republican and Democrat media sources.  It is fairly safe to assume that this stark division in the media may be, at least partially, at fault for the growing division in the population.

By comparing three models, with two different transformers, then iterating over hyper-parameters to optimize accuracy, a nearly 75% accuracy rate was achieved by modeling the news article titles alone.  In a world with a purely objective, un-biased media one could assume accuracy would be 50%, given a dataset with equal representation from both sides of the political spectrum ie. the base case.  When news source was added to the model pipeline, accuracy increased to 92%.  Given this dataset, and the current media landscape, a simple list of right-leaning media versus left-leaning media would yield 100% accuracy rate.

**Recommendations:**As opposed to having just two classes, left versus right, it may be more useful to use sentiment analysis on the 'titles' to quantify how different media outlets report on the same events.  With this information it may be possible to map a spectrum of political leanings, far left to far right, and everything in between. 

### Sources
https://rasbt.github.io/mlxtend/user_guide/preprocessing/DenseTransformer/
https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
GA Breakfast Hour
GA Lessons 4.04 - 6.03 

### Data Dictionary
|Feature|Type|Dataset|Description|
|---|---|---|---|
|**title**|*object*|Subreddit API Scrape|Title of subreddit post| 
|**domain**|*object*|Subreddit API Scrape|Subreddit post content source| 
|**author**|*object*|Subreddit API Scrape|Poster's Reddit username| 
|**upvote_ratio**|*float64*|Subreddit API Scrape|Total # of upvotes / total votes| 
|**id**|*object*|Subreddit API Scrape|Unique post id| 
|**created_UTC**|*object*|Subreddit API Scrape|Date/Time subreddit post was created| 
|**subreddit**|*object*|Subreddit API Scrape|Subredit which post was scraped from| 