# T30: PDF/CSV export functionality
import json, csv
from fpdf import FPDF

def export_to_csv(list_json, filename):
    items = json.loads(list_json)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Store', 'Item'])
        for store, item_list in items.items():
            for item in item_list:
                writer.writerow([store, item])

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Shopping List', 0, 1, 'C')

def export_to_pdf(list_json, filename):
    items = json.loads(list_json)
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    for store, item_list in items.items():
        pdf.cell(0, 10, f'Store: {store}', 0, 1)
        for item in item_list:
            pdf.cell(0, 10, f'  - {item}', 0, 1)
    pdf.output(filename)
