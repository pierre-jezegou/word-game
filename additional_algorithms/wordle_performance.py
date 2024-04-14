''' Aim of this file :
    - Use json export from wordle automatic mode
'''
import json
import numpy


def get_json(filename: str) -> list[dict[str|int|float]]:
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    print(data)
    return data

def extract_attempts_per_length(datas: dict[int|float|bool]) -> None:
    print("\nATTEMPTS")
    for i in range(3, 6):
        results = [0 for i in range(11)]
        print(f"----%d-----" % i)
        for data in datas:
            if data["size"] == i:
                results[data["attempts"]] += 1

        for k, value in enumerate(results):
            print("\t\t", (k, value))

def extract_cpu_time_per_length(datas: dict[int|float|bool]) -> None:
    print("\nCPU_TIME")
    for i in range(3, 6):
        print(f"----%d-----" % i)
        result_cpu = []
        for data in datas:
            if data["size"] == i:
                result_cpu.append([data["cpu_time"]])

        print("\t\t", (i, numpy.mean(result_cpu)))

extract_attempts_per_length(get_json('exports/automatic_wordle.json'))
extract_cpu_time_per_length(get_json('exports/automatic_wordle.json'))
