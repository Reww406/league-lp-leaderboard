import requests
import pickle
import datetime
import os
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category20

tier_points = {
    "IRON": 0,
    "BRONZE": 400,
    "SILVER": 800,
    "GOLD": 1200
}
rank_points = {
    "I": 299,
    "II": 200,
    "III": 100,
    "IV": 0
}

ranks_tags = {
    0: "Iron",
    400: "Bronze",
    800: "Silver",
    1200: "Gold"
}

api_token = ""
summoner_names: dict = {
    "Gaziibo": "jnegFz8Qt2SKpXkU0UQ7uyeo04xuHIzHTozGpD4paLnhHY8",
    "Yosh710": "qrkYHRZgRqpsWgr9UZx9h8ZAQz_kzdWTiR6VMXs_vi0jLCi_",
    "Drizzy0415": "FLPg43L1a2HpfDLS9wmcAmNyCeNytuilKprYmPo-eUBmwTS3",
    "Hairy Pooner": "HvXunAyiAxdOb3aAuDdpCLq2SESgnVAOAKxTXtnkbBFwJtvqgSRvYkcvyQ",
    "BigDevInDaHouse": "99-XRTbz3l94Pvhw74QeV8DtM8ysjpU73HQMBVatDx4PPZOl",
    "Griffiniti": "cwI_NPdAAZrejdLDCgtXu9WPJGwxeT54gbFj_jtUUmXdzoUF",
    "TheP1ckl3r": "5qFSxAufMIF07G2c9UI_cPinCOdQmnaZraRGUSwXTHs8lRye",
    "YourDadsFist": "sXxXFZ1Geb97Arzcr4L6IZJmnr-Jal_TOpsixX0XKGi8ViZR",
    "SlootDragoon": "zAu5V-jMB5wFaesaPdbfkAb87Y_9c3foQNvjyedlyH4h3ufR",
    "somdee": "mvFzy02VKGYtI7RqZOQK9pAxlH_obNk9Uji9nvcZIXPOIBg",
    "BZuke": "kDX-noD02l7jTpVmuceZwQWY8RbmpqEMDVj3CEm8SHw_SmA"
}

requests_headers = {
    "X-Riot-Token": api_token
}


def save_obj(obj, name):
    with open('summoner_scores/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('summoner_scores/' + name, 'rb') as f:
        return pickle.load(f)


def get_leader_board():
    summoner_names_total_score = dict()
    for key in summoner_names:
        print("Getting: " + key + " score")
        ranked_response = requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"
                                       .format(id=summoner_names[key]), headers=requests_headers)

        ranked_response_json = ranked_response.json()
        summoner_total_score = calculate_rank_score(ranked_response_json[0]["leaguePoints"],
                                                    ranked_response_json[0]["tier"], ranked_response_json[0]["rank"])

        summoner_names_total_score[key] = summoner_total_score

    print(summoner_names_total_score)
    save_obj(summoner_names_total_score, "summoner_names_total_score-" + str(datetime.date.today()))
    plot_ranks()


def load_rank_and_time():
    total_scores = dict()
    for file_name in os.listdir("summoner_scores"):
        print(file_name)
        lp_date = file_name[file_name.find("-") + 1: file_name.find(".")]
        print(lp_date)
        summoner_scores: dict = load_obj(file_name)
        total_scores[lp_date] = summoner_scores

    for date in total_scores.keys():
        print(date + " " + str(total_scores.get(date)))

    return total_scores


def plot_history_graph(rank_history: dict):
    print(rank_history)
    summoner_points: list = list()
    for date in rank_history.keys():
        summoner_league_points: dict = rank_history.get(date)
        summoner_points.append(list(summoner_league_points.values()))
    xs = list(rank_history.keys())
    print("summoner " + str(len(summoner_points)))
    graph = figure(title="History of LP", x_range=xs, width=1000, height=700)
    one_user = list()
    first_date = list(rank_history.keys())[0]
    summoner_names: list = list(rank_history.get(first_date).keys())
    print("names" + str(summoner_names))
    print(str(Category20))
    i = 0
    for x in range(len(summoner_points[0])):
        one_users_score = list()
        for lp_score in summoner_points:
            lp_score: list
            one_users_score.append(lp_score[i])
        print("one users score: " + str(one_users_score))
        print("dates: " + str(xs))
        graph.line(y=one_users_score, x=xs, name=summoner_names[x], width=2.5,
                   legend_label=summoner_names[x], color=Category20[len(summoner_names)][x])
        i += 1
    graph.add_layout(graph.legend[0], 'right')
    show(graph)


def repeat_dates_list(dates_list: list):
    date_list_of_list = list()
    for x in range(len(dates_list)):
        date_list_of_list.append(dates_list)
    print("Repeated Date List" + str(date_list_of_list))


def plot_ranks():
    graph_name = "The Family Ranked Leader Board - " + str(datetime.date.today())
    summoner_names_total_score: dict = load_obj("summoner_names_total_score-" + str(datetime.date.today()))
    summoner_names_total_score = dict(sorted(summoner_names_total_score.items(), key=lambda item: item[1]))
    print(type(summoner_names_total_score.keys()))
    plot = figure(x_range=list(summoner_names_total_score.keys()),
                  plot_width=1200, plot_height=800, x_axis_label="Summoner Name",
                  y_axis_label="Total LP", title=graph_name)
    curdoc().theme = 'dark_minimal'

    plot.circle_dot(list(summoner_names_total_score.keys()),
                    list(summoner_names_total_score.values()),
                    size=20, color="#ff9bff", hatch_color="#DDA0DD")
    show(plot)


def calculate_rank_score(league_points: int, tier: str, rank: str):
    total_score = 0
    total_score += league_points
    total_score += rank_points[rank]
    total_score += tier_points[tier]
    return total_score


if __name__ == '__main__':
    # get_leader_board()
    plot_history_graph(load_rank_and_time())
