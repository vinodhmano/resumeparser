from nltk.tokenize import word_tokenize
from utility import *
import spacy


def get_skills(resume_text):
    tokens = list(set(map(lambda x : x.lower(), word_tokenize(resume_text))))
    skills = [skill for skill in tokens if skill in prgm_lang_list]
    return skills

def get_skills_2(resume_text):
    stop_words = get_stop_words()
    nlp = spacy.load('spacy_models//en_core_web_sm//en_core_web_sm-2.1.0')
    nlp_ed = nlp(resume_text)
    n_phrases = [token.text.strip().lower() for token in nlp_ed.noun_chunks
                 if token.text not in stop_words]
    skills = [skill for skill in n_phrases if skill in master_skill_list]
    return skills


prgm_lang_list = [x.strip().lower() for x in get_prgm_lang_list()]
master_skill_list = prgm_lang_list
resumes_df = create_df()
#resumes_df['skills'] = resumes_df['resume_text'].apply(get_skills)
#print(resumes_df.head(20))



print(get_skills_2(resumes_df.iloc[13]['resume_text']))
