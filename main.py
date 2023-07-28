import schoolmouv.schoolmouv as schoolmouv
from schoolmouv.Webscrap import WebScrap
import os
import colorama
import pprint
import re
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, askdirectory
import sys,time,random
from typing import List

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

#def suppr_up_line(n=1):
#    for i in range(n):
#        sys.stdout.write("\033[F")
#        sys.stdout.write("\033[K")

def suppr_up_line(n=1):
    for i in range(n):
        # Move the cursor up one line
        sys.stdout.write('\x1b[1A')
        # Clear the entire line
        sys.stdout.write('\x1b[2K')
        sys.stdout.flush()

def list_formating(var : List[str], indexed = True):
    if indexed:
        b = "\t1 - "
        number = 2
        for i in var:
            b = b + i + "\n\t"
            b += str(number) + " - "
            number += 1
        return b[0:len(b)-5]
    else:
        b = "\t"
        for i in var:
            b = b + i + "\n\t"
        return b[0:len(b)-2]


def format_folder_name(folder_name):
    # Define a regex pattern to remove invalid characters
    invalid_chars_pattern = r'[\\/:"*?<>|]+'
    # Remove or replace invalid characters with underscores
    formatted_name = re.sub(invalid_chars_pattern, '_', folder_name)
    return formatted_name


def make_and_change_dir(folder_name):
    if not os.path.exists(folder_name):
        folder_name = format_folder_name(folder_name)
        os.mkdir(folder_name)
    os.chdir(folder_name)

def slow_type(t, bpm = 9999, end="\n"):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/bpm)
    print('', end=end)

def one_or_two():
    print(colorama.Fore.YELLOW,end="")
    slow_type("Vous : ", end="\t")
    print(colorama.Fore.WHITE,end="")
    inp = input()
    suppr_up_line()
    while inp != "1" and inp != "2":
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.RED, end="")
        slow_type(f"Vous devez choisir entre 1 ou 2 ! Pas {inp}",bpm = 500)
        print(colorama.Fore.WHITE, end="")
        inp = input("\t")
        suppr_up_line()
        suppr_up_line()
    if inp == "1":
        return 1
    if inp == "2":
        return 2 

def ask_dict(data : dict):
    valid_inputs = [i for i in range(1, len(list(data.keys())) + 1 )]
    inp = input()
    while inp not in valid_inputs:
        suppr_up_line()
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE,end="")
        if isinstance(inp, str) and not inp.isdigit():
            print(colorama.Fore.RED, end="")
            slow_type(f"{inp} n'est pas un numéro...")
            print(colorama.Fore.WHITE, end="")
            inp = input("\t")
            suppr_up_line()
            continue
        elif int(inp) not in valid_inputs:
            print(colorama.Fore.RED, end="")
            slow_type(f"{inp} n'est pas dans la liste des options donnée...")
            print(colorama.Fore.WHITE, end="")
            inp = input("\t")
            suppr_up_line()
            continue
        inp = int(inp)
    if not isinstance(inp, int):
        inp = int(inp)
        suppr_up_line()
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE,end="")
    return inp

if __name__ == "__main__":
    scrap = WebScrap()
    
    response = grade = index = path = subject = ""
    os.system("cls")
    print(colorama.Fore.MAGENTA,end="")
    slow_type("Fred : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type("Bonjour ! Je serais votre assistant tout au long de l'installations des fichiers...\n\tCommençons par le plus difficile, où voulez-vous que vos fichiers soient installés ?", bpm=500)
    print()
    check = False
    while check != True:
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        time.sleep(2)
        path = askdirectory() # show an "Open" dialog box and return the path to the selected file
        while path == "":
            print(colorama.Fore.RED, end="")
            slow_type("Vous ne pouvez pas sauter cette étape ! Choissisez une destination !")
            time.sleep(2)
            path = askdirectory()
            suppr_up_line()
            print(colorama.Fore.YELLOW,end="")
            print("Vous : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(path, bpm=500)
        print()
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred :", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type("Êtes-vous sur ?\n\t[1 : Oui, 2 : Non]", bpm=500)
        print()
        response = one_or_two()
        if response == 2:
            suppr_up_line(5)
            continue
        else:
            check = True
    print(colorama.Fore.YELLOW,end="")
    slow_type("Vous : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type(str(response), bpm=500)
    print()
    print(colorama.Fore.MAGENTA,end="")
    slow_type("Fred : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type("Maintenant, il est temps de choisir une classe, quel classe voulez-vous téléchargez ?", bpm=500)
    print()
    data = scrap.scrap_grades()
    slow_type(list_formating(var=list(data.keys())), bpm=1000)
    check = False
    while check != True:
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE,end="")
        inp = ask_dict(data=data)
        grade = list(data.keys())[inp-1]
        slow_type(grade)
        print()
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred :", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(f"Êtes-vous sur ? ({data[grade]})\n\t[1 : Oui, 2 : Non]", bpm=500)
        print()
        response = one_or_two()
        if response == 2:
            suppr_up_line(5)
            continue
        else:
            check = True
    print(colorama.Fore.YELLOW,end="")
    slow_type("Vous : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type(str(response), bpm=500)
    print()
    print(colorama.Fore.MAGENTA,end="")
    slow_type("Fred : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type("C'est bien, nous avançons, rentrons dans le vif du sujet, quelles matières voulez-vous télécharger ?", bpm=500)
    print()
    data = scrap.scrap_subjects(school_grade=f"/{grade}")
    slow_type(list_formating(var=list(data.keys())), bpm=1000)
    check = False
    while check != True:
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE,end="")
        inp = ask_dict(data=data)
        subject = list(data.keys())[inp-1]
        slow_type(subject)
        print()
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred :", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(f"Êtes-vous sur ? ({data[subject]})\n\t[1 : Oui, 2 : Non]", bpm=500)
        print()
        response = one_or_two()
        if response == 2:
            suppr_up_line(5)
            continue
        else:
            check = True
    print(colorama.Fore.YELLOW,end="")
    slow_type("Vous : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type(str(response), bpm=500)
    print()
    print(colorama.Fore.MAGENTA,end="")
    slow_type("Fred : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type("Je vois, je vois, et dans cette matières vous voulez téléchargez quels indexs ?", bpm=500)
    print()
    data1 = scrap.scrap_indexes(subject_url=f"/{grade}/{subject}")
    slow_type(list_formating(var=list(data1.keys())), bpm=1000)
    check = False
    while check != True:
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE,end="")
        inp = ask_dict(data=data)
        index = list(data1.keys())[inp-1]
        slow_type(index)
        print()
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred :", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(f"Êtes-vous sur ? ({data1[index]})\n\t[1 : Oui, 2 : Non]", bpm=500)
        print()
        response = one_or_two()
        if response == 2:
            suppr_up_line(5)
            continue
        else:
            check = True
    print(colorama.Fore.YELLOW,end="")
    slow_type("Vous : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type(str(response), bpm=500)
    print()
    print(colorama.Fore.MAGENTA,end="")
    slow_type("Fred : ", end="\t")
    print(colorama.Fore.WHITE, end="")
    slow_type("Nous avançons plûtot bien, voulez-vous télécharger un chapitre en particulier ?\n\t[1 : Oui, 2 : Non]\n", bpm=500)
    data = scrap.scrap_courses(indexes_url=data1[index])
    slow_type(list_formating(var=list(data.keys()), indexed=False), bpm=1000)
    print()
    response = one_or_two()
    courses = ''
    if response == 1:
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type("Choissisez donc ce que vous voulez.", bpm=500)
        print()
        check = False
        while check != True:
            print(colorama.Fore.YELLOW,end="")
            slow_type("Vous : ", end="\t")
            print(colorama.Fore.WHITE,end="")
            inp = ask_dict(data=data)
            courses = list(data.keys())[inp-1]
            slow_type(courses)
            print()
            print(colorama.Fore.MAGENTA,end="")
            slow_type("Fred :", end="\t")
            print(colorama.Fore.WHITE, end="")
            slow_type(f"Êtes-vous sur ? ({courses})\n\t[1 : Oui, 2 : Non]", bpm=500)
            print()
            response = one_or_two()
            if response == 2:
                suppr_up_line(5)
                continue
            else:
                check = True
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(str(response), bpm=500)
        print()
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(f"Page {scrap.baseURL + data1[index]}\n\t{courses}\n\tDossier : {path}\n\n\tVoulez-vous continuer ?\n\t[1 : Oui, 2 : Non]", bpm=500)
        print()
        response = one_or_two()
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(str(response), bpm=500)
        print()
        if response == 2:
            exit()
        os.chdir(path=path)
        make_and_change_dir(courses) # Chapitre 1, Chapitre 2...
        dict_url_course = data[courses]
        for sections in dict_url_course:
            make_and_change_dir(sections) # Cours du chapitre 1, Cours du chapitre 2
            scrap.scrap_sections(courses_url=dict_url_course[sections], download=True, path=os.getcwd())
            print()
            os.chdir("..")
        print("Fin du programme..")
        time.sleep(999)
    else:
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(f"Page {scrap.baseURL + data1[index]}\n\tDossier : {path}\n\n\tVoulez-vous continuer ?\n\t[1 : Oui, 2 : Non]", bpm=500)
        response = one_or_two()
        if response == 2:
            exit()
        print(colorama.Fore.YELLOW,end="")
        slow_type("Vous : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(str(response), bpm=500)
        print()
        os.chdir(path=path)
        courses = scrap.scrap_courses(data1[index]) #dict_url_index
        for course in courses:
            make_and_change_dir(course) # Chapitre 1, Chapitre 2...
            dict_url_course = courses[course]
            for sections in dict_url_course:
                make_and_change_dir(sections) # Cours du chapitre 1, Cours du chapitre 2
                scrap.scrap_sections(courses_url=dict_url_course[sections], download=True, path=os.getcwd())
                print()
                os.chdir("..")
            os.chdir("..")
        print(colorama.Fore.MAGENTA,end="")
        slow_type("Fred : ", end="\t")
        print(colorama.Fore.WHITE, end="")
        slow_type(f"Merci d'avoir utilisé ce programme.", bpm=500)
        time.sleep(999)