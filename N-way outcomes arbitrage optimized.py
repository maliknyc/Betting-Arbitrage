'''
N-way outcomes arbitrage
'''
import csv 

file = "odds_pga.csv"
# file = "test_odds.csv"

# read csv file where column A has arbitrary names/labels, and column B respective list of American odds
def file_reader(filename, idx):
    with open(filename, "r", encoding = 'utf-8-sig') as infile:
        reader = csv.reader(infile)
        return [i[idx] for i in reader]
    
names = file_reader(file, 0)
odds = [int(x) for x in file_reader(file, 1)]

# [NOT USED] recalculate American odds w/o betting vig
def odds_calc_partial_vigless(odds):
    if odds < 0:
        vigless_prob = -odds / (-odds + 100)
    else:
        vigless_prob = 100 / (odds + 100)
    return vigless_prob

# [NOT USED] confirm vig odds add up to implied prob of 100%
def prob_no_vig(name, name_list, odds_list):
    prob_list = [odds_calc_partial_vigless(odd) for odd in odds_list]
    sum_prob_list = sum(prob_list)
    spec_prob = odds_calc_partial_vigless(odds_list[name_list.index(name)])
    vigless_total_prob = round((spec_prob / sum_prob_list) * 100, 2)
    
    return vigless_total_prob

# convert American odds to decimal odds
def american_to_decimal(odds):
    if odds > 0:
        odds_dec = 1 + odds/100
    else:
        odds_dec = 1 - 100/odds
    # print(odds_dec)
    return odds_dec

# list of decimal odds from list of American odds
def dec_odds_list(odds_list1):
    dec_odds = []
    for i in odds_list1:
        dec_odds.append(american_to_decimal(i))
    return dec_odds

# calculate total implied probability of decimal odds list
def sum_dec_finder(dec_odds1):
    sum_dec = 0
    for i in dec_odds1:
        sum_dec += 1/i
    return sum_dec

# calculate profit on individual bets/outcomes based on results
def prof_indiv_bets(odds_list, bets_list, result):
    prof = 0
    for i in range(len(odds_list)):
        if odds_list[i] < 0 and result == i:
            prof += 100/-odds_list[i] * bets_list[i]
        elif odds_list[i] > 0 and result == i:
            prof += odds_list[i]/100 * bets_list[i]
        elif result != i:
            prof += -bets_list[i]
    return prof

# returns a list of the % each number in a list makes up of the sum of the list
def proportion(list1):
    sum_list = sum(list1)
    proportion_list = [i/sum_list for i in list1]

    return proportion_list

def arb_identifier_new(odds_list1):
    
    '''
        1. Identifies arbitrage opportunities based on implied probability:
            if implied probability >= 100%, there'll be no arbitrage opportunity
            if implied probability < 100%, there'll be an arbitrage opportunity equal to how much it falls under 100%
        2. Calculates list of bet amounts (stake_list) based on a total payout of 100
        3. Calculates proportion of each bet in stake_list
        4. Recalculates stake_list based on user's desired total investment amount, and tells user what to bet
        5. Calculates optimal profit amount (if you were to place the exact optimal bets)
        6. Calculates optimal ROI (constant regardless of desired investment)
    '''
    
    dec_odds = dec_odds_list(odds_list1)
    sum_dec = sum_dec_finder(dec_odds)
    stake_list = []
    arb_or_not = False
    print("The total implied probability is:", sum_dec)
    print()
    if sum_dec >= 1:
        print("There is no arbitrage opportunity.")
    elif sum_dec < 1:
        print("There is an arbitrage opportunity!")
        arb_or_not = True
        # desired_payout = float(input("What is your desired total payout? "))
        desired_payout = 100
        for i in range(len(dec_odds)):
            stake = desired_payout/dec_odds[i]
            # print(stake)
            stake_list.append(stake)
        
        desired_investment = float(input("What is your desired total investment? "))
        print()
        
        proportions = proportion(stake_list)
        desired_bets = []
        for i in proportions:
            desired_bets.append(i*desired_investment)    
            
        print("The optimal bets are:", desired_bets)
        print()
        print("The optimal bet ratio is:", proportions)
        print()
        
        optimal_prof_amt = prof_indiv_bets(odds_list1, desired_bets, 0)
        print("The optimal arbitrage profit is:", optimal_prof_amt)
        print()
        
        return_on_bet = (optimal_prof_amt/sum(desired_bets)) * 100
        print("This is a", return_on_bet, "% optimal return")
        
    return sum_dec, stake_list, arb_or_not


def arb_results_test(odds):
    
    '''
        1. Asks user to test out bets
            - In practice, user should test rounding up or down to nearest whole dollar
        2. Shows profit amount and % for each outcome
        3. Identifies whether user is making a risk-free bet
            - if all outcomes lead to a non-negative profit, the bet is risk-free
            - otherwise it's a risky bet
                - User may want to test a different rounding procedure if they want a risk-free bet
    '''
    
    bet_counter = 1
    risky_counter = 0
    list_of_bets = []
    list_of_profits = []
    
    print()
    print("Let's test it out!")
    for i in range(len(odds)):
        bet = float(input("Place bet " + str(bet_counter) + ": "))
        bet_counter += 1
        list_of_bets.append(bet)
        
    print()
        
    for i in range(len(names)):
        print("If outcome", i + 1, "wins, you make", prof_indiv_bets(odds, list_of_bets, i))
        print("This is a", (prof_indiv_bets(odds, list_of_bets, i))/sum(list_of_bets) * 100, "% return")
        print()
        list_of_profits.append(prof_indiv_bets(odds, list_of_bets, i))
        
    print()
    
    for i in list_of_profits:
        if i < 0:
            risky_counter += 1
    if risky_counter > 0:
        print("This is a risky bet!")
    else:
        print("This is a risk-free bet!")
    
    return list_of_profits

# call arb_identifier_new to identify whether there's an arbitrage opportunity, and runs 
# arb_results_test to test bets in the case that there is
if __name__ == "__main__":
    
   # odds_list = [-333, 300, 900, 1200, 1400]
    
   sum_dec, stake_list, arb_or_not = arb_identifier_new(odds)
   
   if arb_or_not:
       list_of_profits = arb_results_test(odds)
       








