import requests
import pickle
import datetime
import os
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show

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
    with open('summoner_scores/' + name + '.pkl', 'rb') as f:
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
    for file_name in os.listdir("summoner_scores"):
        single_dict = load_obj(file_name)



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
    get_leader_board()
