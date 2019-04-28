# -*-coding:utf-8 -*

import unittest
import json
import re
import sys

# ouverture du dico

def dico():
    with open('convertion.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# convertion nombre arabe

def mots_nombre(words):
    nombre = []
    a = 0
    for word in words:
        found = False
        d = data['mot-arabe']
        for index in range(len(d)):
            find = re.findall(d[index]['autochtone'], word)
            if find:
                found = True
                nombre.append(d[index]['arabe'])
                if len(str(d[index]['arabe'])) > 6 and a == 0:
                    a = 0
                    nombre.append('+')
                elif len(str(d[index]['arabe'])) > 3 and a != 0:
                    nombre.pop(a-1)
                    a = 0
                    nombre.append('+')
                elif len(str(d[index]['arabe'])) > 2 and a == 0:
                    nombre.append('+')
                    a = len(nombre)
        if found == False:
            return word
    return nombre

# séparation des nombres (ex : 1000 = 1 000)

def espace(nombre):
    tab = []
    result = []
    j = 0
    for i in nombre:
        if i != '+':
            tab.append(i)
        elif i == '+' and j != 0:
            result.append(tab)
            tab = []
            j = 0
        j += 1
    result.append(tab)
    return result

# cas de séparation (ex : 70 = soixante-dix)

def separation(nombre):
    words = []
    word = ""
    for i, lettre in enumerate(nombre):
        if lettre == " " or lettre == "-":
            words.append(word)
            word = ""
        else:
            word += lettre
        if i+1 == len(nombre):
            words.append(word)
    return words

# convertion chiffre romain

def chiffre_romain(nombre):
    result = 0
    d = data['romain-arabe']
    for i in range(len(d)):
        result += nombre.count(d[i]['autochtone']) * d[i]['arabe']
    return result

# séparation chiffre romain

def pouet(nombre):
    str_nb = str(nombre)[::-1]
    nb = ""
    for i in range(len(str_nb)):
        nb += str_nb[i]
        if i % 3 == 2:
            nb += " "
    return nb[::-1]

# covertion total

def total(nombres):
    end = 0
    result = 0
    for tab in nombres:
        try:
            while len(tab) > 0:
                first = tab.pop(0)
                sec = tab.pop(0)
        except:
            end += first
    return end

def truc(text):
    try:
        if len(re.findall(r'^[MDCLXVI]*$', text)[0]):
            return 0
    except:
        return 1

# base

def main(text):
    if truc(text):
        a = separation(text)
        b = mots_nombre(a)
        if type(b) is str:
            print(
                "Hein ?! Mais '{}' ça veut rien dire, enfin en tout cas moi je ne sais pas le lire".format(b))
            return 'Error'
        else:
            c = espace(b)
            end = total(c)
    else:
        end = chiffre_romain(text)
    format_end = pouet(end)
    print("{} = {}".format(text, format_end))
    return format_end


class TestNombre(unittest.TestCase):

    def test_1(self):
        self.assertIn(main(
            "IV"), "4")

    def test_2(self):
        self.assertIn(
            main("six cents soixante six"), "666")

    def test_3(self):
        self.assertIn(main("iubdjcv"), "Error")

    def test_4(self):
        self.assertIn(main(
            "un Million Trois cents"), "1 000 300")

    def test_5(self):
        self.assertIn(main("MDCLXVI"), "1 666")

# texte entrée et erreurx

if __name__ == '__main__':
    data = dico()

    text_input = input('Quel nombre ou chiffre romain souhaitez vous convertir :')
    m = main(text_input)
    while m == "Error":
        m = main(input('Veuillez en essayer un autre :'))