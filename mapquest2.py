import urllib.parse
import requests
import sys
import configparser
from tabulate import tabulate
from datetime import datetime

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "8pZqf042uMGvHGAFMxCssCSCx7z6Znyv"
config = configparser.ConfigParser()
config.read('config.ini') #Read config file
unit = config["units"]["distance"]

def main():   
   while True:
      welcomeChoice = welcomeScreen()  #Option to go to the Main Program or the Settings
      
      if welcomeChoice == 1:
         while True:
            orig, dest, routeType, drivingStlye = getParameters()                      #Get the parameters needed to make a request
            json_data, json_status = urlEncode(orig, dest, routeType, drivingStlye)    #Encode the parameters and perform a request,
                                                                                       #and receive a response.
            
            if statusIsValid(json_status): #Request validation         
               break
         
         choice = displayOptions()                       #Ask how the data will be displayed
         displayData(orig, dest, json_data, choice)      #Displays the data
      
         while True:                                                    #Repeat the program if desired
            tryAgain = input("Try Map Quest Again? [y/n] ").lower()
            if tryAgain == 'y' or tryAgain == 'n':
               print()
               break
            else:
               print("Invalid input. Try again.")
         
         if tryAgain == 'n':
            break
         elif tryAgain == 'y':
            continue
         
      elif welcomeChoice == 2:
         settings()                                         #Go to the settings
      
def welcomeScreen():
   welcomeScreen = [["Welcome to Mapquest"]]
   while True:
      welcomeScreen.append(["[1] Go to main program"])
      welcomeScreen.append(["[2] Go to Settings"])
      
      print(tabulate(welcomeScreen,tablefmt="pretty"))
      
      welcomeChoice = int(input("input: "))
      
      if welcomeChoice not in range(1,3): #If welcomeChoice is NOT 1 or 2
         print("Invalid input. Try Again.")
      else:
         return welcomeChoice


#Get url parameters
def getParameters():
   routeTypeChoices = ["fastest","shortest","pedestrian","bicycle"]  #Route Type valid choices
   drivingStlyeChoices = ["cautious", "normal", "aggressive"]        #Driving Style valid choices
   
   orig = input("\nStarting Location: ")        #Starting location Parameter
   dest = input("Destination: ")                #Destination Parameter
   
   routeType = input("Route Type (fastest is default) [fastest/shortest/pedestrian/bicycle]: ") #Route Type Parameter
      
   #Route Type validation
   while True:
      if routeType in routeTypeChoices:
         break
      else:
         routeType = input("\nInvalid input. Please choose one of the options: [fastest/shortest/pedestrian/bicycle]: ")

   drivingStyle = input("Driving Style (normal is the default) [cautious, normal, aggressive] ")
   
   #Driving Style validation
   while True:
      if drivingStyle in drivingStlyeChoices:
         break
      else:
         drivingStyle = input("\nInvalid input. Please choose one of the options: [cautious, normal, aggressive]: ")
      
   return orig, dest, routeType, drivingStyle

#Encode URL
def urlEncode(orig, dest, routeType, drivingStyle):   
   url = main_api + urllib.parse.urlencode({ #combine main_api and parameters to create the url 
         "key": key,
         "from":orig,
         "to":dest,
         "routeType": routeType,
         "drivingStyle":drivingStyle,
         "unit": unit
         })
   
   print("URL: " + (url))
   json_data = requests.get(url).json()
   json_status = json_data["info"]["statuscode"]
   
   return json_data, json_status
   
def statusIsValid(json_status):
   if json_status == 0:
      print()
      print("API Status: " + str(json_status) + " = A successful route call.\n")
      return True
   elif json_status == 402:
      print("\n**********************************************")
      print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
      print("**********************************************")
      
      return False
   elif json_status == 611:
      print("\n**********************************************")
      print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
      print("**********************************************")
      
      return False
   else:
      print("\n************************************************************************")
      print("For Staus Code: " + str(json_status) + "; Refer to:")
      print("https://developer.mapquest.com/documentation/directions-api/status-codes")
      print("************************************************************************")
      
      return False

def displayOptions():
   while True:                                  #Display Options
      trip=[["__MENU__"],["[1] Trip Duration"],["[2] Distance"],["[3] Directions"],
         ["[4] Display all information"],["[5] Quit"]]

      print(tabulate(trip,tablefmt="pretty"))
      
      while True:
         try:
            choice = int(input("Choose one input only: "))
         except ValueError:
            print("Use integer values only.")
         else:
            break
      
      if choice not in range(1, 6):
         print("Invalid Input. Try again.")
      else:
         return choice

def displayData(orig, dest, json_data, choice):
   config = configparser.ConfigParser()
   config.read('config.ini') #Read config file
   
   #Covnert Time to DD:HH:MM:SS
   raw_duration = json_data["route"]["formattedTime"]
   nums = raw_duration.split(':')
   days = 0
   hrs = int(nums[0])
   mins = int(nums[1])
   secs = int(nums[2])
   
   if hrs > 24:
      days = int(hrs/24)
      hrs = hrs - (days*24)
   
   converted_time = str('{} day/s, {}:{}:{}'.format(days, hrs, mins, secs))
   
   if choice == 1:         #Trip Duration Only
      print("Trip Duration: " + (converted_time))
   elif choice == 2:       #Distance Only
       print("Distance Travelled: {} {}".format(str((json_data["route"]["distance"])), config["units"]["distance"]))
   elif choice == 3:       #Directions Only
      print()
      navs=[["Directions"]]
      for each in json_data["route"]["legs"][0]["maneuvers"]:
         navs.append([(each["narrative"]) + str(": {:.2f} {}".format(each["distance"], config["units"]["distance"]))])
      print(tabulate(navs,tablefmt="pretty"))
      
   elif choice == 4:       #Display All
      table=[["Directions from " + (orig) + " to " + (dest)],
      ["Trip Duration: " + (converted_time)],
      ["Distance Travelled: " + str("{:.2f} {}".format(json_data["route"]["distance"], config["units"]["distance"]))]]
      
      print(tabulate(table,tablefmt="pretty"))
      print()
      
      navs=[["Directions"]]
      for each in json_data["route"]["legs"][0]["maneuvers"]:
         navs.append([(each["narrative"]) + str(": {:.2f} {}".format(each["distance"], config["units"]["distance"]))])
      print(tabulate(navs,tablefmt="pretty"))
   elif choice == 5:
      sys.exit()

def settings():
   while True:
      print()
      settings=[["__SETTINGS__"],
      ["[1] Change units for distance"],
      ["[2] return to Welcome Screen"]]
      
      print(tabulate(settings,tablefmt="pretty"))
      
      #settings validation
      while True:
         settingsChoice = int(input("Input: "))
         if settingsChoice not in range(1,3):
            print("Invalid input. Try again.")
         else:
            break
      
      if settingsChoice == 1:
         print("\nChange unit for Distance to:")
         print("[1] Miles (m)")
         print("[2] Kilometers (k)")
         print("Current unit for Distance: " + config["units"]["Distance"])
         
         #distance validation
         while True:
            distanceUnit = int(input(""))
            
            if distanceUnit not in range(1,3):
               print("Invalid Input. Try again")
            else:
               break
               
         if distanceUnit == 1:
            config.set('units','Distance','m')
         elif distanceUnit == 2:
            config.set('units','Distance','k')
         
         with open('config.ini', 'w') as configfile: #Write new settings to config file
            config.write(configfile)
         
         print("Settings updated.\n")
      elif settingsChoice == 2:
         print()
         break 
   
if __name__ == '__main__':
   main()