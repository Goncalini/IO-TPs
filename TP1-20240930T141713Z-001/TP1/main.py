S = [7, 10, 11]
NS = {
    7: 8,
    10: 5,
    11: "inf"
}
D = [2, 3, 4, 5]
ND = {
    2: 4,
    3: 10,
    4: 8,
    5: 5,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
}
R = [ 9, 8, 7, 6, 5, 4, 3 ]

# S = [5, 6, 9]
# NS = {
#     5: "inf",
#     6: "inf",
#     9: "inf"
# }
# D = [2, 3, 4]
# ND = {
#     2: 20,
#     3: 10,
#     4: 20,
#     5: 0,
#     6: 0,
#     7: 0,
# }
# R = [7, 6, 5, 4, 3, 2]

def getC(l):
    l = list(set([k for k in D if k < l]))
    l.sort(reverse=True)
    return l

def getB(l):
    l = list(set([k for k in D if (k + l) in (S + R)]))
    l.sort(reverse=True)
    return l

variables = []

z = []

for l in S:
    y1 = []
    for k in getC(l):
        y1.append(f"y{l}_{k}")

    y2 = []
    for k in getB(l):
        y2.append(f"y{k+l}_{k}")

    y1.sort(reverse=True)
    y2.sort(reverse=True)
    variables = variables + y1 + y2
    z.append(str(l) + " " + f" + {str(l)} ".join(y1) + (f" - {str(l)} " if len(y2) > 0 else "") + f" - {str(l)} ".join(y2))

z = " + ".join(z)

def getA(l):
    l = list(set([k for k in (S + R) if k > l and l in D]))
    l.sort(reverse=True)
    return l

r = []

# restrições de quantidade de contentores

for l in S:
    y1 = []
    for k in getC(l):
        y1.append(f"y{l}_{k}")

    y2 = []
    for k in getB(l):
        y2.append(f"y{k+l}_{k}")

    y1.sort(reverse=True)
    y2.sort(reverse=True)
    variables = variables + y1 + y2
    if str(NS[l]) != "inf":
        r.append(" + ".join(y1) + (" - " if len(y2) > 0 else "") + " - ".join(y2) + " <= " + str(NS[l]))

# restrições de quantidade de itens

for l in set([i for i in (D + R) if i not in S]):
    y1 = []
    for k in getA(l):
        y1.append(f"y{k}_{l}")
    for k in getB(l):
        y1.append(f"y{k+l}_{k}")

    y2 = []
    for k in getC(l):
        y2.append(f"y{l}_{k}")

    y1.sort(reverse=True)
    y2.sort(reverse=True)
    variables = variables + y1 + y2
    r.append(" + ".join(y1) + (" - " if len(y2) > 0 else "") + " - ".join(y2) + " >= " + str(ND[l]))

r = ";\n".join(r) + ";"

res = ""

res += f"/* MINIMIZE: */\n\nmin: {z};\n\n/* SUBJECT TO: */\n\n{r}"

filtered_variables = list(set([v for v in variables if v[0] == "y"]))
filtered_variables.sort(reverse=True)

# more_than_zero = " >= 0;\n".join(filtered_variables) + " >= 0;"
res += f"\n\n/* --- */\n\n"
res += f"int {', '.join(filtered_variables)};"

with open("input.lp", "w") as f:
    f.write(res)

print("\nREDUNDANT VARIABLES:\n")

for v in filtered_variables:
    for sv in [sv for sv in filtered_variables if (sv.split("y")[1].split("_")[0] == v.split("y")[1].split("_")[0]) and (sv.split("y")[1].split("_")[1] < v.split("y")[1].split("_")[1])]:
        if int(sv.split("y")[1].split("_")[0]) - int(sv.split("y")[1].split("_")[1]) == int(v.split("y")[1].split("_")[1]):
            print(f"{sv} (Same as {v})")
