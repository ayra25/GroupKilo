# =================================
# 🚌 Bus Ticket Booking System
# =================================
# Guidelines:
# 1. Install Pillow: pip install pillow
# 2. Install qrcode: pip install qrcode
# 3. Run : Click "run" button and click "start debugging" and choose python debugger

from PIL import Image, ImageDraw, ImageFont
import qrcode

# Step 1: Ask region
print("Choose Region:")
print("1. Peninsular Malaysia")
print("2. Borneo (Sabah & Sarawak)")
region_choice = input("Enter choice (1/2): ")


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

peninsular_companies = ["Transnasional", "Plusliner", "MARA Liner", "KKKL Express"]
borneo_companies = ["Borneo Express", "Sipitang Express", "Sungei Merah", "Miri Express"]

fare_rates = {
    "Budget": {"Standard": 0.11},
    "Economy": {"Standard": 0.13, "VIP": 0.18},
    "Premium": {"VIP": 0.22}
}
borneo_flat_fares = {"Standard": 60, "VIP": 90}

if region_choice == "1":
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
        break
    except (ValueError, IndexError):
        print("❌ Invalid terminal number, please try again.")

date = input("Enter Travel Date (DD/MM/YYYY): ")
time = input("Enter Departure Time (e.g. 11:30 AM): ")
pax = int(input("Enter Total Passengers: "))



def get_passenger_names(pax):
    return [input(f"Enter Passenger {i+1} Name: ") for i in range(pax)]