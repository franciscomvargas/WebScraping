import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv
import pandas as pd

from termcolor import colored

import matplotlib.pyplot as plt
import numpy as np
import datetime

@dataclass
class Pull:
    Date: str
    Price: str
    Ball_1: int
    Ball_2: int
    Ball_3: int
    Ball_4: int
    Ball_5: int
    L_Ball: int
    Sum: int    

def get_html(year):
    url = f'https://www.lotto.net/lucky-for-life/numbers/{year}'
    resp = httpx.get(url)
    if resp.status_code != 200:
        print(colored("Page request error: " + str(resp), 'red'))
        return 'error'

    print(colored("Page request sucess: " + str(resp), 'green'))
    return resp.text

def write_html_page(file_name, source_page):
    with open(f'.data/{file_name}.html', 'w') as fw:
        fw.writelines(source_page)
    fw.close()
def read_html_page(file_name):
    with open(f'.data/{file_name}.html', 'r') as fr:
        source = fr.readlines()
    fr.close()

    return "\n".join(source)

def parse_pulls(html):
    try:
        html = HTMLParser(html)
        pulls = html.css('#content > div.archive-container > div:nth-child(n)')
        results = []
        for item in pulls:
            balls = item.css_first('ul.balls').text().split()
            new_item = Pull(
                Date = item.css_first('div.date').text().strip().replace(item.css_first('div.date span').text(), ''),
                Price = item.css_first('div.jackpot span').text().strip()[1:].strip(),
                Ball_1 = int(balls[0]),
                Ball_2 = int(balls[1]),
                Ball_3 = int(balls[2]),
                Ball_4 = int(balls[3]),
                Ball_5 = int(balls[4]),
                L_Ball = int(balls[5][:-1]),
                Sum =  int(balls[0]) + int(balls[1]) + int(balls[2]) + int(balls[3]) + int(balls[4]) + int(balls[5][:-1])
            )
            results.append(asdict(new_item))
        print(colored("Sucess parsing page data", 'green'))
    except Exception as e:
        print(colored("Error parsing page data: " + e, 'red'))
        return []


    return results

def to_csv(data, file_name):
    with open(f'{file_name}.csv', 'w') as fa:
        writer = csv.writer(fa, lineterminator='\n')
        writer.writerow(data[0].keys())
        writer = csv.DictWriter(fa, fieldnames=data[0].keys(), lineterminator='\n')
        writer.writerows(data)

# Data process Functions
def moooeeeep(l):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in l if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )

def process_lotto_data(balls_data_year1, balls_data_year2, year1, year2):
    sum1 = []
    sum2 = []
    timestamp1 = []
    timestamp2 = []
    for data_1 in balls_data_year1:
        timestamp1.insert(0, int(round(datetime.datetime.strptime(data_1['Date'], '%B %d %Y').timestamp())))
        sum1.insert(0, data_1['Sum'])
    
    sum1_dup = moooeeeep(sum1)
    sum1_uniq = list(set(sum1))
    sum1_rep = []
    for s1 in sum1_uniq:
        if s1 in sum1_dup:
            sum1_rep.append(sum1.count(s1))
            continue
        sum1_rep.append(1)


    for data_2 in balls_data_year2:
        timestamp2.insert(0, int(round(datetime.datetime.strptime(data_2['Date'], '%B %d %Y').timestamp())))
        sum2.insert(0, data_2['Sum'])


    plt.subplot(2, 1, 2)
    xpoints1uniq = np.array(sum1_uniq)
    ypoints1rep = np.array(sum1_rep)
    plt.bar(xpoints1uniq,ypoints1rep, color= "#4CAF50")
    plt.title("Sum of Lotto balls values", loc = 'left')
    plt.xlabel(f"{year1} Lotto Unique Sums")
    plt.ylabel(f"{year1} Lotto Sum Repetitions")

    
    if len(sum1) >= len(sum2):
        xpoints1 = np.array(timestamp1)
        ypoints1 = np.array(sum1)
        ypoints2 = np.array(sum2)
    else:   # all this becouse 2nd scatter xpoints1[:len(ypoints2)]
        xpoints1 = np.array(timestamp2)
        ypoints1 = np.array(sum2)
        ypoints2 = np.array(sum1)
        tmpyear = year1
        year1 = year2
        year2 = tmpyear
        del tmpyear

    plt.subplot(2, 1, 1)
    plt.scatter(xpoints1, ypoints1, color='blue')
    plt.scatter(xpoints1[:len(ypoints2)], ypoints2, color='orange')
    plt.legend([f'{year1}', f'{year2}'], loc ="lower right")
    plt.title(f"Sum of Lotto balls values in {year1}/{year2}", loc = 'left')
    plt.xlabel(f"{year1} Lotto TimeStamps")
    
    plt.show()


def main():
    years = [2022, 2023]

    '''#Pull data from web
    html_year1 = get_html(years[0])
    html_year2 = get_html(years[1])
    if html_year1 == 'error' or html_year2 == 'error':
        return
    write_html_page(years[0], html_year1)
    write_html_page(years[1], html_year2)'''
    

    #Pull data html file
    html_year1 = read_html_page(years[0])
    html_year2 = read_html_page(years[1])
    
    balls_data_year1 = parse_pulls(html_year1)
    balls_data_year2 = parse_pulls(html_year2)
    if balls_data_year1 == [] or balls_data_year2 == []:
        return
    
    #Extract data 
    # as csv:
    to_csv(balls_data_year1, years[0])
    to_csv(balls_data_year2, years[1]) 
    # as xlsx | excel
    df_balls_year1 = pd.DataFrame(data=balls_data_year1)
    df_balls_year2 = pd.DataFrame(data=balls_data_year2)
    df_balls_year1.to_excel(f"{years[0]}.xlsx", index=False)
    df_balls_year2.to_excel(f"{years[1]}.xlsx", index=False)
    
    
    #Process Data
    process_lotto_data(balls_data_year1, balls_data_year2, years[0], years[1])

if __name__ == '__main__':
    main()
