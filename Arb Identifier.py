'''
Arbitrage Opportunity Identifier (2-way outcomes)
'''

import matplotlib.pyplot as plt
import random
import csv 
import collections
import datetime
import json

CARD = "ufc 282.csv"


def file_reader(filename, idx):
    
    # initialize list to store file contents
    list1 = []

    # open and read file
    with open(filename, "r") as infile:
        reader = csv.reader(infile)
        # use for loop to add contents into list
        for i in reader:
            list1.append(i[idx])
                
    return list1


def odds_calc(odds1, odds2):
    
    if odds1 < 0:
        prob1 = -odds1 / (-odds1 + 100)
    else:
        prob1 = 100 / (odds1 + 100)
        
    if odds2 < 0:
        prob2 = -odds2 / (-odds2 + 100)
    else:
        prob2 = 100 / (odds2 + 100)
        
    final_prob1 = round((prob1 / (prob1 + prob2)) * 100, 2)
    final_prob2 = round((prob2 / (prob1 + prob2)) * 100, 2)
    
    return final_prob1

def payout_calc(stake, odds1, result):
    if odds1 < 0 and result == 1:
        profit = 100/-odds1 * stake
    elif odds1 > 0 and result == 1:
        profit = odds1/100 * stake
    elif result == 0:
        profit = -stake

    payout = profit + stake
    
    return profit

def arb_profit(stake1, stake2, odds1, odds2, result1):
    if result1 == 1:
        result2 = 0
    else:
        result2 = 1
    profit1 = payout_calc(stake1, odds1, result1)
    profit2 = payout_calc(stake2, odds2, result2)
    arb_profit = profit1 + profit2
    
    return arb_profit

def is_it_risk_free(arb_prof_1, arb_prof_2):
    is_it = None
    if arb_prof_1 >= 0 and arb_prof_2 >= 0:
        is_it = 1
    else:
        is_it = 0
    if is_it == 1:
        print("This is a risk-free bet!")
    else:
        print("This is a risky bet!")
        
def american_to_decimal(odds):
    if odds > 0:
        odds_dec = 1 + odds/100
    else:
        odds_dec = 1 - 100/odds
    # print(odds_dec)
    return odds_dec

def arb_identifier(odds_dec1, odds_dec2):
    stake_a = 0
    stake_b = 0
    dec1 = american_to_decimal(odds_dec1)
    dec2 = american_to_decimal(odds_dec2)
    sum_dec = 1/dec1 + 1/dec2
    print("The total implied probability is:", sum_dec)
    if sum_dec >= 1:
        print("There is no arbitrage opportunity.")
    elif sum_dec < 1:
        print("There is an arbitrage opportunity!")
        # desired_payout = float(input("How much payout do you want? "))
        desired_payout = 100
        stake_a = desired_payout/dec1
        stake_b = desired_payout/dec2
        # print("You have to bet", stake_a, "on fighter 1, and", stake_b, "on fighter 2 for arbitrage.")
        print()
        print("If you bet at a", stake_a/stake_b, "ratio, you can make arbitrage.")
    
    return sum_dec, stake_a, stake_b


if __name__ == "__main__":
    
    # fighter1, fighter2 = odds_calc(180, -220)
    stake1 = float(input("How much do you want to bet on fighter 1?: "))
    stake2 = float(input("How about on fighter 2?: "))
    # input1 = int(input("What are the odds of the fighter? "))
    
    odds1 = int(input("What are the odds of fighter 1?: "))
    odds2 = int(input("What about fighter 2?: "))
    # result1 = int(input("Did fighter 1 win? 1 means yes and 0 means no: "))
    
    # desired_payout = float(input("How much payout do you want to make if there is an arbitrage opportunity? "))
    
    fighter1 = odds_calc(odds1, odds2)
    fighter2 = round(100 - fighter1, 2)
    print()
    print("Implied prob 1 (no vig):", fighter1)
    print("Implied prob 2 (no vig):", fighter2)
    print(fighter1 + fighter2)
    print()
    
    # profit = payout_calc(stake_input, input1, 0)
    arb_prof_fighter1_win = arb_profit(stake1, stake2, odds1, odds2, 1)
    arb_prof_fighter2_win = arb_profit(stake1, stake2, odds1, odds2, 0)
    
    print("Your profit would be", arb_prof_fighter1_win, "if fighter 1 wins.")
    print("It would be", arb_prof_fighter2_win, "if fighter 2 wins.")
    print()
    
    is_it_risk_free(arb_prof_fighter1_win, arb_prof_fighter2_win)
    print()
    
    arb_identifier(odds1, odds2)
    
    
    # print("Your profit would be: ", profit)



















