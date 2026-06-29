# Indian Oil Petrol Pump Receipt Generator

Exact format + logic for Indian Oil (IOCL) thermal receipts used in petrol pumps across India.

This tool generates realistic Indian Oil dispenser receipts matching the real hardware output.

## Features

- **Exact IOCL format** — Matches real thermal printer output (Receipt No, FCC ID, IP/Nozzle, Preset Type, Rate/Volume/Amount, Atot/Vtot, LST/VAT, etc.)
- **Correct business logic**:
  - When `Preset Type = Amount`: `Volume = round(Amount / Rate, 2)`
  - Proper zero-padding exactly as shown on dispenser displays (`00004.92`, `00500.00`, etc.)
- Generates both:
  - Plain text (ready to send to thermal printer)
  - Professional PDF preview **with official Indian Oil logo**
- Fully customizable — change amount, rate, receipt number, dealer details, etc.

## Files

| File                        | Description                              |
|----------------------------|------------------------------------------|
| `generate_indian_oil_receipt.py` | Main Python script                       |
| `indian_oil_receipt.txt`    | Sample text output ready for printer     |
| `logo.png`                  | Official Indian Oil logo                 |

## Quick Start

```bash
python3 generate_indian_oil_receipt.py
```

This will print the receipt to console + save `indian_oil_receipt.txt` and `indian_oil_receipt.pdf` (with logo).

## How to Send to Your Thermal Printer

```bash
lp indian_oil_receipt.txt
# or
cat indian_oil_receipt.txt > /dev/usb/lp0
```

## Customize

Edit parameters in the function call inside the script or import and use programmatically.

## Indian Oil Receipt Logic

```python
volume = round(amount / rate, 2)          # Core calculation when preset by amount
vol_str   = f"{volume:08.2f}"             # 00004.92 style
amt_str   = f"{amount:08.2f}"
```

## Requirements

- Python 3
- `reportlab` (will be installed automatically if missing)

## Use Cases

- Petrol pump software / billing systems
- Thermal printer testing
- Sample receipt generation for development
- Digital records & PDF archiving

---

**Version 1.1** — Includes official Indian Oil logo in PDF

Derived from real receipt example (Zaisa Petroleum, Rajkot)