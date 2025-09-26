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
# Main Program

def main():
    # Step 1 (Hannan)
    region_choice = choose_region()