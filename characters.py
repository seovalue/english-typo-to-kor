
vowels_english_lower = ['y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'b', 'n', 'm']
vowels_english_upper = ['O', 'P']

vowels_english = vowels_english_upper + vowels_english_lower

vowels_korean_lower = ['ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ', 'ㅠ', 'ㅜ', 'ㅡ']
vowels_korean_upper = ['ㅒ', 'ㅖ']

consonant_english_lower = ['q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b']
consonant_english_upper = ['Q', 'W', 'E', 'R', 'T']

consonant_korean_lower = ['ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ']
consonant_korean_upper = ['ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ']

# 사전 만들기
def to_dict(eng_dict, kor_dict):
    return {e:k for e, k in zip(eng_dict, kor_dict)}
vowels_lower_dict = to_dict(vowels_english_lower, vowels_korean_lower)
vowels_upper_dict = to_dict(vowels_english_upper, vowels_korean_upper)
consonant_lower_dict = to_dict(consonant_english_lower, consonant_korean_lower)
consonant_upper_dict = to_dict(consonant_english_upper, consonant_korean_upper)
# 사전 합치기
eng_to_kor_dict = {**vowels_lower_dict, **vowels_upper_dict, **consonant_lower_dict, **consonant_upper_dict}
stop_vowels = ['h', 'n', 'm']
check_vowels = ['k', 'o', 'j', 'p', 'l']
# tuple은 hash key로 쓸 수 있어서, 역 테이블을 만들 수 있다.
comb_vowels = {'ㅘ': ('h', 'k'),
               'ㅙ': ('h', 'o'),
               'ㅝ': ('n', 'j'),
               'ㅞ': ('n', 'p'),
               'ㅚ': ('h', 'l'),
               'ㅟ': ('n', 'l'),
               'ㅢ': ('m', 'l')}
def get_reverse(a_dict):
    return {value:key for key, value in a_dict.items()}
re_comb_vowels = get_reverse(comb_vowels)
stop_consonants = ['r', 's', 'f', 'q']
check_consonants = ['t', 'w', 'g', 'r', 'a', 'q', 'x', 'v', 'g']
comb_consonants = {'ㄳ': ('r', 't'),
                   'ㄵ': ('s', 'w'),
                   'ㄶ': ('s', 'g'),
                   'ㄺ': ('f', 'r'),
                   'ㄻ': ('f', 'a'),
                   'ㄼ': ('f', 'q'),
                   'ㄽ': ('f', 't'),
                   'ㄾ': ('f', 'x'),
                   'ㄿ': ('f', 'v'),
                   'ㅀ': ('f', 'g'),
                   'ㅄ': ('q', 't')}
re_comb_consonants = get_reverse(comb_consonants)