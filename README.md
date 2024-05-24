# Large Scale Analysis: Abortion Discourse on r/Conservative

## Introduction

Abortion remains a contentious and deeply entrenched debate in America and American politics. Despite its apparent legal solidity following the landmark case Roe v. Wade in 1973, which guaranteed the constitutional right to privacy (including the right to an abortion), this framework was dramatically altered in the unprecedented ruling of Dobbs v. Jackson Women’s Health Organization. In 2022, this decision effectively overturned Roe v. Wade and returned the power of regulating abortion back to the states.

Following the Dobbs ruling, the legality of abortion in America has become fragmented, with over fourteen states enacting all-out abortion bans and an additional seven implementing laws severely restricting abortion ([State Bans on Abortion Throughout Pregnancy, 2024](https://www.guttmacher.org/state-policy/explore/state-policies-abortion-bans)). Furthermore, the issue has emerged as a focal point in the upcoming 2024 election, where abortion is expected to be a battleground issue. In over eleven states, voters will weigh in on addressing measures surrounding abortion ([Mulvihill and Kruesi, 2024](https://apnews.com/article/abortion-ballot-amendment-ban-protection-states-2024-052ff9846f8416efb725240af22b92ec)). Against this unparalleled legal upheaval, political turmoil, and the continued erosion of established rights, research into the discourse and attitudes surrounding the topic becomes even more imperative.


## Objective

In light of this climate, my final project here aims to conduct a large-scale analysis of abortion discourse using Reddit, a social media platform known for its unique features like pseudonymity and topical division of ‘Subreddits.’ These attributes not only distinguish Reddit as a platform but present a compelling opportunity for research, potentially fostering more candid and open discussions, especially regarding more sensitive and stigmatized topics such as abortion.

Specifically, I will be examining discourse surrounding abortion within the r/Conservative Subreddit. I have chosen this Subreddit for several reasons:

1. The Subreddit has over 1 million users, making it a prominent platform within Reddit.
2. Preliminary research (limited to 1000 posts via the Reddit API) revealed significant activity surrounding abortion within the Subreddit.
3. The persistent reaction and stances of Conservative politicians regarding abortion underscore the significance of the topic within the party, often becoming a focal point of their political identity. This emphasis placed on abortion within Conservative circles makes r/Conservative a pivotal place for my intended research, and to investigate my primary research question of whether abortion attitudes and discourse have evolved.

By utilizing PySpark, I will efficiently extract, clean, and analyze large-scale datasets, like the complete history of Subreddits. This would be impractical with more traditional methods, such as using CSV files and Pandas. By leveraging its features, such as data distribution and workloads across multiple nodes, I will parallelize almost every aspect of my work, making the processing both scalable and feasible.


## Data Collection and Methods

### Data Collection

Following changes to the Reddit API in 2023, and the subsequent deprecation/inaccessibility of ‘Pushshift’, accessing the complete history of Subreddit has become infinitely more challenging. Fortunately, a Reddit, 'watchful1; has made torrent versions of the platform's history available. Leveraging qBittorrent, I gathered the complete submission and comment history from the conservative Subreddit dating from 2008 to 2023.

### Submission Data

Because the submission dataset was a relatively modest size (64 MB ZST, approximately 1 million data points), I used Google Colab to extract any submission containing the word ‘abortion’ in the title. My decision to use Colab for the smaller file stemmed from my lack of experience working with ZST files. I thought it would be better to familiarize myself with what the dataset contained before jumping into PySpark. However, I learned that the two environments were significantly different and that this approach presented more challenges than necessary.

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/posts_about_abortion.png" alt="Percentage of Posts With Abortion in The Title" width="600" />

After extracting the relevant posts from the dataset, I collected 10,372 submission posts. Despite the relatively small size, I still utilized the power of PySpark to perform data cleaning, Latent Dirichlet Allocation (LDA), bigram extraction, the creation of word clouds, and ultimately, to gather the ‘IDs’ of each submission. These ‘IDs’ played a crucial role in ensuring the accuracy of the extraction of corresponding comments.

#### Topics Extracted from LDA of Post Titles:

| Topic | Words |
|-------|---------------------------------------------------------------------------------------|
| 0     | [biden, proabortion, new, trump, catholic, joe, news, banned, administration, campaign] |
| 1     | [murder, rape, child, argument, pro, choice, change, prochoice, ny, good]               |
| 2     | [bill, support, birth, democrats, want, americans, house, vote, democrat, poll]         |
| 3     | [babies, people, killing, roe, like, lateterm, left, one, think, baby]                  |
| 4     | [black, die, baby, uk, business, syndrome, based, west, moral, race]                    |
| 5     | [planned, parenthood, women, laws, children, pregnant, clinics, governor, get, babies]  |
| 6     | [woman, democrats, kill, pay, travel, virginia, bill, kids, funding, story]             |
| 7     | [law, court, ban, texas, supreme, bill, state, new, states, gov]                        |
| 8     | [life, us, dems, gets, term, late, american, fight, obamacare, amendment]               |
| 9     | [prolife, proabortion, right, says, activists, group, antiabortion, life, clinic, women]|


### Word Clouds

I also used Word Clouds to visualize commonalities between submission titles, analyzing them by year to identify potential shifts in discourse. As illustrated in the word clouds, the major changes revolve around the key political figures of each year. This indicates that the submissions were largely politically oriented, which interestingly, is not a trend that the comments to these submissions seemed to follow.

<div style="display: flex; flex-wrap: wrap;">
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2013.png" alt="Word Cloud 2013" width="500"/>

  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2016.png" alt="Word Cloud 2016" width="500"/>

  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2018.png" alt="Word Cloud 2018" width="500"/>

  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2020.png" alt="Word Cloud 2020" width="500"/>

  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2022.png" alt="Word Cloud 2022" width="500"/>

  </div>
</div>

### Comment Data

Due to the substantial size of the comment data, which consisted of a 2GB ZST file, I opted to utilize PySpark for the extraction process, due to its parallelization and efficiency. Since the file was too large to open on my local machine, I uploaded it to an S3 bucket, making it accessible within my JupyterHub on an EMR cluster. Extracting the comments was by far the most difficult part of this project/

After reading the file into my environment as text data, I defined a schema and used PySpark’s from_json() function to parse the large-scale data. Following this, I matched this resulting data frame on ‘IDs’ with the ‘IDs’ mentioned in the submission section, resulting in a dataset of 206,756 comments and their corresponding data. Lastly, I wrote this dataset into a Parquet file and stored it in an S3 bucket for later use.

Like the submission data, I thoroughly cleaned the dataset using PySpark’s parallelization. This involved removing deleted comments, as well as comments that were too short, cleaning the textual data, and converting the time information from Unix timestamps (‘1640635686’) to readable representations (‘2022-08-24 15:45:39’). Lastly, I matched any 'null' time values (mistakes from the original file) with the corresponding ‘submission’ time (for estimations). This gave me a final dataset size of 142,924 comments

The utilization of PySpark was crucial for the extraction and the cleaning process due to the large dataset size, as it allowed for efficient parallel processing and handling of the data. The complexity and scale of the task underscored the importance of PySpark in achieving timely and accurate results, which would have been challenging, if not impossible (especially with the extraction) with traditional methods.

After cleaning, I again used PySpark to conduct a data analysis. Each Machine Learning/NLP task employed a pipeline to leverage scalability between the two datasets, work distribution, and consistency. A simplified example of one of my ML Pipelines:

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/pipelineexample.jpg" alt="Pipeline Example" width="500" />

Regarding the comment analysis, I used Yake Keyword Extraction and continued with LDA and Bigram models. Additionally, I performed a temporal topic analysis of the topic-specific activity over time.

#### Yake Keyword Extraction 

I used Yake Keyword Extraction to discern the common messages or themes throughout the corpus. Interestingly, there was a shift in 2022 where the top comments were pro-choice adjacent comments. This was a stark contrast to the previous years.

<div style="text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/Screenshot%202024-05-23%20at%208.07.12%E2%80%AFAM.png" alt="Top Posts of 2016 with YAKE extraction" width="800" />
</div>

<div style="text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/Screenshot%202024-05-23%20at%208.07.41%E2%80%AFAM.png" alt="Top Posts of 2016 with YAKE extraction" width="800" />
</div>

#### Bigram Analysis

To examine potential shifts in framing, topics, or language surrounding abortion, I analyzed the top bigrams by year. When setting the minimum occurrence to 15, I found 12,633 unique bigrams within the dataset. While the predominant bigrams remained relatively stable, the order in which they appeared varied, suggesting a unique emphasis on different aspects of discourse. Notably, the largest shift seems to be in 2022, where the bigrams appear to be focusing on the reasons someone might want (or need) an abortion, rather than skewing strictly pro-life as observed earlier. This aligns with what was seen in the top comment of 2022 in the keyword extraction, possibly suggesting a shift in discourse or attitudes.

<font size="2">
  
Top Bigrams in 2014 | Top Bigrams in 2016 | Top Bigrams in 2018 | Top Bigrams in 2020 | Top Bigrams in 2022 |
|----------------------|----------------------|----------------------|----------------------|----------------------|
| planned parenthood   | human life           | birth control       | birth control       | supreme court       |
| birth control        | birth control        | human life          | human life          | birth control       |
| human life           | supreme court        | right life          | planned parenthood  | roe wade            |
| human dna            | pro life             | roe wade            | dont want           | year old            |
| undocumented immi... | right life           | planned parenthood  | pro choice          | human life          |
| take care            | unborn child         | life begins        | roe wade            | rape incest         |
| abortion clinics     | human beings         | death penalty       | dont think          | federal government |
| right life           | roe wade             | unborn child        | supreme court       | get abortion        |
| gay marriage         | planned parenthood   | catholic church     | pro life            | sounds like         |
| late term            | late term            | pro life         | life begins        | get pregnant         |


</font>

#### Temporal Analysis

I also performed Latent Dirichlet Allocation on the comment corpus. By using PySpark, I processed the dataset of 143,000 comments upwards of 200 times (to stabilize the results) in approximately a minute. This level of efficiency would have been unattainable with traditional methods.

I also took the Latent Dirichlet Allocation a step further, and analyzed the activity of each topic over time, once again using the power of PySpark's distributed processing.

Topic 11 suggests a shift from overwhelming pro-life rhetoric, as observed in the earlier analysis.

**Topic 2 Keywords: states, state, law, right, government, laws, court, roe, rights, issue**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic_2.png" alt="Temporal Analysis (Topic 2)" width="700" />

**Topic 3 Keywords: read, bill, link\*, ban, article, support, first, even, didnt, said**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic3.png" alt="Temporal Analysis (Topic 3)" width="700" />

**Topic 4 Keywords: shit, going, thats, hes, pro, trump, choice, fucking, guy, got**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic4.png" alt="Temporal Analysis (Topic 4)" width="700" />

**Topic 11 Keywords: life, human, murder, person, argument, fetus, right, people, killing, believe**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic11.png" alt="Temporal Analysis (Topic 11)" width="700" />

*Note: The term "link" was used during regex to replace links being shared. This indicates that many links are being shared within this topic.
<br>
** The complete visualizations for every analysis/year are available within the PySpark notebooks, I just chose the most interesting or representative ones to display here

## Limitations

Although I conducted a comprehensive analysis, this project is not without limitations. First, the data collection relied on a third party, meaning that there was no way for me to fully verify its completeness. Although the creator intended to capture the full history of the Subreddit, some data may be missing. 

Second, I only allowed for submissions and their respective comments with the word ‘abortion’ in the title. To have a more complete analysis, next time I will allow for other keywords in the abortion argument such as ‘Pro-Life’, ‘Pro-Choice’, ‘Roe v Wade’, ‘Dobbs v Jackson’, ext. Broadening the scope of submission titles and keywords will allow for a much more comprehensive analysis and understanding.

Further, although LDA offered a general overview of themes, the model, with its bag-of-words method, likely struggled to capture the complexity within the text data, primarily in longer-form comments. To address this, I plan to explore the use of sentence embeddings and transformers in future research. 

Lastly, although I conducted a thorough cleaning of both submissions and comments, the volume (of comments in particular) was far too large to ensure complete accuracy. Irrelevant data may be still present within the corpus.

## Conclusion
Overall, the project showcases the power and effectiveness of using PySpark for large-scale data analysis. As mentioned several times, the majority of this project would not have been possible without the capabilities of parallel processing and distribution granted by PySpark and the features within it. 

Through this analysis, I have observed frequent shifts in abortion discourse on an annual basis, which appears to be related to changes in significant political figures and events. However, a more noteworthy trend appeared within the bigram and temporal topic analysis. These results suggest a slight shift from a previously overwhelming 'Pro-Life' rhetoric. Although it is important to emphasize that these results warrant further investigation before drawing any conclusions, these findings offer valuable insights into the potential evolution of abortion discourse and attitudes.

Throughout this project, I have become increasingly comfortable with PySpark, and I am excited about continuing this research and delving deeper into the evolution of abortion attitudes and discourse. Additionally, I plan to expand my research beyond the Conservative Subreddit and include other communities with ideological differences. By doing so, I hope to broaden our understanding of online abortion discourse and contribute valuable insights to the ongoing conversations surrounding abortion attitudes and the implications they have on our society.

## Navigating this Repo

### Code Folder:

- **zst_submission_extract.ipynb**: Code for extracting submissions from a ZST file.
  
- **fix_csv.ipynb**: Code for fixing CSV files to ensure an accurate transfer to PySpark DataFrame.
  
- **eda_lda_posts.ipynb**: Cleaning, EDA, and NLP of submission data.
  
- **fixed_wordclouds.ipynb**: Word clouds of submission titles.
  
- **zst_comment_extract.ipynb**: Code for extracting comments from a 2GB ZST file.
  
- **EDA_comments.ipynb**: Cleaning and EDA of extracted comments.
  
- **NLP_comments_clean.ipynb**: Analysis and NLP of comments.
- **requirements.txt**: list of requirements

### Emr_Scripts Folder:
- **emrlaunch.py**: Used to launch cluster, install more packages
- **setup.sh**: Used to setup necessary packages on the cluster (code from Spark NLP - Installation, 2023)
- **sparknlp-config.json**: Used to configure NLP (code from Spark NLP - Installation, 2023)

### visualizations Folder:
- Contains PNG images of plots extracted from notebooks for this readme.


## Work and Resources Cited

- JohnSnowLabs. (n.d.). Keyword_Extraction_YAKE.ipynb. Retrieved from [https://github.com/JohnSnowLabs/spark-nlp/blob/master/examples/python/annotation/text/english/keyword-extraction/Keyword_Extraction_YAKE.ipynb](https://github.com/JohnSnowLabs/spark-nlp/blob/master/examples/python/annotation/text/english/keyword-extraction/Keyword_Extraction_YAKE.ipynb)

- L, S. (2024, February 18). Tutorial: Feature engineering for Time series Forecasting in PySpark. *Medium*. [https://medium.com/@soyoungluna/tutorial-feature-engineering-for-weekly-time-series-forecasting-in-pyspark-b207c41869f4](https://medium.com/@soyoungluna/tutorial-feature-engineering-for-weekly-time-series-forecasting-in-pyspark-b207c41869f4)

- Mulvihill, G., & Kruesi, K. (2024, April 10). Which states could have abortion on the ballot in 2024? | AP News. *AP News*. [https://apnews.com/article/abortion-ballot-amendment-ban-protection-states-2024-052ff9846f8416efb725240af22b92ec](https://apnews.com/article/abortion-ballot-amendment-ban-protection-states-2024-052ff9846f8416efb725240af22b92ec)

- Obedkova, M. (2021, December 14). Topic Modelling with PySpark and Spark NLP - TrustYou Engineering - *Medium*. [https://medium.com/trustyou-engineering/topic-modelling-with-pyspark-and-spark-nlp-a99d063f1a6e](https://medium.com/trustyou-engineering/topic-modelling-with-pyspark-and-spark-nlp-a99d063f1a6e)

- State bans on abortion throughout pregnancy. (2024, May 2). *Guttmacher Institute*. [https://www.guttmacher.org/state-policy/explore/state-policies-abortion-bans](https://www.guttmacher.org/state-policy/explore/state-policies-abortion-bans)

- Spark NLP - installation. (2023, May 10). https://sparknlp.org/docs/en/install
    
- Watchful1. (n.d). Subreddit comments/submissions 2005-06 to 2023-12. [https://academictorrents.com/details/56aa49f9653ba545f48df2e33679f014d2829c10](https://academictorrents.com/details/56aa49f9653ba545f48df2e33679f014d2829c10)

- Watchful1. (n.d.). PushshiftDumps/scripts/single_file.py at master · Watchful1/PushshiftDumps. *GitHub*. [https://github.com/Watchful1/PushshiftDumps/blob/master/scripts/single_file.py](https://github.com/Watchful1/PushshiftDumps/blob/master/scripts/single_file.py)


**AI Narrative**
- [Asking how to make LDA more efficient](https://chatgpt.com/share/0dccc45f-afc9-490b-ab8e-75cd34a088c8)
- [Time series plot help](https://chatgpt.com/share/f1c73b56-07d3-4855-b42b-d045a3ec724b)
- [Livy server help](https://chatgpt.com/share/eec2f8bc-105c-4a13-b9eb-2c637cf79511)
- [UDF/parallelization help](https://chatgpt.com/share/a312ca01-99f9-4a9d-90ff-1af52cd178fe)
- [Beginning to work with ZST in PySpark](https://chatgpt.com/share/3336cb32-3990-4b85-9a4c-6d9da208fe76)
