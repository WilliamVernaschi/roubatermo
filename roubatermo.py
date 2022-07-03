import sys
from urllib.request import urlopen
import re

def get_letters(color):
    letters = list()
    for i in range(5):
        ith_col = input(f'Digite as letras em {color} da coluna {i+1} \
(deixe vazio se não exisitir): ')
        ith_col = "".join(ith_col.split()) # removes all whitespace
        letters.append(ith_col)
    return letters

words_pt_br = "https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt"
words_en_us = "https://raw.githubusercontent.com/dwyl/\
               english-words/master/words.txt"

game_is = 'termo'
if len(sys.argv) > 1:
    game_is = sys.argv[1].lower().strip() # game can be either wordle or termo

dic = ''
if game_is == 'termo':
    dic = words_pt_br
elif game_is == 'wordle':
    dic = words_en_us
else:
    raise Exception(f"{game_is} pode ser apenas wordle ou termo")

dic = str(urlopen(dic).read()).replace('\\n', '\n')

grey_letters = input('Digite as letras em cinza (que não \
fazem parte da palavra: ')
orange_letters = get_letters('laranja')
green_letters = get_letters('verde')

# removes overlap between grey and orange letters
grey_letters = ''.join(list(set(grey_letters) -
                            set(''.join([l for l in orange_letters]))))

# the regex pattern is of the form ^[^][^][^][^][^]$
# we determine what's inside each of the brackets.

regex_letters_patterns = list()
for i in range(5):
    ith_letter_pattern = ""
    if green_letters[i] == "": # if the correct letters is unknown
        ith_letter_pattern = '[^' + grey_letters + orange_letters[i] + ']'
    else:
        ith_letter_pattern = green_letters[i]
    regex_letters_patterns.append(ith_letter_pattern)

regex_pattern = '^' + ''.join(regex_letters_patterns) + '$'

must_have_letters = ''.join([col for col in orange_letters])
pre_possible = re.findall(regex_pattern, dic,
                          flags=re.MULTILINE | re.IGNORECASE)

print("Possíveis palavras: ")
for word in pre_possible:
    if set(must_have_letters).issubset(list(word.lower())):
        print(word.lower())

#bug conhecido: se a palavra correta for morte, e o usuário digitar 
#ossos, as letras ficarão: laranja, cinza, cinza, cinza, cinza, e o
#programa retornará como palavras possíveis, "xerox", mas não é possível,
#já que se a letra "o" fosse válida na posição 4, a 1ª letra da palavra
#ossos estaria cinza e a 4ª verde.
#Para corrigir, seria necessário que o usuário digitasse as letras cinzas
#por coluna, mas pela inconveniência de digitar e raridade da ocorrência,
#não será alterado.



