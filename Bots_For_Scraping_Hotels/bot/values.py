# This file takes all the inputs from the user

class Values():
    def __init__(self):
        self.base_url = "https://www.trivago.com/"
        print("Welcome to the web scraping project! Initializing............\n")
        self.country = input("Enter your country! First letter in caps....\n")
        self.lan = input("Enter your preferred language! First letter in caps.....\n")
        self.cur = input("Enter your preferred currency! Please put acronyms in block letters (Ex: USD for the American Dollar, INR for the Indian Rupee etc).....\n")
        self.destination = input("Enter your destination! First letter in caps.....\n")
        print("Your check in date is __ months away.\n") 
        self.check_in = int(input("(Ex: Enter 2 if it is July, 2024 and you are checking in September, 2024 ; enter 0 if you are checking in this month.)\n"))
        self.cid = input("Enter your check in date in 'YYYY-MM-DD' format.\n")
        print("Your check out date is __ months away.\n")
        self.check_out = int(input("(Ex: Enter 2 if it is July, 2024 and you are checking out in September, 2024 ; enter 0 if you are checking out this month.)\n"))
        self.check_out -= (self.check_in+1)
        self.cod = input("Enter your check out date in 'YYYY-MM-DD' format.\n")
        print("Please remember that one room can accommodate 8 people max.\n")
        print("And the number of rooms you are booking must not exceed the number of adults.\n")
        self.adult_num = int(input("Enter the number of adults.\n"))
        self.child_num = int(input("Enter the number of children.\n"))
        self.room_num = int(input("Enter the number of rooms you are looking to book.\n"))
        self.reqd_room_num = self.room_num-1-((self.adult_num+self.child_num)//8)
        self.children_age_list = []
        print("We need to know the ages of the children\n")
        for _ in range(1, self.child_num+1):
            temp = input("Enter age!\n")
            self.children_age_list.append(temp)
        self.children = len(self.children_age_list)
        self.pet = input("Do you want pet-friendly rooms? (y/n)\n")
        self.is_pet_friendly = False
        if (self.pet == "y"):
            self.is_pet_friendly = True
        print("Fetching deals for you........\n")
