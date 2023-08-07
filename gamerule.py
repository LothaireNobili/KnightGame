

class Gamerules():

    def __init__(self):
        #define game rules and variable
        self.current_fighter = 1
        self.bandit_count = 1
        self.total_fighter = self.bandit_count + 1 #amount of bandit + the player
        self.action_wait_time = 40
        self.heal_potion_effect = 15
