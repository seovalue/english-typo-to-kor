from django.shortcuts import render, redirect
from hangul_utils import join_jamos
import re
   
vowels_english_lower = ['y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'b', 'n', 'm']
vowels_english_upper = ['O', 'P']

vowels_korean_lower = ['ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ', 'ㅠ', 'ㅜ', 'ㅡ']
vowels_korean_upper = ['ㅒ', 'ㅖ']

consonant_english_lower = ['q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b']
consonant_english_upper = ['Q', 'W', 'E', 'R', 'T']

consonant_korean_lower = ['ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ']
consonant_korean_upper = ['ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ']

# 사전 만들기
def to_dict(eng_dict, kor_dict):
    {e:k for e, k in zip(eng_dict, kor_dict)}

vowels_lower_dict = to_dict(vowels_english_lower, vowels_korean_lower)
vowels_upper_dict = to_dict(vowels_english_upper, vowels_korean_upper)

consonant_lower_dict = to_dict(consonant_english_lower, consonant_korean_lower)
consonant_upper_dict = to_dict(consonant_english_upper, consonant_korean_upper)

# 사전 합치기
eng_to_kor_dict = {**vowels_lower_dict, **vowels_upper_dict, **consonant_lower_dict, **consonant_upper_dict}

stop_vowels = ['h', 'n', 'm']
check_vowels = ['k', 'o', 'j', 'p', 'l']

# tuple은 hash key로 쓸 수 있어서, 역 테이블을 만들 수 있다.
comb_vowels = {'ㅘ': ('h', 'k'), 'ㅙ': ('h', 'o'),'ㅝ': ('n', 'j'), 'ㅞ': ('n', 'p'), 'ㅚ': ('h', 'l'), 'ㅟ': ('n', 'l'), 'ㅢ': ('m', 'l')}

def get_reverse(a_dict):
    return {value:key for key, value in a_dict.items()}

re_comb_vowels = get_reverse(comb_vowels)

stop_consonants = ['r', 's', 'f', 'q']
check_consonants = ['t', 'w', 'g', 'r', 'a', 'q', 'x', 'v', 'g']

comb_consonants = {'ㄳ': ('r', 't'), 'ㄵ': ('s', 'w'), 'ㄶ': ('s', 'g'), 'ㄺ': ('f', 'r'), 'ㄻ': ('f', 'a'), 'ㄼ': ('f', 'q'),
                    'ㄽ': ('f', 't'), 'ㄾ': ('f', 'x'), 'ㄿ': ('f', 'v'), 'ㅀ': ('f', 'g'), 'ㅄ': ('q', 't')}

re_comb_consonants = get_reverse(comb_consonants)

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
    jamo = []
    i = 0
    while i < len(typos):
        new, special = '', ''
        if typos[i] in stop_vowels and typos[i + 1] in check_vowels:
            comb = (typos[i], typos[i + 1])
            special = special_vowels(comb)
        elif typos[i] in stop_consonants and typos[i + 1] in check_consonants:
            if typos[i+2] in vowels_english_upper or typos[i+2] in vowels_english_lower:
                new = convert_english_to_korean(typos[i])
            comb = (typos[i+len(new)], typos[i+len(new) + 1])
            special = special_consonants(comb)
        else:
            new = convert_english_to_korean(typos[i])
            
        i += len(new) + len(special) * 2
        jamo.append(new + special)
        
    # 문자열을 더하는 것보다 append하고 join하는 게 더 빠릅니다. 파이썬 공식 문서에서 추천하는 방법.
    return "".join(jamo)

def special_vowels(word_tup):
    return re_comb_vowels.get(word_tup, '')

def special_consonants(word_tup):
    return re_comb_consonants.get(word_tup, '')

def convert_english_to_korean(eng):
    return eng_to_kor_dict.get(eng, eng)  # key로 값을 찾아오고, 없으면 디폴트로 eng를 반환

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
