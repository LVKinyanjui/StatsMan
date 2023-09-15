import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer


#------------------------------------------------------------------------------------------------------------------------
# FUNCTION DEFINITION
def read_in(directory='data/'):
    file_name = input("File to analyze : ")
    full_path = directory + file_name + '.csv'

    text_df = pd.read_csv(full_path)
    try:
        texts = str(list(text_df['text']))
    except:
        print("Problem with file. File must be a csvwith a column header named 'text'")

    string = '.'.join(texts)
    return texts, string, file_name

def robust_tokenize(texts):
    if type(texts) == str:
        return word_tokenize(texts)
        
    elif type(texts) == list:
        tokens = [word_tokenize(text) for text in texts]
        return [item for sublist in tokens for item in sublist]
    
    else:
        print('texts not a list or string')

# Extracting all Named Entities without repeat.
def extract_entities(string):
    
    """
    string : Literally a string with the text to analyze
    """
    # chats_str = '.'.join(chats)
    tokens = word_tokenize(string)
    tags = nltk.pos_tag(tokens)
    
    tree = nltk.ne_chunk(tags, binary=True)
    return set(
     " ".join(i[0] for i in t)
     for t in tree
     if hasattr(t, "label") and t.label() == "NE"
)

# General sentiment of entire corpus
def agg_sentiment(string, file_name):
    """
    Plots a graph of the average sentiment in a string provided.
    """
    path=f"I:/My Drive/My Apps/Python Scripts/data/plots/{file_name}.pdf"
    
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(string)

    scores_df = pd.DataFrame(scores, index=['scores'])
    scores_df = scores_df.transpose().reset_index()

    sns.barplot(data=scores_df, x='index', y='scores')
    plt.title(file_name)
    plt.xlabel('sentiment')
    plt.savefig(path, format='pdf')
    plt.show()

    
# Sentiment for each Named Entity
def agg_sentiments(entities, texts, file_name, directory='data/'):
    """
    Plots a graph of the average sentiment for a list of entities
    
    ------------------------------------------------------------------------
    entities : list-like, the entities whose sentiment to plot
    texts : string, tokenized, from which entities are drawn
    
    ------------------------------------------------------------------------
    Returns : None
    """
    text = nltk.Text(texts)
    entity_list = [text.concordance_list(entity) for entity in list(entities)]
    
    sia = SentimentIntensityAnalyzer()
    
    # create a PdfPages object to save the plots in a PDF file
    full_path = directory + file_name + '_entities.pdf'
    pdf_pages = PdfPages(full_path)
    
    for index, entity in enumerate(entity_list):
        if len(entity) != 0:
            string = entity_list[index][0].line

            scores = sia.polarity_scores(string)

            scores_df = pd.DataFrame(scores, index=['scores'])
            scores_df = scores_df.transpose().reset_index()
            

            # create your plots using Matplotlib
            # Create a Figure object
            fig = plt.figure()

            ax1 = fig.add_subplot()  # Subplot at position 1
            sns.barplot(data=scores_df, x='index', y='scores', ax=ax1)
            ax1.set_title(list(entities)[index])
            
            #ax2 = fig.add_subplot(2, 1, 2)  # Subplot at position 2
            #text.dispersion_plot(list(entities))
            
            # save each plot to the pdf file
            pdf_pages.savefig(fig)

    # close the pdf file
    pdf_pages.close()

#------------------------------------------------------------------------------------------------------------------------
# FUNCTION CALLS
texts, string, file_name = read_in()
tokens = robust_tokenize(texts)
named_entities = extract_entities(string)
# agg_sentiment(string, file_name)
agg_sentiments(named_entities, tokens, file_name)