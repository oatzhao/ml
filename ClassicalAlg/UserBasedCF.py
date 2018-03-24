#-*-coding:utf-8-*-

import sys
import math
from texttable import Texttable

#cos
def getcosDist(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    for key1 in user1:
        for key2 in user2:
            sum_x += key1[1] * key1[1]
            sum_y += key2[1] * key2[1]
            sum_xy += key1[1] * key2[1]

    if sum_xy == 0.0:
        return 0
    demo = math.sqrt((sum_x * sum_y))
    return sum_xy / demo

#read
def readFile(filename):
    f = open(filename, "r")
    contents = f.readlines()
    f.close()
    return contents

#array
def getRatingInfo(ratings):
    rates = []
    i = 0
    for line in ratings:
        if i ==0:
            pass
        else:
            rate = line.split(",")
            rates.append([int(rate[0]), int(rate[1]), float(rate[2])])
        i+=1
    return rates

#score
def getUserScoeDataStructure(rates):
    #userDict[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
    userDict = {}
    #itemUser={31:[1,2,56,……]}表示1，2，56 ……用户都看过电影31
    itemUser = {}
    for k in rates:
        user_rank = (k[1], k[2])
        if k[0] in userDict:
            userDict[k[0]].append(user_rank)
        else:
            userDict[k[0]] = [user_rank]

        if k[1] in itemUser:
            itemUser[k[1]].append(k[0])
        else:
            itemUser[k[1]] = [k[0]]
    return userDict, itemUser

#neighbor
def getNearestNeighbor(userId, userDict, itemUser):
    #user1看到1，2，3 电影，同样看过1电影的还有user8，user9用户，同样看过2点用的还有user3、user4用户
    #那么user1的neighbors是【user8,user9,user3,user4】
    neighbors = []
    for item in userDict[userId]:
        for neighbor in itemUser[item[0]]:
            if neighbor != userId and neighbor not in neighbors:
                neighbors.append(neighbor)

    #通过余弦相似求user1和neigbors中每个其他用户的相似度
    #neighbors_dist=[[9,user8],[7,user2],……]
    neighbors_dist = []
    for neighbor in neighbors:
        dist = getcosDist(userDict[userId], userDict[neighbor])
        neighbors_dist.append([dist, neighbor])
    neighbors_dist.sort(reverse=True)
    return neighbors_dist

#UserFC
def recommendByUserFC(filename, userId, k = 5):
    contents = readFile(filename)
    rates = getRatingInfo(contents)
    userDict, itemUser = getUserScoeDataStructure(rates)
    neighbors = getNearestNeighbor(userId, userDict, itemUser)

    recommand_dict = {}
    for neighbor in neighbors:
        neighbor_user_id = neighbor[1]
        movies = userDict[neighbor_user_id]
        for movie in movies:
            if movie[0] not in recommand_dict:
                recommand_dict[movie[0]] = neighbor[0]
            else:
                recommand_dict[movie[0]] += neighbor[0]

    recommand_list = []
    for key in recommand_dict:
        recommand_list.append([recommand_dict[key], key])
    recommand_list.sort(reverse=True)
    user_movies = [k[0] for k in userDict[userId]]
    return [k[1] for k in recommand_list], user_movies, itemUser, neighbors

def getMovieList(filename):
    i = 0
    contents = readFile(filename)
    movies_info = {}
    for movie in contents:
        if i == 0:
            pass
        else:
            single_info = movie.split(",")
            movies_info[int(single_info[0])] = single_info[1:]
        i += 1
    return movies_info


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    # 获取所有电影的列表
    movies = getMovieList("movies.csv")
    recommend_list, user_movie, items_movie, neighbors = recommendByUserFC("ratings.csv", 50, 80)
    neighbors_id = [i[1] for i in neighbors]
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(["l", "l", "l"])
    rows = []
    rows.append([u"movie name", u"release", u"from userid"])
    for movie_id in recommend_list[:20]:
        from_user = []
        for user_id in items_movie[movie_id]:
            if user_id in neighbors_id:
                from_user.append(user_id)
        rows.append([movies[movie_id][0], movies[movie_id][1], from_user])
    table.add_rows(rows)
    print table.draw()

