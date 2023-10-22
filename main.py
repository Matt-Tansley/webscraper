import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import constant


def parse_candidates(candidates):
    candidates_soup = BeautifulSoup(candidates, "xml")

    candidates_df = pd.DataFrame(columns=["candidate_number", "name", "electorate", "party", "list_number"])

    all_candidates = candidates_soup.find_all("candidate")

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

        candidates_df = pd.concat([candidates_df, pd.DataFrame([row])], ignore_index=True)

    return candidates_df


def parse_parties(parties):
    parties_soup = BeautifulSoup(parties, "xml")

    parties_df = pd.DataFrame(columns=["party_number", "abbreviation", "short_name", "party_name", "registered"])

    all_parties = parties_soup.find_all("party")

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

        parties_df = pd.concat([parties_df, pd.DataFrame([row])], ignore_index=True)

    return parties_df


def parse_electorate_statistics(electorate_statistics, electorate_number):
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
        "total_voting_places": electorate_statistics.find("total_voting_places").text,
        "total_voting_places_counted": electorate_statistics.find("total_voting_places_counted").text,
        "percent_voting_places_counted": electorate_statistics.find("percent_voting_places_counted").text,
        "total_votes_cast": electorate_statistics.find("total_votes_cast").text,
        "percent_votes_cast": electorate_statistics.find("percent_votes_cast").text,
        "total_party_informals": electorate_statistics.find("total_party_informals").text,
        "total_candidate_informals": electorate_statistics.find("total_candidate_informals").text,
        "total_registered_parties": electorate_statistics.find("total_registered_parties").text,
        "total_candidates": electorate_statistics.find("total_candidates").text
    }

    electorate_statistics_df = pd.concat([electorate_statistics_df, pd.DataFrame([row])], ignore_index=True)

    electorate_statistics_df.to_csv(constant.OUTPUT_DIR + "/electorate_statistics/" + electorate_number + "_statistics.csv",
                                    index=False)


def parse_electorate_candidate_votes(electorate_candidate_votes, electorate_number):
    electorate_candidate_votes_df = pd.DataFrame(columns=["candidate_number",
                                                          "candidate_votes"])

    for index, item in enumerate(electorate_candidate_votes):
        candidate_number = item["c_no"]
        votes = item.find("votes").text

        row = {
            "candidate_number": candidate_number,
            "candidate_votes": votes
        }

        electorate_candidate_votes_df = pd.concat([electorate_candidate_votes_df, pd.DataFrame([row])],
                                                  ignore_index=True)

        electorate_candidate_votes_df.to_csv(
            constant.OUTPUT_DIR + "/electorate_candidate_votes/" + electorate_number + "_candidate_votes.csv", index=False)


def parse_electorate_party_votes(electorate_party_votes, electorate_number):
    electorate_party_votes_df = pd.DataFrame(columns=["party_number",
                                                      "party_votes"])

    for index, item in enumerate(electorate_party_votes):
        party_number = item["p_no"]
        votes = item.find("votes").text

        row = {
            "party_number": party_number,
            "party_votes": votes
        }

        electorate_party_votes_df = pd.concat([electorate_party_votes_df, pd.DataFrame([row])], ignore_index=True)

        electorate_party_votes_df.to_csv(
            constant.OUTPUT_DIR + "/electorate_party_votes/" + electorate_number + "_party_votes.csv", index=False)


def parse_specific_electorate(electorate, electorate_number):
    electorate_soup = BeautifulSoup(electorate, "xml")

    electorate_statistics_xml = electorate_soup.find("statistics")
    parse_electorate_statistics(electorate_statistics_xml, electorate_number)

    electorate_party_votes_xml = electorate_soup.find_all("party")
    parse_electorate_party_votes(electorate_party_votes_xml, electorate_number)

    electorate_candidate_votes_xml = electorate_soup.find_all("candidate")
    parse_electorate_candidate_votes(electorate_candidate_votes_xml, electorate_number)


def parse_electorates(electorates):
    soup = BeautifulSoup(electorates, "xml")

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

        if int(electorate_number) < 10:
            electorate_number_to_search = "e0" + electorate_number
        else:
            electorate_number_to_search = "e" + electorate_number

        specific_electorate_url = constant.ELECTION_DATA_XML_BASE + electorate_number_to_search + "/" + electorate_number_to_search + ".xml"
        specific_electorate_xml = requests.get(specific_electorate_url)

        parse_specific_electorate(specific_electorate_xml.content, electorate_number_to_search)

    return df


if not os.path.exists(constant.OUTPUT_DIR):
    os.mkdir(constant.OUTPUT_DIR)

if not os.path.exists(constant.ELECTORATE_STATISTICS_PATH):
    os.mkdir(constant.ELECTORATE_STATISTICS_PATH)

if not os.path.exists(constant.ELECTORATE_PARTY_VOTES_PATH):
    os.mkdir(constant.ELECTORATE_PARTY_VOTES_PATH)

if not os.path.exists(constant.ELECTORATE_CANDIDATE_VOTES_PATH):
    os.mkdir(constant.ELECTORATE_CANDIDATE_VOTES_PATH)

electorates_xml = requests.get(constant.ELECTORATES_URL)
candidates_xml = requests.get(constant.CANDIDATES_URL)
parties_xml = requests.get(constant.PARTIES_URL)
electorate_regions_json = requests.get(constant.ELECTORATE_REGIONS_URL)

electorates_df = parse_electorates(electorates_xml.content)
electorates_df.to_csv("%s/electorates.csv" % constant.OUTPUT_DIR, index=False)

# candidates_df = parse_candidates_xml(candidates_xml.content)
# candidates_df.to_csv("candidates.csv", index=False)
#
# parties_df = parse_parties_xml(parties_xml.content)
# parties_df.to_csv("parties.csv", index=False)
