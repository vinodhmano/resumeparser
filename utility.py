# General Imports
import pandas as pd

# to extract list of programming lanugages from wiki
import urllib.request
from bs4 import BeautifulSoup

# to convert docx to text
import docx2txt
from nltk.corpus import stopwords
import PyPDF2 


def get_prgm_list_from_wiki():
    prgm_lang_list = list()
    # fetch all the programming language names from wikipedia
    wiki = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
    page = urllib.request.urlopen(wiki)
    soup = BeautifulSoup(page, features='html.parser')
    prgm_lang_list_divs = soup.find_all(class_='div-col columns column-width')

    for divs in range(1, len(prgm_lang_list_divs)):
        for link in prgm_lang_list_divs[divs].find_all('a'):
            prgm_lang_list.append(str(link.text).strip())

    return prgm_lang_list


def get_adb_software_list_from_wiki():
    wiki = "https://en.wikipedia.org/wiki/List_of_Adobe_software"
    page = urllib.request.urlopen(wiki)
    soup = BeautifulSoup(page, features='html.parser')
    table_data = soup.find(class_="wikitable")
    links = table_data.find_all('a')
    products = [link.text.strip() for link in links]
    return products


def get_prgm_lang_list():
    # Create a list of programs
    # empty list which will contain all programming language names

    """TODO : get list from the following
    https://en.wikipedia.org/wiki/List_of_Adobe_software
    https://en.wikipedia.org/wiki/List_of_Microsoft_software
    https://en.wikipedia.org/wiki/Integrated_development_environment
    https://en.wikipedia.org/wiki/List_of_Macintosh_software

    """
    try:
        master_list_df = pd.read_csv('programming_languages_list.csv')
        return list(master_list_df['Language Name'])
    except OSError:
        master_list = list()
        master_list.extend(get_prgm_list_from_wiki())
        master_list.extend(get_adb_software_list_from_wiki())
        master_list = [skill.strip().lower() for skill in master_list]

        # save it to a csv file so that we can load it faster
        (pd.Series(master_list)
         .to_csv('programming_languages_list.csv', header=['Language Name'], index=False))

        return master_list


# create the corpus of words from the resumes
def get_stop_words():
    stop_words = set(stopwords.words("english"))
    custome_words = ['test', 'case', 'testing', 'using', 'data', 'system', 'tool', 'technology', 'service',
                     'team', 'customer', 'experience', 'worked', '1', 'client', 'application',
                     'technical', 'review', 'role', 'software', 'tool', 'management', 'pune', 'solution',
                     'service', 'engineer', 'cognizant', 'com', 'completed', 'case', 'requirement',
                     'offshore', 'science', 'ltd', 'certified', 'lead', 'page', 'comcast',
                     'project', 'functional', 'defect', 'regression', 'content', 'execution']
    stop_words = stop_words.union(custome_words)
    return stop_words

def extract_pdfToText_from_file(pdfPath):
    # author : Balamurugan R
    page_content = ""
    # creating a pdf file object 
    pdfFileObj = open(pdfPath, 'rb') 
    
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
    # printing number of pages in pdf file 
    #print(pdfReader.numPages) 

    # extracting text from page all pages of the PDF
    for page_number in range(pdfReader.numPages):
        page = pdfReader.getPage(page_number) # creating a page object 
        page_content += page.extractText() # extracting text from page object

    # closing the pdf file object 
    pdfFileObj.close() 

    #print(page_content)
    return page_content