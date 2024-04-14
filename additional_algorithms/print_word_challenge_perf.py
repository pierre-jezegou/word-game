''' Aim of this file :
    - Use json export from word_challenge to plot performances charts/plots
'''
import json
import numpy as np
from jinja2 import Template

filename = "exports/export.json"
EXPORT_PATH = "documentation/images/visualizations/word_challenge_game_perf.tex"


def get_json(filename: str) -> list[dict[str|int|float]]:
    '''Retrieve json and parse it'''
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data

def gather_informations_per_length(word_length: int,
                                   datas: list[dict[str|int|float]],
                                   information: str
                                   ) -> tuple[int, float]:
    '''Gather counters per word length'''
    result = []

    for data in datas:
        if data['initial_word_length'] == word_length:
            result.append(data[information])

    return word_length, np.mean(result)



# print(gather_informations_per_length(6, get_json(filename), 'cpu_time'))
def gather_all_informations(information) -> str:
    points = ''
    for i in range(11):
        word_length, info = gather_informations_per_length(i, get_json(filename), information)

        if not np.isnan(info):
            points += str((word_length, info))

    return points



def print_infos_in_tikz(needed_informations = list[str],
                        different_axis: bool = False
                        ) -> None:

    with open('additional_algorithms/histograms.tex', 'r') as f:
        template_content = f.read()

    template = Template(template_content)
    legend = needed_informations[0]

    context = {
        'legend': r'\verb|%s|' % legend,
        'points': gather_all_informations(legend)
    }


    with open(EXPORT_PATH, 'w') as f:
        f.write(template.render(context))

# print_infos_in_tikz(['word_counter'])
print_infos_in_tikz(['cpu_time'])
