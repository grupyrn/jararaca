from pathlib import Path
import string
import xlsxwriter
from io import StringIO

from django import conf


def generate_xlsx(stream, queryset, fields):
    workbook = xlsxwriter.Workbook(stream, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    Model = queryset.model
    raw_fields = [field for field in Model._meta.get_fields() if field.name in fields]

    for i, header in enumerate(raw_fields):
        worksheet.write(5, i, str(header.verbose_name).capitalize(), bold)

    for n_row, row in enumerate(queryset.all()):
        n_row = n_row + 1
        # worksheet.write(n_row+5, 0, row)  # name column
        for col, field in enumerate(fields):
            try:
                worksheet.write(n_row+5, col, getattr(row, field))
            except:
                worksheet.write(n_row + 5, col, str(getattr(row, field)))
    for letter in string.ascii_uppercase[:len(fields)]:
        worksheet.set_column(f'{letter}:{letter}', 25)
    logo_path = Path(conf.settings.BASE_DIR) / 'staticfiles' / 'img' / 'logo_small.png'

    worksheet.insert_image('A1', logo_path, {'x_offset': 15, 'y_offset': 12})
    workbook.close()

    return workbook

