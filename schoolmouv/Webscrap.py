"""
@author:Rayster4
Warning: This code can be deprecated easily because it's a webscraping script. 
This tool isn't affiliated to SchoolMouv in any way
"""

import requests
from .schoolmouv import pdf, video
from bs4 import BeautifulSoup
import os
import re

class WebScrap():
    """WebScraping content from https://www.schoolmouv.fr/

    Functions : scrap_subjects
                scrap_indexes
                scrap_courses
                scrap_sections
    """

    def __init__(self):
        self.baseURL = "https://www.schoolmouv.fr"
        self.grades_scrap_class = ["item dropdown-item", "tooltip-item"]
        self.subjects_scrap_class = "subject-module_card__zxiRL"
        self.indexes_scrap_class = "index"
        self.chapters_scrap_class = ["chapter", "chapter-num"]
        self.courses_scrap_class = "sheet-name"
        self.sections_scrap_class = ["resource-button_resource-button__link__LTBQI link-module_xxx__aw2PQ link-module_xxx--large__UT8xp link-module_xxx--tab__zWlyD link-module_xxx--global__pTt-C", "resource-button_resource-button__title__uTwTz", "gss-type"]

    def scrap(self, url : str, is_pdf : bool, overwrite : bool, path : str) -> None:
        """A scrap function which use the library 'schoolmouv' of t0pl

        Args:
            url (str): The url to download
            is_video (bool): change the process if it's a video if it's a video
            overwrite (bool): if need to overwrite
            path (str): The path where files will be downloaded
        """

        if is_pdf:dl_object, ext = pdf(url),"pdf"
        else:dl_object, ext = video(url),"mp4"
        save_as_split = url.split("/")
        save_name = f'{save_as_split[-2]}_{save_as_split[-1]}.{ext}'
        dl_object.run()
        try:
            result = dl_object.result # result found (str) (direct url to pdf)
            if isinstance(result, list):
                _ = requests.get(result[0])
                while len(_.headers.get('content-length', 0)) < 9:
                    dl_object.run()
                    result = dl_object.result
                    _ = requests.get(result[0])
            dl_object.download(result, path, save_as=save_name, overwrite=overwrite) # type: ignore # Default filename is 'Echantillonage 2.pdf' (in this case)
        except Exception as e:
            print(f"An error has occured for {url} ({e})")

    def scrap_grades(self) -> dict:
        """Functions for scrap school's grade:

        Args: //
        """
        data = {}
        url = self.baseURL
        req = requests.get(url).text
        get = BeautifulSoup(req, features="html.parser")
        grades = get.find_all(class_=self.grades_scrap_class[0])
        for grade in grades[0].find_all(class_=self.grades_scrap_class[1]):
            grade = grade.find("a")
            grade_url = grade.get("href") 
            grade_name = grade_url.split("/")[-1]
            data[grade_name] = grade_url
        return data

    def scrap_subjects(self, school_grade : str) -> dict:
        """Functions for scrap school grade's subjects :

        Args:
            school_grade (str): school grade's url (without the baseURL) for eg: /1ere
        """
        data = {}
        url = self.baseURL + school_grade
        req = requests.get(url).text
        get = BeautifulSoup(req, features="html.parser")
        subjects = get.find_all(class_=self.subjects_scrap_class)
        for subject in subjects:
            subject_url = subject.get("href") # https://www.schoolmouv.fr/1ere/enseignement-moral-et-civique
            subject_name = subject_url.split("/")[-1]
            data[subject_name] = subject_url
        return data

    def scrap_indexes(self, subject_url : str) -> dict:
        """Functions for scrap subject's indexes for eg: programs, definitions :

        Args:
            subject_url (str): subject's url (without the baseURL) for eg: /1ere/enseignement-moral-et-civique
        """
        data = {}
        url = self.baseURL + subject_url
        req = requests.get(url).text
        get = BeautifulSoup(req, features="html.parser")
        indexes = get.find_all(class_=self.indexes_scrap_class)
        for index in indexes:
            index_url = index.get("href")
            index_name = index_url.split("/")[-1]
            data[index_name] = index_url
        return data

    def scrap_courses(self, indexes_url : str) -> dict:
        """Functions for scrap indexes's courses:

        Args:
            indexes_url (str): indexes_url's url (without the baseURL) for eg: /1ere/enseignement-moral-et-civique/programme
        """
        data = {}
        url = self.baseURL + indexes_url
        req = requests.get(url).text
        get = BeautifulSoup(req, features="html.parser")
        chapters = get.find_all(class_=self.chapters_scrap_class[0])
        for chapter in chapters:
            title = chapter.find_all(class_=self.chapters_scrap_class[1])[0].text[:-1] + " " + chapter.findAll("h2")[0].find("p").text
            _ = {} 
            for courses in chapter.find_all(class_="sheet-name"):
                course_url = courses.get("href")
                course_name = course_url.split("/")[-2] 
                _[course_name] = course_url
            data[title] = _
        return data

    def scrap_sections(self, courses_url : str, download : bool = False, path : str = "", overwrite = False) -> dict: 
        """Functions for scrap courses's [in] sections:

        Args:
            courses_url (str): courses_url's url (without the baseURL) for eg: /sujets-bac/sujet-zero-2020-specialite-sciences-de-l-ingenieur-le-rameur/fiche-annale
            download (bool) [optional]: A download option (ONLY if the library schoolmouv is IMPORTED), in the located path
            path (bool) [optional]: The path if the download option is activate
        """
        data = {}
        _ = None
        url = self.baseURL + courses_url
        req = requests.get(url).text
        get = BeautifulSoup(req, features="html.parser")
        sections = get.find_all(class_=self.sections_scrap_class[0])
        for section in sections:
            section_url = section.get("href")
            section_name = section.text[1:]
            _ = True
            data[section_name] = section_url
            if download and path:
                self.scrap(url=section_url, is_pdf=True, overwrite=overwrite, path=path)
        if not _:
            try:
                data[get.find_all(class_=self.sections_scrap_class[2])[0].text] = courses_url
                if download and path:
                    self.scrap(url=url, is_pdf=True, overwrite=overwrite, path=path)
            except:
                pass
        else:
            not_recognized_sections = get.find_all(class_=self.sections_scrap_class[1])
            for i in not_recognized_sections:
                if i.text == "Vidéo":
                    passcode = "/cours-video"
                    url_ = self.baseURL + "/".join(courses_url.split("/")[:-1]) + passcode
                    if download and path:
                        self.scrap(url=url_, is_pdf=False, overwrite=overwrite, path=path)
                elif i.text == "Quiz":
                    passcode = "/qcm"
                else:
                    continue
                data[i.text] = "/".join(courses_url.split("/")[:-1]) + passcode
        return data
    
    def format_folder_name(self, folder_name):
        # Define a regex pattern to remove invalid characters
        invalid_chars_pattern = r'[\\/:"*?<>|]+'
        # Remove or replace invalid characters with underscores
        formatted_name = re.sub(invalid_chars_pattern, '_', folder_name)
        return formatted_name
    
    def make_and_change_dir(self):
        if not os.path.exists(folder_name):
            folder_name = self.format_folder_name(folder_name)
            os.mkdir(folder_name)
        os.chdir(folder_name)