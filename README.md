# Large Scale Analysis: Conservative Abortion Discourse

## Introduction

Abortion remains a contentious and deeply entrenched debate in America and American politics. Despite its apparent legal solidity following the landmark case **Roe v. Wade** in 1973, which guaranteed the constitutional right to privacy – including the right to an abortion – this framework was dramatically altered in the unprecedented ruling of **Dobbs v. Jackson Women’s Health Organization** in 2022. This decision effectively overturned Roe v. Wade and returned the power of regulating abortion back to the states.

Following the Dobbs ruling, the legality of abortion in America has become fragmented, with over fourteen states enacting all-out abortion bans and an additional seven implementing laws severely restricting abortion ([Where Can I Get an Abortion?](#), n.d.). Furthermore, the issue has emerged as a focal point in the upcoming 2024 election, where abortion is expected to be a battleground issue. In over eleven states, voters will weigh in on addressing measures surrounding abortion (Mulvihill and Kruesi, 2024). Against this unparalleled legal upheaval, political turmoil, and continued erosion of established rights, research into the discourse surrounding the topic becomes even more imperative.


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

<img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/posts_about_abortion.png" alt="Percentage of Posts With Abortion in The Title" width="700" />

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

<div style="display: flex; flex-wrap: wrap;">
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2013.png" alt="Word Cloud 2013" width="150"/>
    <p>2013</p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2016.png" alt="Word Cloud 2016" width="150"/>
    <p>2016</p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2018.png" alt="Word Cloud 2018" width="150"/>
    <p>2018</p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2020.png" alt="Word Cloud 2020" width="150"/>
    <p>2020</p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/macs30123-s24/final-project-online_abortion_discourse/blob/main/visualizations/wc_2022.png" alt="Word Cloud 2022" width="150"/>
    <p>2022</p>
  </div>
</div>

### Comment Data

Due to the substantial size of the comment data, which consisted of a 2GB ZST file, I opted to utilize PySpark for the extraction process, due to its parallelization and efficiency. As the file was much too large to open on my local machine, I uploaded the file to an S3 bucket, where I could access it within my JupyterHub on an EMR cluster.

After reading in the file as text data, I defined a schema and used PySpark’s from_json() function to parse the large-scale data. Following this, I matched this resulting data frame on ‘IDs’ with the ‘IDs’ mentioned in the submission section, resulting in a dataset of 206,756 comments and their corresponding data. Lastly, I wrote this dataset into a Parquet file and stored it in an S3 bucket for later use.

Similar to the submission data, I performed a thorough cleaning of the dataset, utilizing PySpark’s parallelization. This involved removing deleted comments, as well as comments that were too short, cleaning the textual data, and converting the time information from Unix timestamps (‘1640635686’) to readable representations (‘2022-08-24 15:45:39’). Lastly, I matched any of the ‘null’ time values (mistakes from the original file) with the corresponding ‘submission’ time, providing a general estimation of when the comment was made. This gave me a final dataset size of 142,924 comments. 

The utilization of PySpark was crucial for both the extraction and the cleaning process due to the large dataset size, as it allowed for efficient parallel processing and handling of the data. The complexity and scale of the task underscored the importance of PySpark in achieving timely and accurate results, which would have been challenging, if not impossible (especially with the extraction) with traditional methods.

Following the cleaning process, I again utilized PySpark to conduct a data analysis. This time, I used Yake Keyword Extraction as well as continued my use of LDA and Bigram. Additionally, I performed a temporal topic analysis of the topics over time.
