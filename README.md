# Large Scale Analysis: Conservative Abortion Discourse

## Introduction

Abortion remains a contentious and deeply entrenched debate in America and American politics. Despite its apparent legal solidity following the landmark case **Roe v. Wade** in 1973, which guaranteed the constitutional right to privacy – including the right to an abortion – this framework was dramatically altered in the unprecedented ruling of **Dobbs v. Jackson Women’s Health Organization** in 2022. This decision effectively overturned Roe v. Wade and returned the power of regulating abortion back to the states.

Following the Dobbs ruling, the legality of abortion in America has become fragmented, with over fourteen states enacting all-out abortion bans and an additional seven implementing laws severely restricting abortion ([Where Can I Get an Abortion?](#), n.d.). Furthermore, the issue has emerged as a focal point in the upcoming 2024 election, where abortion is expected to be a battleground issue. In over eleven states, voters will weigh in on addressing measures surrounding abortion (Mulvihill and Kruesi, 2024). Against this unparalleled legal upheaval, political turmoil, and the continued erosion of established rights, research into the discourse surrounding the topic becomes even more imperative.


## Objective

In light of this climate, my final project presented here aims to conduct a large-scale analysis using Reddit, a social media platform known for its unique features like pseudonymity and topical division of ‘Subreddits.’ These attributes not only distinguish Reddit as a platform but present a compelling opportunity for research, potentially fostering more candid and open discussions.
Specifically, I will be examining discourse surrounding abortion within the r/Conservative Subreddit. I have chosen this Subreddit for several reasons:

1. The Subreddit has over 1 million users, making it a prominent platform within Reddit.
2. Preliminary research (limited to 1000 posts via the Reddit API) revealed significant activity surrounding abortion discourse within the Subreddit.
3. The persistent reaction and stances of Conservative politicians regarding abortion underscore the significance of the topic within the party, often becoming a focal point of their political identity.

This emphasis placed on abortion within Conservative circles makes r/Conservative a pivotal place for my intended research.

By utilizing PySpark, I can efficiently extract, clean, and analyze large-scale datasets, like the complete history of Subreddits. This would be impractical with more traditional methods, such as using CSV files and Pandas. By leveraging PySpark's features, such as the distribution of data and workloads across multiple nodes, I will be parallelizing almost every aspect of my work, making the processing both scalable and feasible.


## Data Collection and Methods

### Data Collection

Following changes to the Reddit API in 2023, and the subsequent deprecation/inaccessibility of ‘Pushshift’, accessing the complete history of Subreddit has become infinitely more challenging. Fortunately, a Reddit user known as watchful1 has made torrent versions of the history of the platform available. Leveraging qBittorrent, I was able to gather the complete submission and comment history from the conservative Subreddit, ranging from 2008 to 2023.

### Submission Data

Because the submission dataset was a relatively modest size (64 MB ZST, 1 million data points), I was able to use Google Colab to extract any submission that had the word ‘abortion’ in the title. My decision to use Colab for the smaller of the two files mainly stemmed from the fact that I lacked any prior experience working with ZST files. I thought that it would be better to familiarize myself with what the dataset contained before jumping into PySpark. However, I learned later that the two environments were significantly different, and that this approach ultimately presented more challenges than necessary.

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/posts_about_abortion.png" alt="Percentage of Posts With Abortion in The Title" width="600" />

After extracting the relevant posts from the dataset, I amassed a total of 10,372 submission posts. Despite the relatively small size, I still utilized the power of PySpark to perform data cleaning, Latent Dirichlet Allocation (LDA), bigram extraction, the creation of word clouds, and ultimately, to gather the ‘IDs’ of each submission. These ‘IDs’ played a crucial role in ensuring the accuracy of the extraction of corresponding comments.

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

I used Word Clouds to visualize commonalities between submission titles, analyzing them by year to possibly identify and major shifts in discourse. As illustrated in the word clouds, the major changes revolve around the key political figures of each year. This indicates that the submissions were largely politically oriented, which interestingly enough, is not a trend that the comments to these submissions seemed to follow.

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

Due to the substantial size of the comment data, which consisted of a 2GB ZST file, I opted to utilize PySpark for the extraction process, due to its parallelization and efficiency. As the file was much too large to open on my local machine, I uploaded the file to an S3 bucket, where I could access it within my JupyterHub on an EMR cluster.

After reading in the file as text data, I defined a schema and used PySpark’s from_json() function to parse the large-scale data. Following this, I matched this resulting data frame on ‘IDs’ with the ‘IDs’ mentioned in the submission section, resulting in a dataset of 206,756 comments and their corresponding data. Lastly, I wrote this dataset into a Parquet file and stored it in an S3 bucket for later use.

Similar to the submission data, I performed a thorough cleaning of the dataset, utilizing PySpark’s parallelization. This involved removing deleted comments, as well as comments that were too short, cleaning the textual data, and converting the time information from Unix timestamps (‘1640635686’) to readable representations (‘2022-08-24 15:45:39’). Lastly, I matched any of the ‘null’ time values (mistakes from the original file) with the corresponding ‘submission’ time, providing a general estimation of when the comment was made. This gave me a final dataset size of 142,924 comments. 

The utilization of PySpark was crucial for both the extraction and the cleaning process due to the large dataset size, as it allowed for efficient parallel processing and handling of the data. The complexity and scale of the task underscored the importance of PySpark in achieving timely and accurate results, which would have been challenging, if not impossible (especially with the extraction) with traditional methods.

After cleaning, I again used PySpark to conduct a data analysis. For each Machine Learning/NLP task, I utilized a pipeline to take advantage of scalability between the two datasets, work distribution, and consistency. A simplified example of one of my ML Pipelines:

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/pipelineexample.jpg" alt="Pipeline Example" width="500" />

For an analysis of the comments, I used Yake Keyword Extraction and continued the use of both LDA and Bigram. Additionally, I performed a temporal topic analysis of the topic-specific activity over time.

#### Yake Keyword Extraction 

I used Yake Keyword Extraction to discern the common messages or themes throughout the corpus. Interestingly, there was a shift in 2022 where the majority of top comments were pro-choice adjacent comments. This was a stark contrast to the previous years.

<div style="text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/Screenshot%202024-05-23%20at%208.07.12%E2%80%AFAM.png" alt="Top Posts of 2016 with YAKE extraction" width="800" />
</div>

<div style="text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/Screenshot%202024-05-23%20at%208.07.41%E2%80%AFAM.png" alt="Top Posts of 2016 with YAKE extraction" width="800" />
</div>

#### Bigram Analysis

To examine potential shifts in framing, topics, or language surrounding abortion, I analyzed the top bigrams by year. When setting the minimum occurrence to 15, I found that there were 12,633 unique bigrams within the dataset. While the predominant bigrams remained relatively stable, the order in which they appeared varied, suggesting a unique emphasis on different aspects of discourse. Notably, the largest shift seems to be in 2022, where the bigrams appear to be focusing on the reasons someone might want (or need) an abortion, rather than skewing strictly pro-life as observed earlier. This aligns with what was seen in the top comment of 2022 in the keyword extraction, possibly suggesting a shift in discourse or attitudes.

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

I also performed Latent Dirichlet Allocation on the comment corpus. PySpark was instrumental in being able to do this. By utilizing PySpark, I was able to run through the dataset of approximately 140,000 comments upwards of 200 times (to get the results to stabilize) in a matter of seconds. This would have taken a much longer time using traditional methods.

I also took the Latent Dirichlet Allocation a step further, and analyzed the activity of each topic over time, once again using the power of PySpark's distributed processing.

Topic 11 once again suggests a shift away from an overwhelming pro-life rhetoric, as observed in the earlier analysis.

**Topic 2 Keywords: states, state, law, right, government, laws, court, roe, rights, issue**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic_2.png" alt="Temporal Analysis (Topic 2)" width="700" />

**Topic 3 Keywords: read, bill, link\*, ban, article, support, first, even, didnt, said**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic3.png" alt="Temporal Analysis (Topic 3)" width="700" />

**Topic 4 Keywords: shit, going, thats, hes, pro, trump, choice, fucking, guy, got**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic4.png" alt="Temporal Analysis (Topic 4)" width="700" />

**Topic 11 Keywords: life, human, murder, person, argument, fetus, right, people, killing, believe**

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/topic11.png" alt="Temporal Analysis (Topic 11)" width="700" />

*Note: The term "link" was used during regex to replace links being shared. This indicates that many links are being shared within this topic.
** The complete visualizations for every analysis/year are available within the PySpark notebooks, I just chose the most interesting or representative ones to display here


