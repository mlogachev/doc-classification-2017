import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

base_path = "http://db.chgk.info"

def parse_page(link):
    full_path = "{}/{}".format(base_path, link)
    
    with requests.get(full_path) as page:
        soup = BeautifulSoup(page.text, "lxml")
        
    questions_from_page = []
        
    for even in tqdm(soup.findAll("tr", {"class": "even"})):
        tour_links = el.findChildren("td")[1].findAll("a")

        for l in tour_links:
            questions_from_page += parse_tour(l['href'])
            
    for odd in tqdm(soup.findAll("tr", {"class": "odd"})):
        tour_links = el.findChildren("td")[1].findAll("a")

        for l in tour_links:
            questions_from_page += parse_tour(l['href'])
            
    next_page = soup.find("li", {"class": "pager-next"}).find("a")['href']
            
    return questions_from_page, next_page

def parse_tour(link):
    full_path = "{}/{}".format(base_path, link)
    
    
    with requests.get(full_path) as page:
        page_soup = BeautifulSoup(page.text, "lxml")
        
    questions = []
    
    for q in page_soup.findAll("div", {"class": "question"}):
        question = q.findChildren("p")[0].get_text().strip().replace("\n", " ")
        
        wrapper = q.find("div", {"class": "collapsed"})
        paragraphs = wrapper.findAll("p")
        
        answer = paragraphs[0].get_text().strip().replace("\n", " ")
        author = paragraphs[-1].get_text().strip().replace("\n", " ")
        
        Q = {
            'question': question,
            'answer': answer,
            'author': author
        }
        questions.append(Q)
    
    return questions


if __name__ == "__main__":
    current_page = "last"

    all_questions = []

    while current_page is not None:
        print("Next page : {}".format(current_page))
        questions, current_page = parse_page(current_page)
        all_questions += questions
        break

    json.dump(all_questions, open("questions.json", "w"))