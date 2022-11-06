import urllib.parse
import requests
import sys
import configparser

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "8pZqf042uMGvHGAFMxCssCSCx7z6Znyv"

def main():
   while True:
      welcomeChoice = welcomeScreen()
      
      if welcomeChoice == 1:
         while True:
            orig, dest, unit, routeType, drivingStlye = getParameters()
            json_data, json_status = urlEncode(orig, dest, unit, routeType, drivingStlye)
            
            if statusIsValid(json_status): #If True
               break
         
         choice = mainProgram()
         displayData(orig, dest, json_data, choice)
      
         while True:
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
         settings()
      
def welcomeScreen():
   print("Welcome to MapQest")
   while True:
      print("\n[1] Go to main program")
      print("[2] Go to Setttings")
      
      welcomeChoice = int(input("input: "))
      
      if welcomeChoice not in range(1,3): #If welcomeChoice is NOT 1 or 2
         print("Invalid input. Try Again.")
      else:
         return welcomeChoice


#Get url parameters
def getParameters():
   config = configparser.ConfigParser()
   config.read('config.ini') #Read config file
   
   unit = config["units"]["distance"]
   
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
      
   return orig, dest, unit, routeType, drivingStyle

#Encode URL    
def urlEncode(orig, dest, unit, routeType, drivingStyle):
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

def mainProgram():
   while True:                                  #Display Options
      print("\n_________Display Options_________")
      print("[1] Trip Duration ")
      print("[2] Distance ")
      print("[3] Fuel used ")
      print("[4] Directions")
      print("[5] Display all information")
      print("[6] Quit")
      
      choice = int(input("Choose one input only: "))
      
      if choice not in range(1, 7):
         print("Invalid Input. Try again.")
      else:
         return choice

def displayData(orig, dest, json_data, choice):
   config = configparser.ConfigParser()
   config.read('config.ini') #Read config file
   
   if config['units']['fuel'] == 'liters':
      fuel = json_data["route"]["fuelUsed"]*3.78
   else:
      fuel = json_data["route"]["fuelUsed"]
   
   if choice == 1:         #Trip Duration Only
      print("Trip Duration: " + (json_data["route"]["formattedTime"]))
   elif choice == 2:       #Distance Only
       print("Distance Travelled: {} {}".format(str((json_data["route"]["distance"])), config["units"]["distance"]))
   elif choice == 3:       #Fuel Only
      print("Fuel Used: " + str("{:.2f} {}".format(fuel, config['units']['fuel'])))
   elif choice == 4:       #Directions Only
      for each in json_data["route"]["legs"][0]["maneuvers"]:
         print((each["narrative"]) + " (" + str("{:.2f} {})".format(each["distance"], config["units"]["distance"])))
         print("=============================================\n")
   elif choice == 5:       #Display All
      print("Directions from " + (orig) + " to " + (dest))
      print("Trip Duration: " + (json_data["route"]["formattedTime"]))
      print("Distance Travelled: " + str("{:.2f} {}".format(json_data["route"]["distance"], config["units"]["distance"])))
      print("Fuel Used ({}): {:.2f}".format(config['units']['fuel'], fuel))
      print("=============================================")
      print()
      
      for each in json_data["route"]["legs"][0]["maneuvers"]:
         print((each["narrative"]) + " (" + str("{:.2f} {})".format(each["distance"], config["units"]["distance"])))
         print("=============================================\n")
   elif choice == 6:
      sys.exit()

def settings():
   config = configparser.ConfigParser()
   config.read('config.ini') #Read config file
   
   while True:
      print("\n_________SETTINGS_________")
      print("[1] Change units for distance")
      print("[2] Change units for fuel")
      print("[3] return to Welcome Screen")
      
      while True:
         settingsChoice = int(input("Input: "))
         if settingsChoice not in range(1,4):
            print("Invalid input. Try again.")
         else:
            break
      
      if settingsChoice == 1:
         print("\nChange unit for Distance to:")
         print("[1] Miles (m)")
         print("[2] Kilometers (k)")
         print("Current unit for Distance: " + config["units"]["Distance"])
         
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
         print("\nChange unit for fuel to:")
         print("[1] Gallons")
         print("[2] Liters")
         print("Current unit for Fuel: " + config["units"]["Fuel"])
         
         while True:
            fuelUnit = int(input(""))
            
            if fuelUnit not in range(1,3):
               print("Invalid Input. Try again")
            else:
               break
               
         if fuelUnit == 1:
            config.set('units','Fuel','gallons')
         elif fuelUnit == 2:
            config.set('units','Fuel','liters')
         
         with open('config.ini', 'w') as configfile: #Write new settings to config file
            config.write(configfile)
      
         print("Settings updated.\n")
      elif settingsChoice == 3:
         print()
         break

main()  