# =================================
# 🚌 Bus Ticket Booking System
# =================================
# Guidelines:
# 1. Install Pillow: pip install pillow
# 2. Install qrcode: pip install qrcode
# 3. Run : Click "run" button and click "start debugging" and choose python debugger

from PIL import Image, ImageDraw, ImageFont
import qrcode


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
