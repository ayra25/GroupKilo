# User has to install "pip install pillow qrcode" before running this system
#To run this system, type "python3 bus_ticket.py" in terminal

from PIL import Image, ImageDraw, ImageFont
import qrcode

print("========================================")
print("      🚌 Bus Ticket Booking System")
print("========================================\n")

# Step 1: Ask region
print("Choose Region:")
print("1. Peninsular Malaysia")
print("2. Borneo (Sabah & Sarawak)")
region_choice = input("Enter choice (1/2): ")

# Step 2: Define terminals
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

# Step 3: Bus companies
peninsular_companies = ["Transnasional", "Plusliner", "MARA Liner", "KKKL Express"]
borneo_companies = ["Borneo Express", "Sipitang Express", "Sungei Merah", "Miri Express"]

# Step 4: Pick region
if region_choice == "1":
    terminals = peninsular_terminals
    companies = peninsular_companies
    region_name = "Peninsular Malaysia"
    price_standard = 40
    price_vip = 60
elif region_choice == "2":
    terminals = borneo_terminals
    companies = borneo_companies
    region_name = "Borneo (Sabah & Sarawak)"
    price_standard = 60
    price_vip = 90
else:
    print("\n❌ Invalid choice. Please restart the system.")
    exit()

# Step 5: Flatten all terminals into a list
all_terminals = []
print(f"\nAvailable Bus Terminals in {region_name}:")
count = 1
for state, stops in terminals.items():
    for stop in stops:
        all_terminals.append(stop)
        print(f"{count}. {stop} ({state})")
        count += 1

# Step 6: User chooses terminals by number
try:
    dep_index = int(input("\nEnter Departure Terminal (number): ")) - 1
    dest_index = int(input("Enter Destination Terminal (number): ")) - 1
    departure = all_terminals[dep_index]
    destination = all_terminals[dest_index]
except (ValueError, IndexError):
    print("\n❌ Invalid terminal number. Restart system.")
    exit()

if departure == destination:
    print("\n❌ Departure and destination cannot be the same.")
    exit()

# Step 7: Other inputs
date = input("Enter Travel Date (DD/MM/YYYY): ")
time = input("Enter Departure Time (e.g. 11:30 AM): ")
pax = int(input("Enter Total Passengers: "))

# Step 8: Seat type
print("\nChoose Seat Type:")
print("1. Standard (Normal Coach)")
print("2. VIP (Spacious, 2+1 seating)")
seat_choice = input("Enter choice (1/2): ")

if seat_choice == "1":
    seat_type = "Standard"
    price_per_ticket = price_standard
elif seat_choice == "2":
    seat_type = "VIP"
    price_per_ticket = price_vip
else:
    print("\n❌ Invalid seat choice. Restart system.")
    exit()

# Step 9: Choose bus company
print("\nAvailable Bus Companies:")
for i, company in enumerate(companies, start=1):
    print(f"{i}. {company}")
try:
    company_choice = int(input("Choose your bus company (number): "))
    chosen_company = companies[company_choice - 1]
except (ValueError, IndexError):
    print("\n❌ Invalid company choice. Restart system.")
    exit()

# Step 10: Ask passenger names
passenger_names = []
for i in range(pax):
    name = input(f"Enter Passenger {i+1} Name: ")
    passenger_names.append(name)

# Step 11: Generate stacked tickets (with borders + eggwhite background)
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

    # Border rectangle
    border_color = "black"
    border_thickness = 5
    draw.rectangle([(0, 0), (W-1, H-1)], outline=border_color, width=border_thickness)

    # Company name (header)
    draw.text((30, 20), f"{chosen_company.upper()}", font=font_title, fill="black")

    # Passenger details
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

    # QR Code with passenger info
    ticket_id = f"{chosen_company[:3].upper()}-{date.replace('/','')}-{passenger[:3].upper()}"
    qr = qrcode.make(ticket_id)
    qr = qr.resize((150, 150))
    ticket_img.paste(qr, (W-200, H-200))

    tickets.append(ticket_img)

# Stack all tickets vertically into one image
stack_height = sum(ticket.height for ticket in tickets)
stacked_img = Image.new("RGB", (tickets[0].width, stack_height), EGGWHITE)

y_offset = 0
for ticket in tickets:
    stacked_img.paste(ticket, (0, y_offset))
    y_offset += ticket.height

# Save one combined image
filename = f"tickets_{chosen_company.replace(' ', '_')}_{date.replace('/', '-')}.png"
stacked_img.save(filename)
print(f"🎟 All tickets saved as {filename}")

# Auto open
stacked_img.show()
