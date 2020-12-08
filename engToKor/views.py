from django.shortcuts import render, redirect
from hangul_utils import join_jamos
import re

from characters import * # 상수를 모두 파일로 만들어서 분리.

def index(request):
    return render(request, 'index.html')


def convert(request):
    if request.method == 'POST':
        typos = request.POST['contents']
        if isHangul(typos):
            return render(request, 'convert.html', {
                'result': typos,
            })
        jamo = typo_to_kor_char(str(typos))
        result = typo_to_hangul(jamo)
        return render(request, 'convert.html', {
            'result': result,
        })


def typo_to_kor_char(typos):
    jamo = []
    i = 0
    length = len(typos) # 매번 len을 호출하는 건 낭비다. 길이는 변하지 않으니까.
    typos += '  ' # 무의미한 공백을 추가해서 index에러를 차단하자.
    
    while i < length:
        new, special = '', ''
        if is_comb_vowel(typos, i):
            special = special_vowels(comb(typos, i))
        elif is_comb_consonant(typos, i):
            if is_vowel(typos, i+2):
                new = convert_english_to_korean(typos[i])
            special = special_consonants(comb(typos, i + len(new)))
        else:
            new = convert_english_to_korean(typos[i])
            
        i += len(new) + len(special) * 2
        jamo.append(new + special)
    return "".join(jamo)

def special_vowels(word_tup):
    return re_comb_vowels.get(word_tup, '')

def special_consonants(word_tup):
    return re_comb_consonants.get(word_tup, '')
    
def comb(typos, i):
    return (typos[i], typos[i + 1])    
    
def is_comb_vowel(typos, i):
    return typos[i] in stop_vowels and typos[i + 1] in check_vowels

def is_comb_consonant(typos, i):
    return typos[i] in stop_consonants and typos[i + 1] in check_consonants

def is_vowel(typos, i):
    return typos[i] in vowels_english

def convert_english_to_korean(eng):
    return eng_to_kor_dict.get(eng, eng)  # key로 값을 찾아오고, 없으면 디폴트로 eng를 반환

# reference: https://m.blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221142971719&proxyReferer=https:%2F%2Fwww.google.com%2F
def isHangul(text):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    return hanCount > 0

def typo_to_hangul(string):
    chars = list(set(string))
    char_to_num = {ch: i for i, ch in enumerate(chars)}
    num_to_char = {i: ch for i, ch in enumerate(chars)}

    numbers = [char_to_num[x] for x in string]
    converted_text = ''.join([num_to_char[x] for x in numbers])
    converted_text = join_jamos(converted_text)
    return converted_text
