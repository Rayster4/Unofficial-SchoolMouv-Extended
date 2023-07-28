# Don't forget to place the folder schoolmouv alongside your file.

from tkinter import Tk 
from tkinter.filedialog import askopenfilename, askdirectory
from schoolmouv.Webscrap import WebScrap
import os 

# Just the url
path = askdirectory()
os.chdir(path=path)
course = "https://www.schoolmouv.fr/cours/les-caracteristiques-du-capitalisme-des-annees-1920-/fiche-de-cours" # PDF
WebScrap.scrap(url=course, is_pdf=True, overwrite=False, path=os.getcwd())
course = "https://www.schoolmouv.fr/cours/les-caracteristiques-du-capitalisme-des-annees-1920-/cours-video" # Vidéo
WebScrap.scrap(url=course, is_pdf=False, overwrite=False, path=os.getcwd())

# All sections in the url
path = askdirectory()
os.chdir(path=path)
course = "https://www.schoolmouv.fr/cours/les-caracteristiques-du-capitalisme-des-annees-1920-/" # It will downloads the 'cours', the 'Vidéo' and the 'Fiche de révision"
WebScrap.scrap_sections(courses_url=course, download=True, path=os.getcwd(), overwrite=False)

# All courses in the index
path = askdirectory()
os.chdir(path=path)
courses = WebScrap.scrap_courses("/1ere/enseignement-moral-et-civique/programme")
for course in courses:
    WebScrap.make_and_change_dir(course) # Chapitre 1, Chapitre 2...
    dict_url_course = courses[course]
    for sections in dict_url_course:
        WebScrap.make_and_change_dir(sections) # Cours du chapitre 1, Cours du chapitre 2
        WebScrap.scrap_sections(courses_url=dict_url_course[sections], download=True, path=os.getcwd(), overwrite=False)
        os.chdir("..")
    os.chdir("..")

# All courses in the index
path = askdirectory()
os.chdir(path=path)
courses = WebScrap.scrap_courses("/1ere/enseignement-moral-et-civique/programme")
for course in courses:
    WebScrap.make_and_change_dir(course) # Chapitre 1, Chapitre 2...
    dict_url_course = courses[course]
    for sections in dict_url_course:
        WebScrap.make_and_change_dir(sections) # Cours du chapitre 1, Cours du chapitre 2
        WebScrap.scrap_sections(courses_url=dict_url_course[sections], download=True, path=os.getcwd(), overwrite=False)
        os.chdir("..")
    os.chdir("..")

# All indexes in the subjects
path = askdirectory()
os.chdir(path=path)
indexes = WebScrap.scrap_indexes(subject_url="/1ere/enseignement-moral-et-civique")
for index in indexes:
    WebScrap.make_and_change_dir(index) # Programme, definitions...
    dict_url_index = indexes[index]
    courses = WebScrap.scrap_courses(dict_url_index) #dict_url_index
    for course in courses:
        WebScrap.make_and_change_dir(course) # Chapitre 1, Chapitre 2...
        dict_url_course = courses[course]
        for sections in dict_url_course:
            WebScrap.make_and_change_dir(sections) # Cours du chapitre 1, Cours du chapitre 2
            WebScrap.scrap_sections(courses_url=dict_url_course[sections], download=True, path=os.getcwd())
            os.chdir("..")
        os.chdir("..")
    os.chdir("..")

# All subjects in the grade
path = askdirectory()
os.chdir(path=path)
subjects = WebScrap.scrap_subjects("/1ere") # For example
for subject in subjects: # Mathématiques...
    dict_url_subjects = subjects[subject]
    indexes = WebScrap.scrap_indexes(subject_url=dict_url_subjects)
    for index in indexes:
        WebScrap.make_and_change_dir(index) # Programme, definitions...
        dict_url_index = indexes[index]
        courses = WebScrap.scrap_courses(dict_url_index) #dict_url_index
        for course in courses:
            WebScrap.make_and_change_dir(course) # Chapitre 1, Chapitre 2...
            dict_url_course = courses[course]
            for sections in dict_url_course:
                WebScrap.make_and_change_dir(sections) # Cours du chapitre 1, Cours du chapitre 2
                WebScrap.scrap_sections(courses_url=dict_url_course[sections], download=True, path=os.getcwd())
                os.chdir("..")
            os.chdir("..")
        os.chdir("..")
    os.chdir("..")
