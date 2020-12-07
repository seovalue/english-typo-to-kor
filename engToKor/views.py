from django.shortcuts import render, redirect
from hangul_utils import join_jamos
import re

# HardCoding Values
consonant_english_lower = ['q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b']
consonant_english_upper = ['Q', 'W', 'E', 'R', 'T']
vowels_english_lower = ['y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'b', 'n', 'm']
vowels_english_upper = ['O', 'P']
consonant_korean_lower = ['ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ']
consonant_korean_upper = ['ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ']
vowels_korean_lower = ['ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ', 'ㅠ', 'ㅜ', 'ㅡ']
vowels_korean_upper = ['ㅒ', 'ㅖ']
stop_vowels = ['h', 'n', 'm']
check_vowels = ['k', 'o', 'j', 'p', 'l']
comb_vowels = {'ㅘ': ['h', 'k'], 'ㅙ': ['h', 'o'], 'ㅝ': ['n', 'j'], 'ㅞ': ['n', 'p'], 'ㅚ': ['h', 'l'],
               'ㅟ': ['n', 'l'], 'ㅢ': ['m', 'l']}
stop_consonants = ['r', 's', 'f', 'q']
check_consonants = ['t', 'w', 'g', 'r', 'a', 'q', 'x', 'v', 'g']
comb_consonants = {'ㄳ': ['r', 't'], 'ㄵ': ['s', 'w'], 'ㄶ': ['s', 'g'], 'ㄺ': ['f', 'r'], 'ㄻ': ['f', 'a'], 'ㄼ': ['f', 'q'],
                   'ㄽ': ['f', 't'], 'ㄾ': ['f', 'x'], 'ㄿ': ['f', 'v'], 'ㅀ': ['f', 'g'], 'ㅄ': ['q', 't']}


def index(request):
    return render(request, 'index.html')


def convert(request):
    if request.method == 'POST':
        typos = request.POST['contents']
        if isHangul(typos):
            return render(request, 'convert.html', {
                'result': typos,
            })
        typos = list(typos)
        jamo = typo_to_kor_char(typos)
        result = typo_to_hangul(jamo)
        return render(request, 'convert.html', {
            'result': result,
        })


def typo_to_kor_char(typos):
    jamo = ''
    i = 0
    while i < len(typos):
        if typos[i] in stop_vowels and typos[i + 1] in check_vowels:
            jamo += convert_english_to_korean_special_vowels([typos[i], typos[i + 1]])
            i += 1
        elif typos[i] in stop_consonants and typos[i + 1] in check_consonants:
            jamo += convert_english_to_korean_special_consonants([typos[i], typos[i + 1]])
            i += 1
        else:
            jamo += convert_english_to_korean(typos[i])
        i += 1
    return jamo


def convert_english_to_korean_special_vowels(word_list):
    for key, value in comb_vowels.items():
        if word_list == value:
            return key


def convert_english_to_korean_special_consonants(word_list):
    for key, value in comb_consonants.items():
        if word_list == value:
            return key


def convert_english_to_korean(eng):
    if eng in consonant_english_lower:
        index = consonant_english_lower.index(eng)
        return consonant_korean_lower[index]
    elif eng in consonant_english_upper:
        index = consonant_english_upper.index(eng)
        return consonant_korean_upper[index]
    elif eng in vowels_english_lower:
        index = vowels_english_lower.index(eng)
        return vowels_korean_lower[index]
    elif eng in vowels_english_upper:
        index = vowels_english_upper.index(eng)
        return vowels_korean_upper[index]
    else:
        return eng


# reference: https://m.blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221142971719&proxyReferer=https:%2F%2Fwww.google.com%2F
def isHangul(text):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    if hanCount > 0:
        return True
    return False


def typo_to_hangul(string):
    chars = list(set(string))
    char_to_num = {ch: i for i, ch in enumerate(chars)}
    num_to_char = {i: ch for i, ch in enumerate(chars)}

    numbers = [char_to_num[x] for x in string]
    converted_text = ''.join([num_to_char[x] for x in numbers])
    converted_text = join_jamos(converted_text)
    return converted_text
