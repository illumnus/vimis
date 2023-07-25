with open("MGI_unsuccess.txt", "r") as f:
    MGI_unsuccess = f.read().split("\n")
    for i in range(len(MGI_unsuccess)):
        MGI_unsuccess[i] = MGI_unsuccess[i].split("\t")
with open("TMC_unsuccess.txt", "r") as f:
    TMC_unsuccess = f.read().split("\n")
    for i in range(len(TMC_unsuccess)):
        TMC_unsuccess[i] = TMC_unsuccess[i].split("\t")

diff = []
for i in TMC_unsuccess:
    a = False
    for j in MGI_unsuccess:
        if i[0] in j:
            a = True
    if a is False:
        diff.append(i)
print(diff)