#!/usr/bin/env python3
"""
Indian Oil Batch Receipt Generator
Based exactly on the original generate_indian_oil_receipt.py layout + randomization
One receipt per page, same style as original single receipt.
"""

import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ============== CONFIG ==============
BASE_RATE = 101.56
DEALER_NAME = "ZAISA PETROLEUM"
DEALER_ADDRESS1 = "JUNA JAKATNAKA"
DEALER_ADDRESS2 = "MORBI ROAD RAJKOT"
FCC_ID = "00000000000972668"


def calculate_volume(amount, rate):
    return round(amount / rate, 2)


def format_volume(v):
    return f"{v:08.2f}"


def format_amount(a):
    return f"{a:08.2f}"


def get_user_input():
    print("=" * 55)
    print("INDIAN OIL BATCH GENERATOR (Original Style)")
    print("=" * 55)
    num = int(input("How many receipts do you want? (e.g. 6): "))
    total = int(input(f"Enter TOTAL amount (e.g. 6000): "))

    print("\nEnter date range for receipts (DD/MM/YY format)")
    start_str = input("Start Date (e.g. 01/04/26): ")
    end_str = input("End Date   (e.g. 30/06/26): ")

    start_date = datetime.strptime(start_str, "%d/%m/%y")
    end_date = datetime.strptime(end_str, "%d/%m/%y")

    return num, total, start_date, end_date


def generate_receipts(num_receipts, total_amount, start_date, end_date):
    amounts = [100] * num_receipts
    remaining = total_amount - (100 * num_receipts)
    for _ in range(remaining // 100):
        amounts[random.randint(0, num_receipts - 1)] += 100
    random.shuffle(amounts)

    # Generate all possible dates in the range
    all_dates = []
    current = start_date
    while current <= end_date:
        all_dates.append(current)
        current += timedelta(days=1)

    if len(all_dates) < num_receipts:
        print(f"Warning: Not enough unique days in range. Using {len(all_dates)} dates.")
        selected_dates = all_dates
    else:
        selected_dates = random.sample(all_dates, num_receipts)  # Unique random dates

    receipts = []

    for i in range(num_receipts):
        rate = round(BASE_RATE + random.uniform(-2, 2), 2)
        volume = calculate_volume(amounts[i], rate)

        d = selected_dates[i]

        # Time
        if random.choice([True, False]):
            t = f"{random.randint(7, 9):02d}:{random.randint(0, 59):02d}"
        else:
            t = f"{random.randint(19, 21):02d}:{random.randint(0, 59):02d}"

        r = {
            "receipt_no": f"F{random.randint(1700, 9999)}",
            "ip_no": str(random.randint(1, 10)),
            "nozzle_no": str(random.randint(1, 10)),
            "rate": rate,
            "volume": volume,
            "amount": amounts[i],
            "date": d.strftime("%d/%m/%y"),
            "time": t,
            "atot": round(random.uniform(108473000, 109500000), 2),
            "vtot": round(random.uniform(1142000, 1155000), 3),
        }
        receipts.append(r)

    return receipts


def draw_receipt_page(c, receipt, page_width, page_height):
    """Draw one receipt using original layout style"""
    margin = 5 * mm
    y = page_height - 12 * mm   # Leave space from top (two blank lines effect)

    # Logo - exactly same placement as original generate_indian_oil_receipt.py
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_width = 32 * mm
        logo_height = logo_width * (144 / 150)
        logo_x = (page_width - logo_width) / 2
        logo_y = page_height - 12 * mm - logo_height   # extra top margin
        c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)
        y = logo_y - 4 * mm

    # Header
    c.setFont("Courier-Bold", 9)
    c.drawCentredString(page_width / 2, y, "Welcomes You")
    y -= 5 * mm

    c.setFont("Courier-Bold", 8)
    c.drawCentredString(page_width / 2, y, DEALER_NAME)
    y -= 3.5 * mm
    c.setFont("Courier", 7)
    c.drawCentredString(page_width / 2, y, DEALER_ADDRESS1)
    y -= 3 * mm
    c.drawCentredString(page_width / 2, y, DEALER_ADDRESS2)
    y -= 5 * mm

    # Separator
    c.setFont("Courier", 7)
    c.drawString(margin, y, "-" * 48)
    y -= 5 * mm

    # Details
    def line(label, value, y_pos):
        c.setFont("Courier", 7)
        c.drawString(margin, y_pos, f"{label} : {value}")
        return y_pos - 4 * mm

    y = line("Receipt No.", receipt["receipt_no"], y)
    y = line("FCC ID", FCC_ID, y)
    y = line("IP No.", receipt["ip_no"], y)
    y = line("Nozzle No.", receipt["nozzle_no"], y)
    y = line("Product", "Petrol", y)
    y -= 2 * mm

    y = line("Preset Type", "Amount", y)
    y = line("Rate(Rs/L)", f"{receipt['rate']:.2f}", y)
    y = line("Volume(L)", f"{receipt['volume']:.2f}", y)
    y = line("Amount(Rs)", f"{receipt['amount']:.2f}", y)
    y -= 2 * mm

    y = line("Atot", f"{receipt['atot']:.2f}", y)
    y = line("Vtot", f"{receipt['vtot']:.3f}", y)
    y -= 3 * mm

    c.drawString(margin, y, "-" * 48)
    y -= 5 * mm

    y = line("Vehicle No", "Not Entered", y)
    y = line("Mobile No", "Not Entered", y)
    y -= 2 * mm

    y = line("Date", receipt["date"], y)
    y = line("Time", receipt["time"], y)
    y -= 3 * mm

    c.drawString(margin, y, "-" * 48)
    y -= 5 * mm

    y = line("CST No", "Not Available", y)
    y = line("LST No", "24091300976", y)
    y = line("VAT No", "Not Available", y)
    y = line("ATTENDANT ID", "Not Available", y)
    y = line("FCC DATE", "Not Available", y)
    y = line("FCC TIME", "Not Available", y)

    y -= 6 * mm
    c.setFont("Courier-Bold", 7)
    c.drawCentredString(page_width / 2, y, "Thank You | Visit Again | Drive Safe")
    y -= 3.5 * mm
    c.setFont("Courier", 6)
    c.drawCentredString(page_width / 2, y, "Indian Oil - The Energy of India")


def main():
    num, total, start_date, end_date = get_user_input()
    receipts = generate_receipts(num, total, start_date, end_date)

    output_path = os.path.join(os.path.dirname(__file__), f"Batch_Receipts_OriginalStyle_{num}.pdf")
    c = canvas.Canvas(output_path, pagesize=(80 * mm, 220 * mm))

    for i, rec in enumerate(receipts):
        if i > 0:
            c.showPage()
        draw_receipt_page(c, rec, 80 * mm, 230 * mm)

    c.save()
    print(f"\n✅ Generated {num} receipts using original layout style.")
    print(f"PDF saved: {output_path}")
    print(f"Total Amount: ₹{sum(r['amount'] for r in receipts)}")


if __name__ == "__main__":
    main()
