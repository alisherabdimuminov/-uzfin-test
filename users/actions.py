from fpdf import FPDF
from django.contrib import admin
from django.db.models.query import QuerySet
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest, HttpResponse


@admin.action(description="Print selected users")
def print_selected_users(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    th = tuple(["First name", "Last name", "username", "raw", ])
    td = list(queryset.values_list("first_name", "last_name", "username", "raw", ))
    TABLE = [th] + td

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for data_row in TABLE:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=users.pdf"
    return response
