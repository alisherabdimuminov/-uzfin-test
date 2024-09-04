from fpdf import FPDF, FontFace
from django.contrib import admin
from django.db.models.query import QuerySet
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest, HttpResponse

class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("logo.png", 5, 5, 20)
        self.set_font("helvetica", "B", 15)
        self.cell(80)
        self.cell(30, 10, "O'zbekiston-Finlandiya pedagogika instituti test markazi.", align="L")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Platform powered by Ali", align="C")


@admin.action(description="Print selected tests")
def print_selected_tests(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset = queryset.order_by("-percentage")
    th = tuple(["No", "Talabgarnining F.I", "Mutaxasislik", "To'plagan bali", "To'g'ri javoblar", "Texnik nosozlik sababli qo'shilgan ball", ])
    td = []
    i = 1
    for test in queryset:
        td += [(f"{i}", f"{test.user.first_name} {test.user.last_name}", f"{test.spec}", f"{test.percentage}", f"{test.correct}", "", )]
        i += 1
    TABLE = [th] + td

    pdf = PDF(orientation="landscape")
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(col_widths=(5, 25, 30, 10, 10, 20), text_align=("CENTER", "LEFT", "LEFT", "CENTER", "CENTER", "LEFT")) as table:
        for data_row in TABLE:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=tests.pdf"
    return response
