#!/usr/bin/env python3
"""
Indian Oil Petrol Pump Receipt Generator
Exact format derived from real Indian Oil (IOCL) thermal receipt example.
Includes calculation logic and formatting for printing machines / thermal printers.
Generates both plain text (for direct printing) and PDF preview.
"""

# Auto-install reportlab if missing (for PDF generation with logo)
try:
    from reportlab.lib.pagesizes import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm as reportlab_mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    import subprocess
    import sys
    print("Installing required package: reportlab ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm as reportlab_mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

import os
from datetime import datetime

# ============== INDIAN OIL RECEIPT LOGIC ==============

def calculate_volume(amount_rs, rate_rs_per_l):
    """
    Indian Oil logic: When Preset Type = 'Amount', Volume is calculated as:
    Volume (L) = round(Amount (Rs) / Rate (Rs/L), 2)
    Then formatted with leading zeros to match dispenser display (e.g. 00004.92)
    """
    if rate_rs_per_l <= 0:
        return 0.0
    volume = round(amount_rs / rate_rs_per_l, 2)
    return volume

def format_volume(volume_l):
    """Format volume like dispenser: 00004.92 (8 characters, leading zeros)"""
    return f"{volume_l:08.2f}"

def format_amount(amount_rs):
    """Format amount like dispenser: 00500.00 (8 characters, leading zeros)"""
    return f"{amount_rs:08.2f}"

def format_cumulative_amount(total_rs):
    """Format cumulative Atot with many digits and 2 decimals"""
    return f"{total_rs:013.2f}"

def format_cumulative_volume(total_l):
    """Format cumulative Vtot"""
    return f"{total_l:013.3f}"

# ============== TEXT FORMAT FOR PRINTING MACHINE ==============

def generate_receipt_text(
    receipt_no="F1733",
    fcc_id="00000000000972668",
    ip_no="03",
    nozzle_no="03",
    product="Petrol",
    preset_type="Amount",
    rate=101.56,
    amount=500.00,
    atot=108473947.40,
    vtot=1142998.080,
    vehicle_no="Not Entered",
    mobile_no="Not Entered",
    date_str="23/06/26",
    time_str="13:15",
    cst_no="",
    lst_no="24091300976",
    vat_no="Not Available",
    attendant_id="Not Available",
    fcc_date="Not Available",
    fcc_time="Not Available",
    dealer_name="ZAISA PETROLEUM",
    dealer_address1="JUNA JAKATNAKA",
    dealer_address2="MORBI ROAD RAJKOT",
    tel_no=""
):
    """
    Generates exact Indian Oil style receipt text.
    Ready to send to thermal printer (add ESC/POS commands if needed for your printer model).
    Use \\n for new lines. Fixed width ~42-48 chars for 80mm paper.
    """
    volume = calculate_volume(amount, rate)
    vol_str = format_volume(volume)
    amt_str = format_amount(amount)
    atot_str = format_cumulative_amount(atot)
    vtot_str = format_cumulative_volume(vtot)

    lines = []
    lines.append("=" * 48)
    lines.append("           INDIAN OIL CORPORATION LTD")
    lines.append("                 (IOCL)")
    lines.append("=" * 48)
    lines.append("")
    lines.append("               Welcomes You")
    lines.append("")
    lines.append(dealer_name.center(48))
    lines.append(dealer_address1.center(48))
    lines.append(dealer_address2.center(48))
    if tel_no:
        lines.append(f"Tel. No. : {tel_no}".center(48))
    lines.append("")
    lines.append("-" * 48)
    lines.append(f"Receipt No. : {receipt_no}")
    lines.append(f"FCC ID      : {fcc_id}")
    lines.append(f"IP No.      : {ip_no}")
    lines.append(f"Nozzle No.  : {nozzle_no}")
    lines.append(f"Product     : {product}")
    lines.append("")
    lines.append(f"Preset Type : {preset_type}")
    lines.append(f"Rate(Rs/L)  : {rate:.2f}")
    lines.append(f"Volume(L)   : {vol_str}")
    lines.append(f"Amount(Rs)  : {amt_str}")
    lines.append("")
    lines.append(f"Atot        : {atot_str}")
    lines.append(f"Vtot        : {vtot_str}")
    lines.append("")
    lines.append("-" * 48)
    lines.append(f"Vehicle No  : {vehicle_no}")
    lines.append(f"Mobile No   : {mobile_no}")
    lines.append("")
    lines.append(f"Date        : {date_str}")
    lines.append(f"Time        : {time_str}")
    lines.append("")
    lines.append("-" * 48)
    lines.append(f"CST No      : {cst_no if cst_no else 'Not Available'}")
    lines.append(f"LST No      : {lst_no}")
    lines.append(f"VAT No      : {vat_no}")
    lines.append(f"ATTENDANT ID: {attendant_id}")
    lines.append(f"FCC DATE    : {fcc_date}")
    lines.append(f"FCC TIME    : {fcc_time}")
    lines.append("")
    lines.append("=" * 48)
    lines.append("        Thank You | Visit Again | Drive Safe")
    lines.append("           Indian Oil - The Energy of India")
    lines.append("=" * 48)
    lines.append("")
    lines.append("** This is a computer generated receipt **")
    lines.append("")

    return "\n".join(lines)

# ============== PDF GENERATOR (for preview / records) ==============

def generate_receipt_pdf(
    output_path=None,
    receipt_no="F1733",
    fcc_id="00000000000972668",
    ip_no="03",
    nozzle_no="03",
    product="Petrol",
    preset_type="Amount",
    rate=101.56,
    amount=500.00,
    atot=108473947.40,
    vtot=1142998.080,
    vehicle_no="Not Entered",
    mobile_no="Not Entered",
    date_str="23/06/26",
    time_str="13:15",
    cst_no="",
    lst_no="24091300976",
    vat_no="Not Available",
    attendant_id="Not Available",
    fcc_date="Not Available",
    fcc_time="Not Available",
    dealer_name="ZAISA PETROLEUM",
    dealer_address1="JUNA JAKATNAKA",
    dealer_address2="MORBI ROAD RAJKOT",
    tel_no=""
):
    """
    Generates a PDF that looks like the thermal receipt.
    Page width set to standard 80mm thermal paper width.
    Uses monospace-style font (Courier) for authentic look.
    """
    if output_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "indian_oil_receipt.pdf")

    # Custom receipt page size: 80mm wide, ~220mm tall (enough for content)
    page_width = 80 * mm
    page_height = 220 * mm

    c = canvas.Canvas(output_path, pagesize=(page_width, page_height))

    # Draw Indian Oil logo exactly like in original receipt
    # Looks for logo.png in the same folder as this script (works on Windows/Mac/Linux)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "logo.png")
    logo = ImageReader(logo_path)
    logo_width = 32 * mm
    logo_height = logo_width * (144 / 150)  # preserve aspect ratio from original PNG
    logo_x = (page_width - logo_width) / 2
    logo_y = page_height - 6 * mm - logo_height
    c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)

    # Starting text position below the logo
    y = logo_y - 4 * mm
    left_margin = 5 * mm
    line_height = 4.5 * mm
    font_name = "Courier"
    font_size = 8
    bold_font_size = 9

    def draw_line(text, y_pos, size=font_size, bold=False):
        c.setFont(font_name, size)
        c.drawString(left_margin, y_pos, text)
        return y_pos - line_height

    def draw_centered(text, y_pos, size=font_size):
        c.setFont(font_name, size)
        text_width = c.stringWidth(text, font_name, size)
        x = (page_width - text_width) / 2
        c.drawString(x, y_pos, text)
        return y_pos - line_height

    def draw_separator(y_pos, char="-"):
        c.setFont(font_name, font_size)
        c.drawString(left_margin, y_pos, char * 42)
        return y_pos - line_height

    # Header (logo already drawn above)
    y = draw_centered("Welcomes You", y, bold_font_size)
    y -= 2 * mm

    # Dealer info
    y = draw_centered(dealer_name, y, bold_font_size)
    y = draw_centered(dealer_address1, y)
    y = draw_centered(dealer_address2, y)
    if tel_no:
        y = draw_centered(f"Tel. No. : {tel_no}", y)
    y -= 2 * mm
    y = draw_separator(y)

    # Transaction details
    volume = calculate_volume(amount, rate)
    vol_str = format_volume(volume)
    amt_str = format_amount(amount)
    atot_str = format_cumulative_amount(atot)
    vtot_str = format_cumulative_volume(vtot)

    y = draw_line(f"Receipt No. : {receipt_no}", y)
    y = draw_line(f"FCC ID      : {fcc_id}", y)
    y = draw_line(f"IP No.      : {ip_no}", y)
    y = draw_line(f"Nozzle No.  : {nozzle_no}", y)
    y = draw_line(f"Product     : {product}", y)
    y -= 1 * mm
    y = draw_line(f"Preset Type : {preset_type}", y)
    y = draw_line(f"Rate(Rs/L)  : {rate:.2f}", y)
    y = draw_line(f"Volume(L)   : {vol_str}", y)
    y = draw_line(f"Amount(Rs)  : {amt_str}", y)
    y -= 1 * mm
    y = draw_line(f"Atot        : {atot_str}", y)
    y = draw_line(f"Vtot        : {vtot_str}", y)
    y -= 1 * mm
    y = draw_separator(y)

    # Customer & time
    y = draw_line(f"Vehicle No  : {vehicle_no}", y)
    y = draw_line(f"Mobile No   : {mobile_no}", y)
    y -= 1 * mm
    y = draw_line(f"Date        : {date_str}", y)
    y = draw_line(f"Time        : {time_str}", y)
    y -= 1 * mm
    y = draw_separator(y)

    # Tax & system
    y = draw_line(f"CST No      : {cst_no if cst_no else 'Not Available'}", y)
    y = draw_line(f"LST No      : {lst_no}", y)
    y = draw_line(f"VAT No      : {vat_no}", y)
    y = draw_line(f"ATTENDANT ID: {attendant_id}", y)
    y = draw_line(f"FCC DATE    : {fcc_date}", y)
    y = draw_line(f"FCC TIME    : {fcc_time}", y)
    y -= 2 * mm
    y = draw_separator(y, "=")

    # Footer
    y = draw_centered("Thank You | Visit Again | Drive Safe", y)
    y = draw_centered("Indian Oil - The Energy of India", y)
    y = draw_separator(y, "=")
    y -= 1 * mm
    y = draw_centered("** Computer Generated Receipt **", y, 7)

    c.save()
    print(f"PDF saved to: {output_path}")
    return output_path

# ============== MAIN ==============

if __name__ == "__main__":
    print("=" * 60)
    print("INDIAN OIL RECEIPT GENERATOR")
    print("Exact format + logic for thermal printing machines")
    print("=" * 60)

    # Generate TEXT version (for your printing machine)
    receipt_text = generate_receipt_text()
    print("\n--- TEXT VERSION (copy this to your printer) ---\n")
    print(receipt_text)

    # Save text to file (in same folder as the script - works on Windows too)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    text_path = os.path.join(script_dir, "indian_oil_receipt.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(receipt_text)
    print(f"\nText file saved to: {text_path}")

    # Generate PDF version (for preview / digital records)
    pdf_path = generate_receipt_pdf()  # Will save next to the .py file
    print(f"\nPDF preview saved to: {pdf_path}")

    print("\n" + "=" * 60)
    print("HOW TO USE:")
    print("1. For thermal printer: cat indian_oil_receipt.txt > /dev/usb/lp0   (or use lp command)")
    print("2. Customize: edit the parameters in generate_receipt_text() call")
    print("3. Add ESC/POS commands (e.g. bold, cut) for your specific printer model if needed.")
    print("4. Indian Oil logic: volume = round(amount / rate, 2) with proper zero-padding.")
    print("=" * 60)
