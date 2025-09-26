# =================================
# 🚌 Bus Ticket Booking System
# =================================
# Guidelines:
# 1. Install Pillow: pip install pillow
# 2. Install qrcode: pip install qrcode
# 3. Run : Click "run" button and click "start debugging" and choose python debugger

from PIL import Image, ImageDraw, ImageFont
import qrcode

print("========================================")
print("      🚌 Bus Ticket Booking System")
print("========================================\n")



def choose_region():
    while True:  
        print("Choose Region:")
        print("1. Peninsular Malaysia")
        print("2. Borneo (Sabah & Sarawak)")
        region_choice = input("Enter choice (1/2): ")
        if region_choice in ["1", "2"]:
            return int(region_choice)
        print("❌ Invalid choice, please enter 1 or 2.\n")

peninsular_terminals = {
    "Kuala Lumpur": ["TBS (Terminal Bersepadu Selatan)"],
    "Selangor": ["Shah Alam Terminal", "Klang Sentral"],
    "Penang": ["Sungai Nibong Terminal", "Butterworth"],
    "Perlis": ["Kangar Terminal"],
    "Kedah": ["Alor Setar Terminal", "Sungai Petani Terminal"],
    "Perak": ["Ipoh Amanjaya", "Taiping Terminal"],
    "Negeri Sembilan": ["Seremban Terminal One"],
    "Melaka": ["Melaka Sentral"],
    "Johor": ["Larkin Sentral (Johor Bahru)", "Mersing Terminal"],
    "Kelantan": ["Kota Bharu Terminal", "Tanah Merah Terminal"],
    "Terengganu": ["Kuala Terengganu MBKT Terminal"],
    "Pahang": ["Kuantan Sentral", "Temerloh Terminal"]
}

borneo_terminals = {
    "Sabah": ["Kota Kinabalu Inanam Terminal", "Sandakan Terminal", "Tawau Terminal"],
    "Sarawak": ["Kuching Sentral", "Sibu Terminal", "Miri Terminal", "Bintulu Terminal"],
    "Labuan": ["Labuan Terminal"]
}

def choose_terminals(region_choice):
    if region_choice == 1:
        terminals = peninsular_terminals
        region_name = "Peninsular Malaysia"
    else:
        terminals = borneo_terminals
        region_name = "Borneo"

    all_terminals = []
    print(f"\nAvailable Bus Terminals in {region_name}:")
    count = 1
    for state, stops in terminals.items():  
        for stop in stops:
            all_terminals.append((stop, state))
            print(f"{count}. {stop} ({state})")
            count += 1

    while True: 
        try:
            dep_index = int(input("\nEnter Departure Terminal (number): ")) - 1
            dest_index = int(input("Enter Destination Terminal (number): ")) - 1
            departure, dep_state = all_terminals[dep_index]
            destination, dest_state = all_terminals[dest_index]
            if departure == destination:
                print("❌ Departure and destination cannot be the same.")
                continue
            return departure, dep_state, destination, dest_state
        except (ValueError, IndexError):
            print("❌ Invalid terminal number, please try again.")     

# Step 3 (Ayra) — compute_distance()

distances_km = {
    ("TBS (Terminal Bersepadu Selatan)", "Sungai Nibong Terminal"): 350,
    ("TBS (Terminal Bersepadu Selatan)", "Larkin Sentral (Johor Bahru)"): 330,
    ("TBS (Terminal Bersepadu Selatan)", "Ipoh Amanjaya"): 200,
    ("TBS (Terminal Bersepadu Selatan)", "Melaka Sentral"): 150,
    ("TBS (Terminal Bersepadu Selatan)", "Klang Sentral"): 30,
    ("TBS (Terminal Bersepadu Selatan)", "Shah Alam Terminal"): 25,
    ("Klang Sentral", "Shah Alam Terminal"): 10,
    ("Sungai Nibong Terminal", "Kangar Terminal"): 180,
    ("Ipoh Amanjaya", "Kota Bharu Terminal"): 400,
    ("Kota Bharu Terminal", "Kuala Terengganu MBKT Terminal"): 170,
    ("Kuantan Sentral", "TBS (Terminal Bersepadu Selatan)"): 260,
}

DEFAULT_SAME_STATE = 50
DEFAULT_DIFF_STATE = 250

def compute_distance(departure, destination, dep_state, dest_state):
    distance = distances_km.get((departure, destination)) or distances_km.get((destination, departure))
    if not distance:
        distance = DEFAULT_SAME_STATE if dep_state == dest_state else DEFAULT_DIFF_STATE
    return distance

# Step 4 (Ezra) — compute_company_fares()

fare_rates = {
    "Budget": {"Standard": 0.11},
    "Economy": {"Standard": 0.13, "VIP": 0.18},
    "Premium": {"VIP": 0.22}
}
borneo_flat_fares = {"Standard": 60, "VIP": 90}

bus_companies_peninsular = {
    "Budget": ["MARA Liner", "Musafir Express", "Cepat Express"],
    "Economy": ["Transnasional", "Plusliner", "Sri Maju Express", "KKKL Express", "Sani Express"],
    "Premium": ["Aeroline", "Super Nice Express", "Billion Stars", "Mutiara LUXE", "Causeway Link Premium Express"]
}
bus_companies_borneo = ["Borneo Express", "Sipitang Express", "Sungei Merah", "Miri Express"]

def compute_company_fares(region_choice, distance):
    company_fares = []
    if region_choice == 1:  # Peninsular fares
        for category, comps in bus_companies_peninsular.items():  # nested for loops
            for company in comps:
                for seat_type, rate in fare_rates[category].items():
                    price = distance * rate
                    company_fares.append((company, seat_type, price))
    return company_fares

# Step 5 (Ipan) — choose_company_and_seat()

def choose_company_and_seat_peninsular(company_fares):
    print("\nAvailable Bus Companies with Fares:")
    for company, seat, price in company_fares:
        print(f"- {company} ({seat}) → RM{price:.2f}")

    while True:  # while loop to validate input
        chosen_company = input("\nEnter chosen Bus Company: ")
        seat_options = [(seat, price) for comp, seat, price in company_fares if comp.lower() == chosen_company.lower()]
        if seat_options:
            break
        print("❌ Invalid company name, please try again.")

    if len(seat_options) == 1:
        chosen_seat_type, price_per_ticket = seat_options[0]
        print(f"\n✅ {chosen_company} only has {chosen_seat_type} → selected automatically.")
    else:
        while True:  # while loop for seat choice
            print("\nAvailable Seat Types:")
            for i, (seat, price) in enumerate(seat_options, start=1):
                print(f"{i}. {seat} → RM{price:.2f}")
            try:
                seat_choice = int(input("Choose seat type (number): "))
                chosen_seat_type, price_per_ticket = seat_options[seat_choice - 1]
                break
            except (ValueError, IndexError):
                print("❌ Invalid choice, please try again.")

    return chosen_company, chosen_seat_type, price_per_ticket

def choose_company_and_seat_borneo():
    print("\nAvailable Bus Companies (Flat Fare):")
    for company in bus_companies_borneo:
        print(f"- {company}")
    while True:
        chosen_company = input("\nEnter chosen Bus Company: ")
        if chosen_company in bus_companies_borneo:
            break
        print("❌ Invalid company name, please try again.")

    while True:  # while loop for seat type
        print("\nSeat Types with Flat Fare:")
        for i, (seat_type, fare) in enumerate(borneo_flat_fares.items(), start=1):
            print(f"{i}. {seat_type} → RM{fare:.2f}")
        try:
            seat_choice = int(input("Choose seat type (number): "))
            chosen_seat_type = list(borneo_flat_fares.keys())[seat_choice - 1]
            price_per_ticket = borneo_flat_fares[chosen_seat_type]
            return chosen_company, chosen_seat_type, price_per_ticket
        except (ValueError, IndexError):
            print("❌ Invalid choice, please try again.")

            # Step 6 (Hannan) — choose_departure_time()

DEPARTURE_TIMES = ["08:00 AM", "01:00 PM", "06:00 PM"]

def choose_departure_time():
    print("\nAvailable Departure Times:")
    for i, time in enumerate(DEPARTURE_TIMES, start=1):
        print(f"{i}. {time}")
    while True:  # while loop for validation
        try:
            choice = int(input("Enter choice (1-3): "))
            if 1 <= choice <= len(DEPARTURE_TIMES):
                return DEPARTURE_TIMES[choice - 1]
            else:
                print("❌ Invalid choice, please select 1-3.")
        except ValueError:
            print("❌ Please enter a valid number.")


# Main Program

def main():
    # Step 1 (Hannan)
    region_choice = choose_region()
    # Step 2 (Kadeesya)
    departure, dep_state, destination, dest_state = choose_terminals(region_choice)
    # Step 3 (Ayra)
    distance = compute_distance(departure, destination, dep_state, dest_state)
     # Step 4 (Ezra)
    company_fares = compute_company_fares(region_choice, distance)
    # Step 5 (Ipan)
    if region_choice == 1:
        chosen_company, chosen_seat_type, price_per_ticket = choose_company_and_seat_peninsular(company_fares)
    else:
        chosen_company, chosen_seat_type, price_per_ticket = choose_company_and_seat_borneo()
   