import urllib.parse
import requests
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "8pZqf042uMGvHGAFMxCssCSCx7z6Znyv"
routeTypeChoices = ["fastest","shortest","pedestrian","bicycle"]  #Route Type valid choices
drivingStlyeChoices = ["cautious", "normal", "aggressive"]

print("Welcome to MapQest")                     #Start of program
print("[1] Go to main program")
print("[2] Go to Setttings")

welcomeChoice = int(input("input: "))

if welcomeChoice == 1:
   orig = input("\nStarting Location: ")        #Starting location Parameter
   dest = input("Destination: ")                #Destination Parameter
   routeType = input("Route Type (fastest is default) [fastest/shortest/pedestrian/bicycle]: ") #Route Type Parameter
   
   while True:
      if routeType in routeTypeChoices:
         break
      else:
         routeType = input("\nInvalid input. Please choose one of the options: [fastest/shortest/pedestrian/bicycle]: ")

   drivingStyle = input("Driving Style (normal is the default) [cautious, normal, aggressive]")
   
   while True:
      if drivingStyle in drivingStlyeChoices:
         break
      else:
         drivingStyle = input("\nInvalid input. Please choose one of the options: [cautious, normal, aggressive]: ")
         
   url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType": routeType, "drivingStyle":drivingStyle})
   print("URL: " + (url))
   json_data = requests.get(url).json()
   json_status = json_data["info"]["statuscode"]

   while True:                                  #Menu
      print("\n_________MENU_________")
      print("[1] Trip Duration ")
      print("[2] Distance ")
      print("[3] Fuel used ")
      print("[4] Directions")
      print("[5] Display all information")
      print("[6] Try different location")
      print("[7] Quit")
      print("")
      
      choice = input("Choose One Input only: ")
      
      print("")
      if choice == "7":                                                                                        #Quit
         break
      if choice == "1":                                                                                        #Trip Duration Only
         if json_status == 0:
            
            print("Trip Duration: " + (json_data["route"]["formattedTime"]))
            print("")
            print("")
      if choice == "2":                                                                                        #Distance Only
         if json_status == 0:
            print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
            print("")
            print("")
      
      if choice == "3":                                                                                        #Fuel only
         if json_status == 0:
            print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
            print("")
            print("")
      if choice == "4":                                                                                        #Directions Only
         if json_status == 0:
            for each in json_data["route"]["legs"][0]["maneuvers"]:
               print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
               print("=============================================\n")
               print("")
               print("")
      if choice == "5":                                                                                         #Display All information
         if json_status == 0:
            print("API Status: " + str(json_status) + " = A successful route call.\n")
            print("=============================================")
            print("Directions from " + (orig) + " to " + (dest))
            print("Trip Duration: " + (json_data["route"]["formattedTime"]))
            print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
            print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
            print("=============================================")
            print("")
            for each in json_data["route"]["legs"][0]["maneuvers"]:
               print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
               print("=============================================\n")
               print("")
               print("")
      if choice == "6":                                                                                           #Try different location
         if json_status == 0:
               orig = input("Starting Location: ")
               dest = input("Destination: ")
               url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType": "shortest"})
               print("URL: " + (url))
               json_data = requests.get(url).json()
               json_status = json_data["info"]["statuscode"]   

         elif json_status == 402:
               print("**********************************************")
               print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
               print("**********************************************\n")

         elif json_status == 611:
               print("**********************************************")
               print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
               print("**********************************************\n")
         else:
               print("************************************************************************")
               print("For Staus Code: " + str(json_status) + "; Refer to:")
               print("https://developer.mapquest.com/documentation/directions-api/status-codes")
               print("************************************************************************\n")
else:
   print("\nSettings go here")