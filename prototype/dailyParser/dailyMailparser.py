import requests
from bs4 import BeautifulSoup


class DailyMailParser:
    def __init__(self):
        self.soup = None

    def openDoc(self, filepath):
        """
        Open an html file and form a beautiful soup object of it
        """
        with open(filepath, 'r') as f:
            htmlData = f.read()
        self.soup = BeautifulSoup(htmlData, 'html.parser')        

    def openURL(self, url):
        """
        Open an html from url and for beautiful soup object of it
        """
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def findFacets(self):
        """
        Find all the human written bullet points, which can be used
        as rouge facets. Method returns list of facets
        """
        facets = []
        content = self.soup.find(id='page-container')
        text = content.find(id='js-article-text')
        for facet in text.find('ul', {"class":"mol-bullets-with-font"}):
            facet.text.replace("\xa0", " ")
            facets.append(facet.text)
        return facets

    def findContent(self):
        """
        Find the article and form a string object of it
        """
        article = ""
        content = self.soup.find(id='page-container')
        text = content.find(id='js-article-text')
        for para in text.find_all('p', {'class':'mol-para-with-font'}):
            para.text.replace("\xa0", " ")
            article += " "+para.text
        return article


