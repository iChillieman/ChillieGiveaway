Hello Tweepz! 

This is a script i wrote to track the transfers of a Token to watch who is buying or Selling The Token & And how much they are spending when they buy.

# Intension
- The intention of this script is to Select a Winner of a Giveaway depending on Token Transfer Activity.
- Still Figuring out which Criteria should be most elligable to receieve Giveaways.
- This Script will obviously hook into my Official ChilliePicker project that picks Giveaway Winners on Twitter.

# Important Note:
- The Script is purposely not Finished, as i only want compotent developers that can finish it properly using it.
- Willing to provide a Finished Script for the price of 5 ETH to anyone who doesnt have the required Dev Skills.

# Usage:
1. Enter an Alchemy Project ID and EtherScan API Key into the .env File
2. Open the config.py file and adjust to your liking.
3. A: Implement the db_pick_a_presale_winner_who_never_sold function if you want to choose winners who got Presale, but never sold after you announced the Giveaway.
3. B: Implement the db_pick_a_winner_who_spent_the_most function if you want to choose winners who bought the MOST since you announced the giveaway.
4. Run the chillie_sniffer Script to start collecting data on Token Transfers
5. Run the chillie_picker Script to select Winners
 
# PreReqs:
- Install Python
- Use PIP to install required libraries (You should know how to figure out which ones are needed)
- Must be a Competent Developer.
 
# Inadequecies:
When someone buys a token using a Proxy (Such as an aggregator) the Transaction Value is 0, causing it to not properly be entered in the Giveaway that picks whoever bought the most. Will need to take some time to bring this up to par before Launching Official ChillieGiveaways.
