import requests
from bs4 import BeautifulSoup
import pandas as pd

candidates_xml = requests.get("https://interactives.stuff.co.nz/election-data/2023/xml/candidates.xml")
parties_xml = requests.get("https://interactives.stuff.co.nz/election-data/2023/xml/parties.xml")
electorates_xml = requests.get("https://interactives.stuff.co.nz/election-data/2023/xml/electorates.xml")
electorate_regions_json = requests.get(
    "https://interactives.stuff.co.nz/staging/2023-elec-staging/data/electorate-regions.json")


def parse_candidates_xml(xml_data):
    soup = BeautifulSoup(xml_data, "xml")

    df = pd.DataFrame(columns=["candidate_number", "name", "electorate", "party", "list_number"])

    all_candidates = soup.find_all("candidate")

    for index, item in enumerate(all_candidates):
        candidate_number = item["c_no"]
        name = item.find("candidate_name").text
        electorate = item.find("electorate").text
        party = item.find("party").text
        list_number = item.find("list_no").text

        row = {
            "candidate_number": candidate_number,
            "name": name,
            "electorate": electorate,
            "party": party,
            "list_number": list_number
        }

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    return df


def parse_parties_xml(xml_data):
    soup = BeautifulSoup(xml_data, "xml")

    df = pd.DataFrame(columns=["party_number", "abbreviation", "short_name", "party_name", "registered"])

    all_parties = soup.find_all("party")

    for index, item in enumerate(all_parties):
        party_number = item['p_no']
        abbreviation = item.find("abbrev").text
        short_name = item.find("short_name").text
        party_name = item.find("party_name").text
        registered = item.find("registered").text

        row = {
            "party_number": party_number,
            "abbreviation": abbreviation,
            "short_name": short_name,
            "party_name": party_name,
            "registered": registered
        }

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    return df


def parse_electorate_statistics_xml(xml_data, electorate_number):

    electorate_statistics_df = pd.DataFrame(columns=["total_voting_places",
                                                     "total_voting_places_counted",
                                                     "percent_voting_places_counted",
                                                     "total_votes_cast",
                                                     "percent_votes_cast",
                                                     "total_party_informals",
                                                     "total_candidate_informals",
                                                     "total_registered_parties",
                                                     "total_candidates"])

    row = {
        "total_voting_places": xml_data.find("total_voting_places").text,
        "total_voting_places_counted": xml_data.find("total_voting_places_counted").text,
        "percent_voting_places_counted": xml_data.find("percent_voting_places_counted").text,
        "total_votes_cast": xml_data.find("total_votes_cast").text,
        "percent_votes_cast": xml_data.find("percent_votes_cast").text,
        "total_party_informals": xml_data.find("total_party_informals").text,
        "total_candidate_informals": xml_data.find("total_candidate_informals").text,
        "total_registered_parties": xml_data.find("total_registered_parties").text,
        "total_candidates": xml_data.find("total_candidates").text
    }

    electorate_statistics_df = pd.concat([electorate_statistics_df, pd.DataFrame([row])], ignore_index=True)

    electorate_statistics_df.to_csv(electorate_number+".csv", index=False)


def parse_specific_electorate_xml(xml_data, electorate_number):
    soup = BeautifulSoup(xml_data, "xml")
    electorate_statistics_xml = soup.find("statistics")

    parse_electorate_statistics_xml(electorate_statistics_xml, electorate_number)

    # electorate_party_votes_df = pd.DataFrame(columns=["party_number",
    #                                                   "votes"])
    #
    # electorate_candidate_votes_df = pd.DataFrame(columns=["candidate_number",
    #                                                       "votes"])


def parse_electorates_xml(xml_data):
    soup = BeautifulSoup(xml_data, "xml")

    df = pd.DataFrame(columns=["electorate_number", "electorate_name"])

    all_electorates = soup.find_all("electorate")

    for index, item in enumerate(all_electorates):
        electorate_number = item['e_no']
        electorate_name = item.find("electorate_name").text

        row = {
            "electorate_number": electorate_number,
            "electorate_name": electorate_name,
        }

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)


        electorate_number_to_search = ""
        if int(electorate_number) < 10:
            electorate_number_to_search = "e0" + electorate_number
        else:
            electorate_number_to_search = "e" + electorate_number

        specific_electorate_url = "https://interactives.stuff.co.nz/election-data/2023/xml/" + electorate_number_to_search + "/" + electorate_number_to_search + ".xml"
        specific_electorate_xml = requests.get(specific_electorate_url)

        parse_specific_electorate_xml(specific_electorate_xml.content, electorate_number_to_search)

    return df


# candidates_df = parse_candidates_xml(candidates_xml.content)
# candidates_df.to_csv("candidates.csv", index=False)
#
# parties_df = parse_parties_xml(parties_xml.content)
# parties_df.to_csv("parties.csv", index=False)

electorates_df = parse_electorates_xml(electorates_xml.content)
electorates_df.to_csv("electorates.csv", index=False)
