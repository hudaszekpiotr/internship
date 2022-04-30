def length_of_longest_substring(s: str):
    if type(s) != str:
        raise ValueError("input must be string")
    i = 0
    j = 0
    d = {}
    ans = 0
    while j < len(s):
        if s[j] not in d or i > d[s[j]]:
            ans = max(ans, (j - i + 1))
            d[s[j]] = j
        else:
            i = d[s[j]] + 1
            ans = max(ans, (j - i + 1))
            j -= 1
        # print(ans)
        j += 1
    return ans
