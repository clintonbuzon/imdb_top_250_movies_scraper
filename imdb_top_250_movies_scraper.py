#python prerequisites
#pip install requests
#pip install bs4

import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
import os

#parameters to change
imdb_link="https://www.imdb.com"
imdb_charts_link="https://www.imdb.com/chart/top"
file_name = 'test.csv'

# Function to append rows to a CSV file
def append_csv_row(local_file, data):
	with open(file_name, 'a', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(data)
	csvFile.close()
		
# Function to scrape additional data of a movie using a link
def get_movie_details(movie_link):
	response = requests.get(movie_link)
	soup = BeautifulSoup(response.text, "html.parser")

	description = soup.find("div", attrs={"class":"summary_text"}).get_text("|", strip=True)
	director = soup.find("div", attrs={"class":"credit_summary_item"}).get_text("|", strip=True).split("|")[1]
	
	header_details = soup.find("div", attrs={"class":"subtext"}).get_text(strip=True).split("|")
	rating = header_details[0]
	runtime = header_details[1]
	genres = header_details[2]
	imdb_score = soup.find("span", attrs={"itemprop":"ratingValue"}).get_text(strip=True)
	
	movie_details = [description,director,rating,runtime,genres]
	return movie_details


# Main

# Append first row to csv which will contain header details
column_list = ["rank","title","title_details","link","description","director","rating","runtime","genres"]
append_csv_row(file_name,column_list)

#capture chart page details
response = requests.get(imdb_charts_link)
soup = BeautifulSoup(response.text, "html.parser")

#scrape details for each movie on chart
for movie in soup.findAll("td", attrs={"class":"titleColumn"}):
	title_details = movie.get_text("|", strip=True).split("|")
	rank = title_details[0].replace(".","")
	title = title_details[1]
	title_date = title_details[2]
	link = imdb_link + "/" + movie.a.get('href')
	csv_row = [rank,title,title_date,link]
	csv_row.extend(get_movie_details(link))
	print(csv_row)
	append_csv_row(file_name,csv_row)