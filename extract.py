"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neo_data = []
    with open(neo_csv_path) as neo_csv:
        neo_reader = csv.reader(neo_csv)
        next(neo_reader)
        for neo in neo_reader:
            neo_data.append(NearEarthObject(neo[3], neo[4], neo[15], neo[7]))
    return neo_data


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    close_approach_data = []
    with open(cad_json_path) as cad_json:
        cad_reader = json.load(cad_json)
        for close_approach in cad_reader['data']:
            close_approach_data.append(CloseApproach(close_approach[0], close_approach[3], close_approach[4], close_approach[7]))
    return close_approach_data
