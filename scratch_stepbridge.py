
import os
import pandas as pd
from pprint import pprint

from contract import ContractFactory, DOUBLED
from scrape_double_dummy import dds_tricks_to_tricks_per_suit_per_wind
from scrape_stepbridge import get_direction_for_player

SCRAPED_DIRECTORY = 'scraped'

# stepbridge_overview_url = 'https://portal.stepbridge.nl/tournament/events/index/users/74285'
# df_all_tournament_overview = get_stepbridge_tournament_overview_dataframe(stepbridge_overview_url)
# stepbridge_personal_tournament_url = df_all_tournament_overview[TOURNAMENT_URL_KEY][0]

# a_stepbridge_personal_tournament_url = 'https://results.stepbridge.nl/tournament/events/show/38602/JoostL'
# my_name = os.path.basename(a_stepbridge_personal_tournament_url)
# a_tournament_id = os.path.basename(os.path.split(a_stepbridge_personal_tournament_url)[0])
# print(f'[INFO] scraping boards data for {my_name} in tournament {a_tournament_id}.' +
#       f' url={a_stepbridge_personal_tournament_url}')
# df_tournament = scrape_tournament_dataframe(a_stepbridge_personal_tournament_url, my_name)
# tournament_file_name = determine_scraped_filename_stepbridge(tournament_id=a_tournament_id, player_name=my_name)
# tournament_file_path = os.path.join(SCRAPED_DIRECTORY, tournament_file_name)
# df_tournament.to_pickle(tournament_file_path)

tournament_file_name = r'scraped-stepbridge-tournament_38602_JoostL.pkl'
df_tournament = pd.read_pickle(os.path.join(SCRAPED_DIRECTORY, tournament_file_name))

print()
select_columns = ['contract', 'declarer', 'result', 'contractsNS', 'contractsEW', 'ddtricks']
# select_columns = ['lead', 'best_leads']
# print(df_tournament[select_columns])

row = df_tournament.iloc[1]
print(row['double_dummy_url'])
# print(row)

optimal_contracts = ContractFactory.convert_contract_string(row['contractsNS'].split(':')[1])
played_contract = ContractFactory.convert_contract_string(row['declarer'] + ' ' + row['contract'])[0]

my_name = 'JoostL'
our_direction = get_direction_for_player(row['players'], my_name)
print('our_direction:', our_direction)
pprint(optimal_contracts)
print('played:', played_contract)

did_we_play = row['declarer'] in our_direction
should_we_have_played = optimal_contracts[0].declarer in our_direction

optimal_contracts_in_played_suit = [contract for contract in optimal_contracts
                                    if contract.suit == played_contract.suit]
if did_we_play != should_we_have_played:
    did_declarer_play_in_the_right_suit = None
else:
    did_declarer_play_in_the_right_suit = (optimal_contracts_in_played_suit != [])
print('should_we_have_played:', should_we_have_played)
should_we_have_saved = should_we_have_played and (optimal_contracts[0].doubled_status == DOUBLED)
print('should_we_have_saved:', should_we_have_saved)
should_they_have_saved = (not should_we_have_played) and (optimal_contracts[0].doubled_status == DOUBLED)
print('should_they_have_saved:', should_we_have_saved)

print('did_we_play:', did_we_play)
print('did_declarer_play_in_the_right_suit:', did_declarer_play_in_the_right_suit)
played_in_optimal_contract = (played_contract in optimal_contracts)
print('played_in_optimal_contract:', played_in_optimal_contract)

played_in_equivalent_of_optimal_contract = False
for optimal_contract in optimal_contracts:
    if optimal_contract.is_equivalent(played_contract):
        played_in_equivalent_of_optimal_contract = True
        break


print('played_in_equivalent_of_optimal_contract:', played_in_equivalent_of_optimal_contract)
if not played_in_equivalent_of_optimal_contract:
    if not did_declarer_play_in_the_right_suit:
        print('played in wrong suit')
    else:
        min_optimal_contract = min(optimal_contracts)
        max_optimal_contract = max(optimal_contracts)
        if played_contract < min_optimal_contract:
            print('bid too low')
        elif played_contract > max_optimal_contract:
            print('bid too high')
        else:
            print('unsure why contract bid was not optimal')

dds_tricks_per_suit_per_wind = dds_tricks_to_tricks_per_suit_per_wind(row['ddtricks'])
optimal_tricks_in_suit_played = dds_tricks_per_suit_per_wind[row['declarer']][played_contract.suit]
print('optimal_tricks_in_suit_played:', optimal_tricks_in_suit_played)

tricks_made_in_suit_played = played_contract.level + 6 + row['result']
print('tricks_made_in_suit_played:', tricks_made_in_suit_played)

if tricks_made_in_suit_played == optimal_tricks_in_suit_played:
    print('declarer made optimal number of tricks')
elif tricks_made_in_suit_played < optimal_tricks_in_suit_played:
    print('declarer made too few tricks')
else:
    print('declarer made more tricks than optimal')

# print(df_tournament['contractsNS'])
# TODO: extract bidding
# TODO: extract all double dummy contracts
