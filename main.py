# =================================
# 🚌 Bus Ticket Booking System
# =================================
# Guidelines:
# 1. Install Pillow: pip install pillow
# 2. Install qrcode: pip install qrcode
# 3. Run : Click "run" button and click "start debugging" and choose python debugger

from PIL import Image, ImageDraw, ImageFont
import qrcode


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
time = choose_departure_time()
pax = int(input("Enter Total Passengers: "))

print("\nAvailable Bus Companies:")
for i, company in enumerate(companies, start=1):
    print(f"{i}. {company}")
try:
    company_choice = int(input("Choose your bus company (number): "))
    chosen_company = companies[company_choice - 1]
except (ValueError, IndexError):
    print("\n❌ Invalid company choice. Restart system.")
    exit()

passenger_names = []
for i in range(pax):
    name = input(f"Enter Passenger {i+1} Name: ")
    passenger_names.append(name)

tickets = []
EGGWHITE = "#F0EAD6"

for idx, passenger in enumerate(passenger_names, start=1):
    W, H = 1000, 400
    ticket_img = Image.new("RGB", (W, H), EGGWHITE)
    draw = ImageDraw.Draw(ticket_img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_body = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

       
    border_color = "black"
    border_thickness = 5
    draw.rectangle([(0, 0), (W-1, H-1)], outline=border_color, width=border_thickness)

   
    draw.text((30, 20), f"{chosen_company.upper()}", font=font_title, fill="black")

    
    details = [
        f"Passenger : {passenger}",
        f"From      : {departure}",
        f"To        : {destination}",
        f"Date      : {date}",
        f"Time      : {time}",
        f"Seat Type : {seat_type}",
        f"Price     : RM{price_per_ticket:.2f}",
    ]

    y = 80
    for line in details:
        draw.text((30, y), line, font=font_body, fill="black")
        y += 40

       
    ticket_id = f"{chosen_company[:3].upper()}-{date.replace('/','')}-{passenger[:3].upper()}"
    qr = qrcode.make(ticket_id)
    qr = qr.resize((150, 150))
    ticket_img.paste(qr, (W-200, H-200))

    tickets.append(ticket_img)


stack_height = sum(ticket.height for ticket in tickets)
stacked_img = Image.new("RGB", (tickets[0].width, stack_height), EGGWHITE)

y_offset = 0
for ticket in tickets:
    stacked_img.paste(ticket, (0, y_offset))
    y_offset += ticket.height