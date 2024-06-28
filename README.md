# N-way Outcomes Arbitrage

## Overview
This Python script helps users identify arbitrage opportunities across multiple betting options and calculate the optimal bet allocations to maximize profit. The script reads American odds from a CSV file and performs various calculations to determine if arbitrage opportunities exist and how to exploit them.

## Prerequisites
Before running the script, ensure you have the following library installed:
- csv (standard library, no installation needed)

## Usage

### Prepare Your Data:
Ensure your betting data is in a CSV file with the following columns:
- Column A: Arbitrary names/labels
- Column B: Respective list of American odds

### Run the Script:
Execute the script and follow the prompts:
python N-way outcomes arbitrage optimized.py


### Input Details:
1. **File Selection:** Update the script with the correct CSV filename containing the odds data.
2. **Desired Total Investment:** Enter the total amount you want to invest.
3. **Individual Bets:** Place individual bets to test the results.

### Output:
The script will display:
- Total implied probability
- Indication of whether there is an arbitrage opportunity
- Optimal bets and bet ratios
- Optimal arbitrage profit
- Optimal return percentage
- Profit amounts and returns for each outcome
- Indication of whether the bet is risk-free or risky
