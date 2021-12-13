from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
url = "https://dizipal107.com/film/"
Names_list=[]
Genres= []
Time = []
Year = []
View = []
Imdp_Point = []
Directors = []
Actors = []

class Finder:
    def __init__(self,url):
        self.url = url
        self.max_page_num = self.find_max_pages_num()
        self.page_num = 1
        self.page_datas()

    def find_max_pages_num(self):
        r = requests.get(self.url)
        datas = BeautifulSoup(r.content, "html.parser")
        datas = datas.find_all(class_="page-link")
        max_num = 0
        for i in datas:
            num = int(i.text)
            if num >= max_num:
                max_num=num
        return max_num
    def new_page(self):
        self.page_num +=1
        url = "https://dizipal107.com/film/"
        self.url = url + "page/" + str(self.page_num)
        if self.page_num - 1 == self.max_page_num :
            pass
        else:
            print(f"NEW PAGES Page is {self.page_num}")
            self.page_datas()

    def page_datas(self):
        time.sleep(1)
        r = requests.get(self.url)
        datas = BeautifulSoup(r.content, "html.parser")

        datas = datas.find(class_='aa-cn')
        datas = datas.find_all("li")
        for data in datas:
            new_link = data.find(class_="lnk-blk")
            movie_url = new_link.get("href")
            self.movie_data(movie_url)
        self.new_page()
    def movie_data(self,movie_url):
        r = requests.get(movie_url)
        datas = BeautifulSoup(r.content, "html.parser")
        name_of_movie = datas.find(class_="entry-title").text
        try:
            genres = datas.find(class_="genres").text
            time_of_movie = datas.find(class_="duration fa-clock far").text
            year_of_movie = datas.find(class_="year fa-calendar far").text
            view = datas.find(class_="views fa-eye far").text
            imdb_point = datas.find(class_="num").text
            print(name_of_movie)
            print(genres)
            print(time_of_movie)
            print(year_of_movie)
            print(view)
            print(imdb_point)

        except Exception:
            genres = ""
            time_of_movie = ""
            year_of_movie = ""
            view = ""
            imdb_point =""
        new_data = datas.find(class_="cast-lst dfx fwp")
        directors_list = []
        actors_list = []
        try:
            new_data = new_data.find_all("li")
            time = 0

            for i in new_data:
                time+=1
                if time == 1:
                    directors = i.find_all("p")
                    for director in directors:
                        directors_list.append(director.text)
                elif time == 2:
                    actors = i.find_all("p")
                    for actor in actors:
                        actors_list.append(actor.text)
            print(directors_list)
            print(actors_list)
            print("\n")
            Names_list.append(name_of_movie)
            Genres.append(genres)
            Time.append(time_of_movie)
            Year.append(year_of_movie)
            View.append(view)
            Imdp_Point.append(imdb_point)
            Directors.append(directors_list)
            Actors.append(actors_list)
        except Exception:
            Names_list.append(name_of_movie)
            Genres.append(genres)
            Time.append(time_of_movie)
            Year.append(year_of_movie)
            View.append(view)
            Imdp_Point.append(imdb_point)
            Directors.append(directors_list)
            Actors.append(actors_list)
            print(directors_list)
            print(actors_list)
            print("\n")
Finder(url)
dataframe = {"Name":Names_list,
        "Genres":Genres,
        "Time":Time,
        "Year":Year,
        "View":View,
        "Imdp Point":Imdp_Point,
        "Directors":Directors,
        "Actors":Actors}

data = pd.DataFrame(dataframe)
data.to_csv('movies.csv', index=False)
