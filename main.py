import argparse
import json
import time

import mysql.connector
import requests
from bs4 import BeautifulSoup
from progress.bar import ChargingBar, IncrementalBar

import vostree




def escape_column_name(name):
    return name.rstrip().lstrip().strip().replace("'", '"')


def get_html(link):
    html = requests.request("GET", link, headers={}, data={}).text.encode("utf8")
    return BeautifulSoup(html, "html.parser")


def get_type():
    cursor.execute("SELECT id,name FROM type")
    return cursor.fetchall()


def get_categorie_lang():
    cursor.execute("SELECT id,name FROM categorie_lang")
    return cursor.fetchall()


def get_lecteur():
    cursor.execute("SELECT id,name FROM lecteur")
    return cursor.fetchall()


def get_anime_by_name(name, saison):
    cursor.execute(
        f"SELECT anime.id, anime.name, anime.update FROM anime WHERE anime.name = '{name}' AND anime.saison = {saison};")
    return cursor.fetchall()


def get_all_episode(search, saison):
    anime = get_anime_by_name(search, saison)
    if len(anime):
        id_anime = anime[0][0]
        cursor.execute(f"SELECT COUNT(id) FROM episode WHERE episode.anime_id = {id_anime};")
        return cursor.fetchall()[0][0]
    return False


def type_update(types_f):
    update = []
    current_type = [x[1] for x in get_type()]
    for type_g in types_f:
        if type_g not in current_type:
            update.append((type_g,))
    if len(update):
        sql = "INSERT INTO type (name) VALUES (%s)"
        cursor.executemany(sql, update)
        mydb.commit()
    return get_type()


def categorie_lang_update(categories_lang_f):
    update = []
    current_catg_lg = [x[1] for x in get_categorie_lang()]
    for categories_lang_g in categories_lang_f:
        if categories_lang_g not in current_catg_lg:
            update.append((categories_lang_g,))
    if len(update):
        sql = "INSERT INTO categorie_lang (name) VALUES (%s)"
        cursor.executemany(sql, update)
        mydb.commit()
    return get_categorie_lang()


def lecteur_update(lecteur_f):
    update = []
    current_lecteur = [x[1] for x in get_lecteur()]
    for lecteur_g in lecteur_f:
        if lecteur_g not in current_lecteur:
            update.append((lecteur_g,))
    if len(update):
        sql = "INSERT INTO lecteur (name) VALUES (%s)"
        cursor.executemany(sql, update)
        mydb.commit()
    return get_lecteur()


def db_upload_anime(itm, bar):
    soup = get_html(itm["link"])

    bar.next()

    episode = vostree.get_all_player(soup)

    bar.next()

    if len(episode) != get_all_episode(itm["name"], itm["saison"]):
        print("passed : ", itm["name"])
        desc = soup.find("div", {"class": "slide-desc"}).text
        anime = get_anime_by_name(itm["name"], itm["saison"])

        bar.next()

        if not len(anime):
            sql = "INSERT INTO anime (anime.name, anime.image, anime.duree, anime.saison, anime.desc, anime.categorie_lang_id) VALUES (%s, %s, %s, %s, %s, %s);"
            val = (itm["name"], itm["image"], itm["duree"], itm["saison"], desc, itm["categorie_lang"])
            cursor.execute(sql, val)
            mydb.commit()

            id_anime = get_anime_by_name(itm["name"], itm["saison"])[0][0]

            sql = "INSERT INTO anime_has_type (anime_id, type_id) VALUES (%s, %s)"
            val = [(id_anime, x) for x in itm["type"]]
            cursor.executemany(sql, val)
            mydb.commit()

        bar.next()

        id_anime = get_anime_by_name(itm["name"], itm["saison"])[0][0]
        # print(itm["name"], id_anime)
        lecteur = {g[1]: g[0] for g in lecteur_update(list(set([x["title"] for i in episode for x in i["methode"]])))}
        # print(lecteur)

        bar.next()

        for i in episode:
            for x in i["methode"]:
                x["title"] = lecteur[x["title"]]

        cursor.execute(f"delete from episode where episode.anime_id = {id_anime};")
        mydb.commit()

        bar.next()

        # print(json.dumps(episode, sort_keys=True, indent=4, ensure_ascii=False))
        for i in episode:
            cursor.execute(f"set information_schema_stats_expiry = 0;")
            mydb.commit()
            sql = "SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_name = 'episode' AND table_schema = 'anime'"
            cursor.execute(sql)
            next_id = cursor.fetchall()[0][0]

            sql = "INSERT INTO episode (numero, anime_id) VALUES (%s, %s)"
            val = (i["title"], id_anime)
            cursor.execute(sql, val)
            mydb.commit()

            sql = "INSERT INTO episode_lecteur ( episode_id, lecteur_id, link) VALUES (%s, %s, %s)"
            val = [(next_id, x["title"], x["link"]) for x in i["methode"]]
            cursor.executemany(sql, val)
            mydb.commit()

        bar.next()
    else:
        for _ in range(5):
            bar.next()


if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(prog='vostree_scrap_new', description='Get new anime from vostree')
    my_parser.add_argument('-n', '--nbpage', metavar='nbpage', type=int, help='Number of pages that will be analyzed')
    my_parser.add_argument('-f', '--force', help="force update anime", action="store_true")
    my_parser.add_argument('-p', '--page', metavar='page', type=str, help='return episode of specified page')
    my_parser.add_argument('-o', '--output', metavar='output', type=str,
                           help='The output file of the page that will be analyzed, if it is not specified, the output will be on the command line')
    my_parser.add_argument('-a', '--alwaysup', help="run prgram, every hours", action="store_true")
    my_parser.add_argument('-t', '--time', type=int, metavar='time', help="every X hours program run. Default 1 hour")
    args = my_parser.parse_args()
    nb_page = args.nbpage
    page = args.page
    output = args.output

    always = args.alwaysup
    if args.time:
        hour = args.time
    else:
        hour = 1

    if page is not None:
        print(f"The page to analyze will be: {page}")
        if output is not None:
            print(f"file output : {output}")
        else:
            print(f"output: command line")
        site = vostree.get_all_player(get_html(page))
        if output is not None:
            with open(output, 'w') as jsonfile:
                json.dump(site, jsonfile, sort_keys=True, indent=4, ensure_ascii=False)
        else:
            print(json.dumps(site, sort_keys=True, indent=4, ensure_ascii=False))
        exit()

    if nb_page is None:
        print("usage: vostree_scrap_new [-h] [-n nbpage [-f/--force] [-a [-t hour]]] [-p page_link [-o output]]")
        print("vostree_scrap_new: error: the following arguments are required: -n/--nbpage or -p/--page")
        exit()

    mydb = mysql.connector.connect(
        host="<HOST>",
        port=<PORT>,
        user="<USER>",
        password="<USER_PWD>",
        database="<SCHEMA>"
    )
    mydb = mysql.connector.connect(

    while True:
        print(f"pages that will be analyzed: {nb_page}")
        if args.force:
            print(f"force mode activated")
        for x in range(1, nb_page + 1):
            anime_update = 0
            dico = []

            soup = get_html(f"https://vostfree.com/last-episode.html/page/{x}/")
            episode = soup.find_all("div", {"class": "last-episode"})

            bar = ChargingBar(f'page: {x}, nbAnime : {len(episode)}', max=6 + (len(episode) * 7))
            bar.next()

            for i in episode:
                dico.append({
                    "categorie_lang": escape_column_name(i.find("div", {"class": "quality"}).text),
                    "image": escape_column_name(i.find("span", {"class": "image"}).contents[0]["src"]),
                    "name": escape_column_name(i.find("div", {"class": "title"}).text),
                    "type": [escape_column_name(x.text) for x in i.find("li", {"class": "type"}).find_all("a")],
                    "saison": int(escape_column_name(i.find("div", {"class": "kp"}).find("b").text)),
                    "episode": int(escape_column_name(i.find("div", {"class": "year"}).find("b").text)),
                    "duree": escape_column_name(
                        i.find_all("i", {"class": "fa-clock-o"})[1].parent.text.replace('Durée:', '')),
                    "link": escape_column_name(i.find("div", {"class": "title"}).contents[0]["href"])
                })

            bar.next()

            types = {x[1]: x[0] for x in type_update(sorted(list(set([x for i in dico for x in i["type"]]))))}
            categorie_lang = {x[1]: x[0] for x in
                              categorie_lang_update(sorted(list(set([i["categorie_lang"] for i in dico]))))}

            bar.next()

            for i in range(len(dico)):
                dico[i]['type'] = [types[i] for i in dico[i]['type']]

            bar.next()

            for i in range(len(dico)):
                dico[i]['categorie_lang'] = categorie_lang[dico[i]["categorie_lang"]]

            bar.next()

            for item in dico:
                anime = get_all_episode(item["name"], item["saison"])
                if (anime is False) or (anime != item["episode"]) or args.force:
                    anime_update += 1
                    db_upload_anime(item, bar)
                else:
                    for i in range(7):
                        bar.next()
            bar.next()
            bar.finish()
            if always:
                print("\n")
                with IncrementalBar('Next scan : ', max=hour*60) as bar:
                    for i in range(hour*60):
                        # Do some work
                        bar.next()
                        time.sleep(60)
                print("\n")
            else:
                exit()
