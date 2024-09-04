from fpdf import FPDF
from django.contrib import admin
from django.db.models.query import QuerySet
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest, HttpResponse


@admin.action(description="Print selected tests")
def print_selected_tests(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    th = tuple(["No", "Talabgarnining F.I", "Mutaxasislik", "To'plagan bali", "To'g'ri javoblar", "Texnik nosozlik sababli qo'shilgan ball", ])
    td = []
    i = 1
    for test in queryset:
        td += [(f"{i}", f"{test.user.first_name} {test.user.last_name}", f"{test.spec}", f"{test.percentage}", f"{test.correct}", "", )]
        i += 1
    TABLE = [th] + td

    pdf = FPDF(orientation="landscape")
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(col_widths=(5, 25, 30, 10, 10, 20)) as table:
        for data_row in TABLE:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=tests.pdf"
    return response
