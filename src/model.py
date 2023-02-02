import twint
import nest_asyncio
import pandas as pd
import numpy as np
import nltk
import matplotlib as mpl
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from io import BytesIO
from . import utils

class Model():
    stemmer = StemmerFactory().create_stemmer()
    swords = stopwords.words('indonesian')
    lex_pos = utils.tsv2dict("/org/gnome/Example/pos.tsv")
    lex_neg = utils.tsv2dict("/org/gnome/Example/neg.tsv")
    conf = twint.Config()
    df = None

    def __init__(self):
        self.conf.Lang = "id"
        self.conf.Pandas = True
        self.conf.Pandas_clean = True
        self.conf.Limit = 250
        self.conf.Hide_output = True

        nest_asyncio.apply()
        mpl.use('Agg')
        plt.style.use('fivethirtyeight')

        df_swords = pd.read_csv(
          utils.get_bytes("/org/gnome/Example/sword.csv"), names=["Stopword"])

        self.swords.extend(df_swords["Stopword"])
        self.swords.extend(stopwords.words('english'))

        self.swords = set(self.swords)
        pd.options.mode.chained_assignment = None

    def bersih(self, teks):
      return ' '.join([w for w in teks.split() if not w in self.swords])

    def sentimize(self, text):
        score = 0

        for word in text.split():
            if (word in self.lex_pos):
                score += self.lex_pos[word]

            if (word in self.lex_neg):
                score += self.lex_neg[word]

        return score

    def labelize(self, score):
      if score > 2:
        return "Positif"
      elif score < -2:
        return "Negatif"
      else:
        return "Netral"

    def pie(self):
      if self.df is None:
        raise Exception("Analisis topik dulu")

      with BytesIO() as buf:
        vc = self.df['label'].value_counts()

        plt.figure(figsize=(4.25, 4.25))
        plt.pie(vc.values, labels = vc.index, autopct='%1.1f%%')
        plt.savefig(buf, format='png', transparent=True, dpi=100)

        return utils.buf2imgarray(buf)

    def wordcloud(self, label, lex, colormap):
      if self.df is None:
        raise Exception("Analisis topik dulu")

      kalimat = self.df.loc[self.df["label"] == label]["bersih"].str.cat(sep=' ')
      c = Counter([x for x in kalimat.split() if x in lex and abs(lex[x]) > 2])

      for x in c.copy():
        c[x] = np.cbrt(c[x]) * np.cbrt(abs(lex[x])) + np.sqrt(abs(lex[x]))

      return WordCloud(width = 480, height = 480,
                background_color = None, mode = "RGBA",
                colormap = colormap).generate_from_frequencies(c).to_array()

    def wordcloud_pos(self):
        return self.wordcloud("Positif", self.lex_pos, "winter")

    def wordcloud_neg(self):
        return self.wordcloud("Negatif", self.lex_neg, "autumn")

    def analisis(self, topik):
      self.conf.Search = topik

      twint.run.Search(self.conf)

      self.df = twint.storage.panda.Tweets_df[["tweet"]]

      self.df["bersih"] = self.df["tweet"].str.replace(
        "^[Rr][Tt]|[\w\.\/\-\=\?]*@\w+:?|https?:?\/?\/?|[\w\.\/\-\=\?]+\.[\w\.\/\-\=\?]+",
        "", regex=True)
      self.df["bersih"] = self.df["bersih"].str.lower().str.replace("[^a-zA-Z]", " ", regex=True)
      self.df["bersih"] = self.df["bersih"].apply(self.stemmer.stem)
      self.df["bersih"] = self.df["bersih"].apply(self.bersih)

      self.df["skor"] = self.df['bersih'].apply(self.sentimize)
      self.df["label"] = self.df["skor"].apply(self.labelize)
