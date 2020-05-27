import sqlite3

# connect to database
conn = sqlite3.connect('spider2.sqlite')
cur = conn.cursor()

# obtain the webs that have both "in" and "out"
# Create a from_id list
cur.execute('SELECT DISTINCT from_id FROM Links')
fromid = []
for item in cur:
    fromid.append(item[0])

# Find the sets of webs from Links where they have both "in" and "out"
cur.execute('SELECT DISTINCT from_id,to_id FROM Links')
toid = []
links = []
for item in cur:
    from_id = item[0]
    to_id = item[1]

    if to_id == from_id:
        continue
    if from_id not in fromid:
        continue
    if to_id not in fromid:
        continue
    links.append(item)
    if to_id not in toid:
        toid.append(to_id)

# get the new rank corresponding to from_id, and put it to oldrank dic
oldrank = {}
for item in fromid:
    cur.execute('SELECT new_rank FROM Pages WHERE id = ? ', (item,))
    row = cur.fetchone()
    oldrank[item] = row[0]

# Double check if there is anything in oldrank
if len(oldrank) < 1:
    print('Something wrong, no data in oldrank')
    quit()

# the number of iterations:
num = input('How many interations?')
if len(num) < 1:
    num = 1
num = int(num)

# Update the page rank:
for i in range(num):
    newrank = {}
    tot = 0
    for (id,old_rank) in list(oldrank.items()):
        newrank[id] = 0.0
        tot = tot + old_rank

    for (id,old_rank) in list(oldrank.items()):
        outlink = []
        for (from_id,to_id) in links:
            if id != from_id:
                continue
            if to_id not in toid: 
                continue
            outlink.append(to_id)
        if len(outlink) < 1:
            continue
        # print(count)
        # print(outlink)
        portion = old_rank/len(outlink)
        # print('portion:', portion)

        for item in outlink:
            newrank[item] = newrank[item] + portion
        
    # find evaporation:
    newtot = 0
    for (id,new_rank) in list(newrank.items()):
        newtot = newtot + new_rank
    evap = (tot-newtot)/len(newrank)    

    for item in newrank:
        newrank[item] = newrank[item] + evap

    # compute the updated newtot to verify if it is equal to tot
    newtott = 0
    for (id,new_rank) in list(newrank.items()):
        newtott = newtott + new_rank
    # print('Old tot and new tot: ', tot, newtott) 

    # Dertermine the changes of this iterations
    totdiff = 0
    for (id,old_rank) in list(oldrank.items()):
        diff = abs(old_rank - newrank[id])
        totdiff = totdiff + diff

    avediff = totdiff / len(oldrank)
    print(i+1, avediff)

    # Update the newrank and oldrank
    oldrank = newrank

# Update the database
print(list(newrank.items())[:5])
cur.execute('UPDATE Pages SET old_rank=new_rank')
for (id,new_rank) in list(newrank.items()):
    cur.execute('''UPDATE Pages SET new_rank = ? WHERE id = ?''', 
                (new_rank, id))
conn.commit()
cur.close()







