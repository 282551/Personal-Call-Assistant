import spacy
import nltk
from nltk.corpus import stopwords
import marisa_trie



nlp_en=spacy.load(r"C:\Users\Thierrynell\PycharmProjects\pythonProject1\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.2.0")


#thesaurus = ['Gestion de projet','machine learning','gestion de l''accueil','Python','Nlp','Réglage des machines']
#stopwords = ['le','la','les','l',"'",'de','du','des','et','en']
stopwords = [',','.','ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

#thesauru = ['Gestion de projet','machine learning','gestion de l''accueil','Python','Nlp','Réglage des machines']


def pre_process(txt):
    #tokens=[tok.lemma_ for tok in nlp_en(txt)]
    tokens = nltk.word_tokenize(txt)
    tokens=[tok.lower() for tok in tokens if tok.lower() not in stopwords]
    return tokens




def find_keywords(sentence,thesaurus):
    pre_processed_thesaurus = ["".join(pre_process(skill)) for skill in thesaurus] #préprocessing Thésaurus
    thesaurus_trie = marisa_trie.Trie(pre_processed_thesaurus)  #load thesaurus into marisa trie
    tokens=pre_process(sentence) #preprocessing sentence
    keywords=[]
    i=0
    current_expression=[]
    while i< len(tokens):
        current_expression.append(tokens[i])
        if len(thesaurus_trie.keys("".join(current_expression)))==0:
            i+=1
            current_expression=[]
        elif "".join(current_expression) in thesaurus_trie:
            keywords.append(" ".join(current_expression))
            i+= len(current_expression)
            current_expression=[]
        else:
            i+=1
    return keywords

#print(find_keywords("des expériences sur des projets mélant du Nlp et du machine learning sont un plus",thesauru))




