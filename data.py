import sqlite3
import pandas as pd

from page_rank import PageRank

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

sql_request_matches =  "SELECT * FROM Match WHERE country_id=4769 AND season='2011/2012'"
data_matches = pd.read_sql_query(sql_request_matches, conn)
table_matches = data_matches.as_matrix(["home_team_api_id", "away_team_api_id", "home_team_goal", "away_team_goal"])

sql_request_teams = "SELECT * FROM Team"
data_teams = pd.read_sql_query(sql_request_teams, conn)
table_teams = data_teams.as_matrix(["team_api_id", "team_long_name", "team_short_name"])

dic_teams = {}
matches = []

for l in table_matches:
    temp = []
    try:
        temp.append(dic_teams[l[0]])
    except:
        for i in table_teams:
            if i[0] == l[0]:
                dic_teams[l[0]]=i[1]
                temp.append(i[1])
                break
    try:
        temp.append(dic_teams[l[1]])
    except:
        for i in table_teams:
            if i[0] == l[1]:
                dic_teams[l[1]]=i[1]
                temp.append(i[1])
                break
    temp.append(l[2])
    temp.append(l[3])
    print(temp)
    matches.append(temp)

nodes = []
vertex=[]

for l in matches:
    try:
        nodes.index(l[0])
    except:
        nodes.append(l[0])
    try:
        nodes.index(l[1])
    except:
        nodes.append(l[1])
    if l[2]>l[3]:
        vertex.append((l[1], l[0]))
    elif l[3]>l[2]:
        vertex.append((l[0], l[1]))

pageRank = PageRank(nodes, vertex)
classment = pageRank.iterate(100)


print(classment)

pageRank.export_graph("datas.json")
