from nltk.tokenize import word_tokenize
from utility import get_stop_words, create_df, get_prgm_lang_list, extract_pdfToText_from_file
import docx2txt
import spacy
import os


def get_skills(resume_text):
    master_skill_list = get_prgm_lang_list()
    tokens = list(set(map(lambda x : x.lower(), word_tokenize(resume_text))))
    skills = [skill for skill in tokens if skill in master_skill_list]
    return skills

def get_skills_2(path):
    master_skill_list = get_prgm_lang_list()
    print(master_skill_list[:5])
    resume_text = get_resume_text(path)
    stop_words = get_stop_words()
    #nlp = spacy.load('spacy_models//en_core_web_sm//en_core_web_sm-2.1.0')
    nlp = spacy.load('en_core_web_sm')
    nlp_ed = nlp(resume_text)
    n_phrases = [token.text.strip().lower() for token in nlp_ed.noun_chunks
                 if token.text not in stop_words]
    skills = [skill for skill in n_phrases if skill in master_skill_list]
    return list(set(skills))


# print("Browse")
# path = input('Enter the path')
# resume_text = ''
# print(path)

def get_resume_text(path):
    resume_text = ''
    if os.path.isdir(path):
        print('Its a directory')
    elif os.path.isfile(path):
        print('Its a file')
        if path[-4:] == 'docx':
            resume_text =  docx2txt.process(path)
        # print(resume_text)
        elif path[-3:] == 'doc':
            pass # replace with Hidayat function
        elif path[-3:] == 'pdf':    
            print('Its a pdf file')
            resume_text = extract_pdfToText_from_file(path)
            # print(resume_text)
    return resume_text

# prgm_lang_list = [x.strip().lower() for x in get_prgm_lang_list()]
# master_skill_list = prgm_lang_list
#resumes_df = create_df()


#print(resumes_df.iloc[10]['resume_text'])
#print(list(set(get_skills_2(resumes_df.iloc[10]['resume_text']))))
# print(list(set(get_skills_2(resume_text))))