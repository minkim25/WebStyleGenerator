<ul><li><b>Problem definition:</b> What is the problem that you are trying to solve? 

    We will solve the age-old problem of deciding your website/blog's style for you. 
    There's an infinite combination of different colours and fonts to choose from. 
    What combination of colours and fonts would best define your personality? 
    It's impossible to decide! You don't need that stress in your life. 
    Let our tool figure it out for you.
    All that you need to worry about is producing good content. 
    Type a few typical sentences that would be on your website. 


What are the challenges of this problem?

    Scraping content from a website sequentially is a slow task because you want to set a timer in order to have the website not block your IP address.
    So the self-imposed timer will often be the main bottle-neck.

    However, given a list of websites and access to a cluster with many nodes, we can have them divide and conquer the list of websites to scrape, each with their self-imposed timer.
	<something frontend> (!!!)

</li><li><b>Methodology:</b> Briefly explain which tool(s)/technique(s) were used for which task and why you chose to implement that way.

    - Cassandra: 
		- It was available on the cluster.
		- Originally we were testing a distributed method of crawling websites, and hypothesized that cassandra-spark integration would be good for parallel inserts.
	- Flask
		- The cached word corpus similarity functions were native to python, and so building a website using a python framework would be good.
		- A good opportunity to learn an employable skill.
	- Spark
		1. Web scraping in parallel would help make the task shorter via the divide-and-conquer approach.
	- Pandas
		1. Easy to use.
	- Gensim
		1. This contained good pre-packaged natural language functions for us to use.
	- BeautifulSoup4
		1. Web-scraping.
	- NLTK
		1. Other natural language tasks.
	- Word2Vec
		1. Word embeddings allowed us to calculate semantic similarity between different websites. 

</li><li><b>Problems:</b> What problems did you encounter while attacking the problem? 

    - Messy websites, with different structured ways of representing style-sheets.
	- It was also difficult to seperate out the useful text from the javascript-related text.
	- Parsing some websites could take up to many seconds.
	- Tumblr API had limits in the number of hits per hour and per day.
	- Amazon had limitations in the number of request (but we still ended up with 100k websites).

How did you solve them?

    - Specifying all the rules of CSS representation.
	- Specifying a custom stop-word list.
	- Running in parallel + patience
	- Running multiple times each day
	- Running multiple times

</li><li><b>Results:</b> What are the outcomes of the project? 

    - Website that generates style recommendations based on the input text
	- Fascinating dataset
	- Analysis opportunities

What did you learn from the data analysis? 

    - There are clusters of colours that are typically unused for websites
	- Primary and greyscale colours are popular choices for websites
	- Tumblr blogs also use pastel/greyscale

What did you learn from the implementation?

    - Web scraping is difficult.
	- Parallelization of tasks sometimes can be faster by just spawning different threads rather than using Spark
	- Flask
	- 

</li><li><b>Project Summary:</b> A summary of what you did to guide our marking.

    At the end of your project report, please provide a summary of the emphasis/priorities in your project. 
	Give yourself a total of 20 point in these categories:

    Getting the data: Acquiring/gathering/downloading. 4
	
    ETL: Extract-Transform-Load work and cleaning the data set. 4
    
	Problem: Work on defining problem itself and motivation for the analysis. 1
    
	Algorithmic work: Work on the algorithms needed to work with the data, including integrating data mining and machine learning techniques. 2
    
	Bigness/parallelization: Efficiency of the analysis on a cluster, and scalability to larger data sets. 1
    
	UI: User interface to the results, possibly including web or data exploration frontends. 4
    
	Visualization: Visualization of analysis results. 2
    
	Technologies: New technologies learned as part of doing the project. 2

	Total: 20

	Don't think of this as giving yourself a mark. (That's our job.) This is intended to be a guide for our marking, so we don't miss significant work you did. (e.g. if you give yourself 6 points on “new technologies” and we haven't noticed any, we know to keep looking; if you gave yourself 0 then we can move on and look at other aspects.)

	Since this will be guiding our marking, you may want to address these areas in your report as well.

	You will likely be giving yourself 0 in some of these categories: that's perfectly reasonable. You aren't expected to do all of these, but should (of course) have done some subset of them (including “bigness” which we expect you to think about).

	[If there are other categories you think should be here, ask us.]

</li></ul>