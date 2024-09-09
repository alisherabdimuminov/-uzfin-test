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


@admin.action(description="Print test question as .txt file")
def print_test_questions(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    content = ""
    for result in queryset:
        print(result)
        for question in result.questions.all():
            print(question.content)
            print("a)", question.answer_a)
            print("b)", question.answer_b)
            print("c)", question.answer_c)
            print("d)", question.answer_d)
            print("correct: ", question.correct)
            content += f"{question.content}\n\na) {question.answer_a}\nb) {question.answer_b}\nc) {question.answer_c}\nd) {question.answer_d}\ncorrect: {question.correct}\n\n"
    response = HttpResponse(content=content, content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename=questions.txt'
    return response


@admin.action(description="Natijani PDF fayl ko'rinishida yuklab olish")
def print_test_answers_as_pdf(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    th = tuple(["ID", "Correct", "Answer", "State"])
    td = []
    pdf = PDF(orientation="landscape")
    for result in queryset:
        for i in result.cases:
            case = result.cases[i]
            td += [(str(i), case.get('correct'), case.get('answer'), 
                    "To'g'ri" if case.get('state') else "Noto'g'ri")
            ]
    TABLE = [th] + td
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(col_widths=[5, 25, 35, 35]) as table:
        for i, data_row in enumerate(TABLE):
            row = table.row()
            for j, datum in enumerate(data_row):
                row.cell(datum)
    response = HttpResponse(content=bytes(pdf.output()), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename=results.pdf'
    return response


@admin.action(description="Natijani TEXT fayl ko'rinishida yuklab olish")
def print_test_answers_as_text(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    html = ""
    for result in queryset:
        for i in result.cases:
            case = result.cases[i]
            html += "{} - {} {} {}\n".format(
                i,
                case.get('correct'),
                case.get('answer'),
                u'\u2705' if case.get('state') else u'\u274c',
            )
    response = HttpResponse(content=html, content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename=results.txt'
    return response
