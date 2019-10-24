# General Imports
import os
import pandas as pd

# to extract list of programming lanugages from wiki
import urllib.request
from bs4 import BeautifulSoup

# to convert docx to text
import docx2txt

# for nlp
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

# To extract text from pdf
#from pdfminer.converter import TextConverter
#from pdfminer.pdfinterp import PDFPageInterpreter
#from pdfminer.pdfinterp import PDFResourceManager
#from pdfminer.pdfpage import PDFPage
import io

import PyPDF2 

resumes_path = "C:\\Users\\144725\\PythonProjects\\TAGBot\\Sample Resumes"
#PdfPath = "C:\\Users\\144725\\PythonProjects\\TAGBot\\Sample Resumes\\Resum1.pdf"


# keep all the resumes in the path Sample Resumes
def create_df():
    # resume_input_path = ".\\Sample Resumes"
    all_files = list()

    # list to keep the file names that were already convereted so that it need not be convereted again
    # converting process takes too much time

    df = pd.DataFrame(columns=['resume_text'])
    already_converted_files = pd.DataFrame(columns=['file_name'])
    try:
        df = pd.read_csv('resume_in_text.csv', index_col=0)
    except OSError:
        print('resume_in_text.csv not found. New one will be created')

    try:
        already_converted_files = pd.read_csv('converted_files_list.csv', index_col=0)
    except OSError:
        print('converted_files_list.csv not found. New one will be created')

    # Build a map of file name with full path
    for root, subdir, files in os.walk(resumes_path):
        # print(files)
        files_in_this_dir = map(lambda x: os.path.join(root, x), files)
        all_files.append(files_in_this_dir)

    # Create a list out of the map's first element
    # TODO: Change this hard coding. Need to write a smart function to create the list with fils with full path
    fl = list(all_files[0])

    # Create a dataframe of resumes

    for file in fl:
        if file not in already_converted_files['file_name'].values:
            if file[-4:] == 'docx':
                df = df.append({'resume_text': docx2txt.process(file)}, ignore_index=True)
                # df = df.append([[docx2txt.process(file)]])
                already_converted_files = already_converted_files.append({'file_name': file}, ignore_index=True)
                # already_converted_files = already_converted_files.append([[file]])
            elif file[-3:] == 'pdf':
                df = df.append({'resume_text': extract_pdfToText_from_file(file)}, ignore_index=True)
                # df = df.append([[extract_text_from_pdf(file)]])
                already_converted_files = already_converted_files.append({'file_name': file}, ignore_index=True)
                # already_converted_files = already_converted_files.append([[file]])

    # TODO : Eventually store the converted text in database
    df.to_csv('resume_in_text.csv')
    already_converted_files.to_csv('converted_files_list.csv')

    return df


# def extract_text_from_pdf(pdf_file):
#     resource_manager = PDFResourceManager()
#     fake_file = io.StringIO()
#     converter = TextConverter(resource_manager, fake_file)
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)

#     with open(pdf_file, 'rb') as f:
#         for page in PDFPage.get_pages(f):
#             page_interpreter.process_page(page)
#         text = fake_file.getvalue()

#     converter.close()
#     fake_file.close()

#     if text:
#         return text


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


def clean_corpus():
    corpus = list()
    stop_words = get_stop_words()
    df = create_df()
    for i in range(len(df.index)):
        text = re.sub(r'[^a-zA-Z0-9\+*\#]', ' ', df['resume_text'][i])
        text = text.lower()
        text = text.split()
        # ps = PorterStemmer()
        # text = [ps.stem(x) for x in text if x not in stop_words]
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(x) for x in text if x not in stop_words]
        text = ' '.join(text)
        corpus.append(text)
    return corpus


def clean_text(text):
    stop_words = get_stop_words()
    text = re.sub(r'[^a-zA-Z0-9\+*\#]', ' ', text).lower().split()
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(x) for x in text if x not in stop_words]
    text = ' '.join(text)
    return text

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