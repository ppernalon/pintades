# import const 


def suite(u_0, N):
    u_n=[u_0]
    for k in range(1, N+1): 
        if (k<=182):
            u_n.append(u_n[-1])
        if (k>182 and k%3==0):
            u_n.append(u_n[-1] + (u_n[len(u_n)-1-182])//2)
        else:
            u_n.append(u_n[-1])
    return(u_n[-1])

nber_pintades_initial= suite(2,728)

print(nber_pintades_initial)