import datetime


class CricketPlayer:
    def __init__(self, fname, lname,birth_year,team):
        self.fname = fname
        self.lname = lname
        self.birth_year = birth_year
        self.team = team
        self.score = []
    def add_score(self, score):
        self.score.append(score)

    def average_score(self):
        return sum(self.score)/len(self.score)
    def age(self):
        return datetime.datetime.now().year - self.birth_year

    def __str__(self):
        return f" Name : {self.fname} {self.lname} Team : {self.team} Age : {self.age()}"

virat = CricketPlayer("Virat","Virat",1999,1)
virat.add_score(10)
virat.add_score(20)
virat.add_score(30)
virat.add_score(40)
print(virat.average_score())
print(virat)
rohit = CricketPlayer("Rohit","Rohit",1999,2)