# coding:utf-8
from gensim import corpora, models

# load corpus and dictionaries
corpus_titles = corpora.MmCorpus('Model/corpus_titles')
corpus_contents = corpora.MmCorpus('Model/corpus_contents')

dictionary_titles = corpora.Dictionary.load('Model/dict_titles')
dictionary_contents = corpora.Dictionary.load('Model/dict_contents')

# build tfidf model
tfidf_title = models.TfidfModel(corpus_titles)
tfidf_content = models.TfidfModel(corpus_contents)

# save tfidf model
tfidf_title.save('Model/tfidf_title.model')
tfidf_content.save('Model/tfidf_content.model')

# TF-IDF transformation
corpus_titles_tfidf = tfidf_title[corpus_titles]
corpus_contents_tfidf = tfidf_content[corpus_contents]

# build LDA model
lda_content = models.LdaModel(corpus_contents_tfidf, id2word=dictionary_contents, num_topics=50)
lda_title = models.LdaModel(corpus_titles_tfidf, id2word=dictionary_titles, num_topics=20)

# save LDA model
lda_content.save('Model/lda_content.model')
lda_title.save('Model/lda_title.model')

