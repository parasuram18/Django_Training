def romanToInt() -> int:
    a={'I':1,
       'V'  :5,
       'X'  :10,
       'L'  :50,
       'C'  :100,
       'D'  :500,
       'M'  :1000,
    }

    s = "III"
    output = a[s[-1]]
    for i in range(len(s)-1,0,-1):
        let = s[i]
        bef = s[i-1]
        if a[bef]<output:
            output-=a[bef]
        else:
            output+=a[bef]
    return output
ans = romanToInt()
# print(ans)


list1 = [1,2,4]
list2 = [1,3,4]

list3 = sorted(list1+list2)
