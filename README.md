# Indian Oil Petrol Pump Receipt Generator

Exact format + logic for Indian Oil (IOCL) thermal receipts, ready for your printing machine.

## Features
- **Exact replica** of real IOCL dispenser receipts (from Zaisa Petroleum example)
- **Correct business logic**: Volume auto-calculated from Amount × Rate when Preset Type = "Amount"
- **Proper zero-padding** exactly as shown on real IOCL machines (`00004.92`, `00500.00`, etc.)
- Generates both **plain text** (for thermal printers) and **PDF** preview
- Fully customizable via Python function

## Files
- `generate_indian_oil_receipt.py` — Main generator script
- `indian_oil_receipt.txt` — Sample text output (ready to print)
- `indian_oil_receipt.pdf` — Sample PDF version

## Quick Start

```bash
python3 generate_indian_oil_receipt.py
```

This will print the receipt to terminal + save:
- `indian_oil_receipt.txt`
- `indian_oil_receipt.pdf`

## How to Print on Your Thermal Printer

```bash
# Linux example
lp indian_oil_receipt.txt
# or
cat indian_oil_receipt.txt > /dev/usb/lp0
```

Add ESC/POS commands if your printer needs paper cut, bold text, etc.

## Customize a Receipt

Edit the parameters in the script or call the function directly:

```python
from generate_indian_oil_receipt import generate_receipt_text, generate_receipt_pdf

text = generate_receipt_text(
    receipt_no="F1734",
    rate=101.80,
    amount=750.00,
    date_str="29/06/26",
    time_str="21:45",
    vehicle_no="GJ03AB1234"
)
print(text)

generate_receipt_pdf(receipt_no="F1734", amount=750.00, rate=101.80)
```

## Indian Oil Logic Implemented

```python
volume = round(amount / rate, 2)          # Core calculation
vol_str = f"{volume:08.2f}"               # 00004.92 style
amt_str = f"{amount:08.2f}"               # 00500.00 style
```

All other fields (FCC ID, IP/Nozzle, Atot, Vtot, LST No, etc.) match real IOCL format.

## Requirements
- Python 3
- reportlab (auto-installed if missing in the script)

## License
Free to use for your petrol pump / printing needs.

---

**Generated on 29 June 2026** from real Indian Oil receipt photo.
