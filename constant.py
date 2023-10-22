STUFF_HOST = "https://interactives.stuff.co.nz"

ELECTION_DATA_PATH = "/election-data/2023/xml/"

ELECTION_DATA_XML_BASE = (STUFF_HOST, ELECTION_DATA_PATH)

ELECTORATES_URL = "%s%selectorates.xml" % ELECTION_DATA_XML_BASE

PARTIES_URL = "%s%sparties.xml" % ELECTION_DATA_XML_BASE

CANDIDATES_URL = "%s%scandidates.xml" % ELECTION_DATA_XML_BASE

ELECTORATE_REGIONS_URL = "%s/staging/2023-elec-staging/data/electorate-regions.json" % STUFF_HOST

OUTPUT_DIR = "output"

ELECTORATE_CANDIDATE_VOTES_PATH = "%s/electorate_candidate_votes" % OUTPUT_DIR

ELECTORATE_PARTY_VOTES_PATH = "%s/electorate_party_votes" % OUTPUT_DIR

ELECTORATE_STATISTICS_PATH = "%s/electorate_statistics" % OUTPUT_DIR
