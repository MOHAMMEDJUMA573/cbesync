import io
import uuid
import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.colors import black, navy, red, yellow, lightgrey, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, Image, TableStyle
from reportlab.lib.units import inch
from django.http import FileResponse
from django.contrib.staticfiles import finders
from reports.models import StudentEReportProfile
from results.models import ResultsProfile
from django.db.models import Prefetch, OuterRef, Subquery
from django.http import HttpResponse

#000->Helper (UNIVERSAL)
def fetch_logo(request):
    path = finders.find('project/images/moe.png')
    if path is None:
        print("Static file not found")
        return None
    try:
        with open(path, 'rb') as f:
            return io.BytesIO(f.read())
    except Exception as e:
        print(f"Failed to read static file: {e}")
        return None 
styles = getSampleStyleSheet()
heading1 = ParagraphStyle(
    name='Heading1',
    parent=styles['Heading1'],
    fontSize=18,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
    textColor=black,
)
heading2 = ParagraphStyle(
    name='Heading2',
    parent=styles['Heading2'],
    fontSize=12,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
    textColor=black
)
#001->Helper 
def create_report_header(elements, styles, logo_buffer, class_passed, exam_passed):
    if logo_buffer:
        logo = Image(logo_buffer, height=0.8*inch, width=2*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.1*inch))
    school_p1 = Paragraph(f"{class_passed.class_school.school_name.upper()}", heading1)
    school_p2 = Paragraph(f"P.O BOX {class_passed.class_school.school_postal_box} <br/> {exam_passed.examination_period.upper()} OF TERM {exam_passed.examination_term[2:]}, {exam_passed.examination_year}", heading2)
    elements.append(school_p1)
    elements.append(school_p2)
#001->Helper
def create_student_page(elements, styles,logo_buffer, student_obj, class_passed, exam_passed):
    #header part
    create_report_header(elements, styles, logo_buffer, class_passed, exam_passed)
    text1 = ParagraphStyle(
        name="Heading3",
        parent=styles['Heading3'],
        fontSize=12,
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        textColor=black
    )
    term = Paragraph(f"&nbsp; CLASS: <b> <font color=#d90000 size=11 > GRADE {class_passed.class_level} </font>  <br/> </b>&nbsp NAME: <b> <font color=#d90000 size=11 > {student_obj[0].upper()} </font>  </b>", text1)
    elements.append(term) 
    # first part
    table_data = [['LEARNING AREA', 'SCORE', 'POINTS', 'PERFORMANCE LEVEL']]
    for result_passed in student_obj[1]:
        table_data.append(
            [
                result_passed.result_subject.subject_name.upper(),
                result_passed.result_score,
                str(result_passed.result_p_level[1]),
                str(result_passed.result_p_level[0])
            ]
        )
    table_data.append(
        [
            'TOTAL',
            str(student_obj[2].streport_t_score),
            str(student_obj[2].streport_points_score),
            str(student_obj[2].streport_p_level)
        ]
    )
    table1 = Table(
        table_data,
        rowHeights=0.3*inch,
        colWidths=[250, 60, 60, 120],
        style=[
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (-1, 1), (-1, -1), colors.navy),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
    )
    elements.append(table1)
    elements.append(Spacer(1, 0.3*inch))
    #second part
    text2 = ParagraphStyle(
        name="Heading3",
        parent=styles['Heading3'],
        fontSize=12,
        alignment=TA_LEFT,
        fontName="Helvetica",
        textColor=black
    )
    row1p1 = Paragraph(f"TOTAL: <font color=#d90000 size=11 > <b> { str(student_obj[2].streport_t_score)} </b> </font>", text2)
    row1p2 = Paragraph(f"OUT OF: <b>{len(student_obj[1])*100}</b>", text2)
    row2p1 = Paragraph(f"POSITION: <font color=#d90000 size=11 > <b> { str(student_obj[2].streport_c_position)} </b> </font> ", text2)
    row2p2 = Paragraph(f" OUT OF: <b> {class_passed.student_profiles.all().count()} </b>", text2)
    row3p1 = Paragraph(f"GENERAL PERFORMANCE LEVEL: <font color=#d90000 size=11 > {str(student_obj[2].streport_p_level)} </font>", text2)
    row3p2 = Paragraph(f"")
    table1_data = [
        [row1p1, row1p2],
        [row2p1, row2p2],
        [row3p1, row3p2]
    ]
    table1 = Table(
        table1_data,
        colWidths=[300, 120],
        style=[
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ],
    )
    elements.append(table1)
    elements.append(Spacer(1, 0.3*inch))
    #last report part
    row1p1 = Paragraph(".....................................................<br/> CLASS TEACHER'S SIGNATURE:<br/> &nbsp; ", styles['Normal'])
    row2p1 = Paragraph(".....................................................<br/> PRINCIPAL'S SIGNATURE:<br/> &nbsp;", styles['Normal'])
    table3_data = [
        [row1p1],
        [row2p1]
    ]
    table3 = Table(
        table3_data,
        colWidths=[200],
        rowHeights=1*inch,
        style=[
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ],
        hAlign='LEFT'
    )
    elements.append(table3)
    elements.append(Spacer(1, 0.8*inch))
    footer = Paragraph(f"<a href='https://cbesync.com' color='green'><u>www.cbesync.com</u></a> &nbsp; © 2026 cbesync -: {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    elements.append(footer)
    elements.append(Spacer(1, 0*inch))
    elements.append(PageBreak())
#001->Helper
def create_classreport_page(elements, styles, logo_buffer, students_reports_dict, class_passed, exam_passed):
    #header part
    create_report_header(elements, styles, logo_buffer, class_passed, exam_passed)
    text1 = ParagraphStyle(
        name="Heading3",
        parent=styles['Heading3'],
        fontSize=9,
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        textColor=black
    )
    class_data = Paragraph(f"&nbsp; CLASS: <b> <font color=#d90000 size=9 > GRADE {class_passed.class_level} </font> &nbsp; </b>&nbsp CLASS TEACHER: <b> <font color=#d90000 size=9 > {class_passed.class_teacher.teacher_official_name} </font>  </b>", text1)
    elements.append(class_data)
    # first part
    table_data = [['STUDENT NAME', 'SCORE', 'POINTS', 'P.LEVEL', 'POS']]
    student_subjects = [
        s.subject_code
        for s in class_passed.class_subjects.order_by("subject_name")
    ]
    student_subjects_cols = [
        35
        for subject in student_subjects
    ]
    table_data[0][1:1] = student_subjects
    #Student records fill
    table_data[1:] = [
        [
            f"{student_id.student_first_name.upper()} {student_id.student_middle_name[:1].upper()} {student_id.student_last_name.upper()}"[:21],
            *[
                str(result.result_score)
                for result in student_data[1]
            ],
            student_data[2].streport_t_score,
            student_data[2].streport_points_score,
            student_data[2].streport_p_level,
            student_data[2].streport_c_position         
        ]
        for student_id, student_data in students_reports_dict.items()
    ]
    table1 = Table(
        table_data,
        rowHeights=0.25*inch,
        colWidths=[110,*student_subjects_cols,40,40,45,35],
        style=[
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (-1, 1), (-1, -1), colors.navy),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
    )
    elements.append(table1)

    #footer at the end
    elements.append(Spacer(1, 0.8*inch))
    footer = Paragraph(f"<a href='https://cbesync.com' color='green'><u>www.cbesync.com</u></a> &nbsp; © 2026 cbesync -: {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    elements.append(footer)
    elements.append(Spacer(1, 0*inch))
    elements.append(PageBreak())
#main class reports generator from admin(school) -> 001
def student_report1_generator(class_passed, exam_passed, request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=10,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    elements = []
    logo_buffer = fetch_logo(request)
    # Student data from the document
    students_qs = (
        class_passed
        .student_profiles.all()
        .annotate(
            total_score=Subquery(
                StudentEReportProfile.objects.filter(
                    streport_student=OuterRef('pk'),
                    streport_examination=exam_passed,
                )
                .values('streport_t_score')[:1]
            )
        )
        .order_by('-total_score', 'student_first_name')
    )
    results_qs = (
        ResultsProfile.objects.filter(
            result_examination=exam_passed,
            result_student__in=students_qs,
        )
        .select_related('result_subject', 'result_student')
        .order_by('result_subject__subject_name')
    )
    ereport_qs = StudentEReportProfile.objects.filter(
        streport_examination = exam_passed,
        streport_student__in = students_qs
    )
    students_qs = students_qs.prefetch_related(
        Prefetch('result_profiles', queryset=results_qs, to_attr='prefetched_results'),
        Prefetch('stereport_profile', queryset=ereport_qs, to_attr='prefetched_ereport'),
    )
    students_reports_dict = {
        student: [
            f"{student.student_first_name} {student.student_middle_name} {student.student_last_name}",
            student.prefetched_results,
            student.prefetched_ereport[0] if student.prefetched_ereport else None
        ] for student in students_qs
    }
    create_classreport_page(elements, styles, logo_buffer, students_reports_dict, class_passed, exam_passed)

    for student_id, student_data in students_reports_dict.items():
        create_student_page(elements, styles, logo_buffer, student_data, class_passed, exam_passed)
    # Remove the last PageBreak
    if elements and isinstance(elements[-1], PageBreak):
        elements.pop()
    doc.build(elements)
    buffer.seek(0)
    filename = f"full_student_report_{uuid.uuid4().hex[:8]}.pdf"

    return FileResponse(buffer, as_attachment=True, filename=filename)

#002->Helper
def create_stledger_class_header(elements, styles, logo_buffer,class_passed):
    if logo_buffer:
        logo = Image(logo_buffer, height=0.8*inch, width=2*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.1*inch))
    school_p1 = Paragraph(f"{class_passed.class_school.school_name.upper()}", heading1)
    school_p2 = Paragraph(f"P.O BOX {class_passed.class_school.school_postal_box} <br/> {class_passed.class_level_str.upper()} OF {class_passed.class_creation_date.year}", heading2)
    elements.append(school_p1)
    elements.append(school_p2)
#002->Helper
def create_stledger_class_page(elements, styles, logo_buffer, class_passed):
    create_stledger_class_header(elements, styles, logo_buffer,class_passed)
    #first part
    free_cols = 7
    table_data = [
        ["No","STUDENT FULL NAME","G","STUDENT_ID",*["V" for i in range(free_cols)]]
    ]
    class_students = list(class_passed.student_profiles.all().order_by("student_id"))
    table_data[1:] = [
        [
            int(class_students.index(st))+1, f"{st.student_first_name} {st.student_middle_name} {st.student_last_name}",
            str(st.student_gender),str(st.student_id),*[" " for i in range(free_cols)]
        ]
        for st in class_students
    ]
    data_table = Table(
        table_data,
        rowHeights=0.25*inch,
        colWidths=[40,190,30,100,*[30 for i in range(free_cols)]],
        style=[
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (-1, 1), (-1, -1), colors.navy),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('FONTSIZE', (1, 1), (1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
    )
    elements.append(data_table)
    #footer at the end
    elements.append(Spacer(1, 0.8*inch))
    footer = Paragraph(f"<a href='https://cbesync.com' color='green'><u>www.cbesync.com</u></a> &nbsp; © 2026 cbesync -: {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    elements.append(footer)
    elements.append(Spacer(1, 0*inch))
    elements.append(PageBreak())
#main students ledger generator from admin(school) -> 002
def student_ledger_generator(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    current_school = request.user.school_profile
    c_school_classes = current_school.class_profiles.all().order_by("class_level","class_title")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=10,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    elements = []
    logo_buffer = fetch_logo(request)

    for st_class in c_school_classes:
        create_stledger_class_page(elements,styles,logo_buffer,st_class)

    # Remove the last PageBreak
    if elements and isinstance(elements[-1], PageBreak):
        elements.pop()
    doc.build(elements)
    buffer.seek(0)
    filename = f"SCHOOL_LEDGER:{uuid.uuid4().hex[:8].upper()}.pdf"

    return FileResponse(buffer, as_attachment=True, filename=filename)

#Learn func -> 000
def student_report_paragraph_gen(request=None):
        # Create the document
    doc = SimpleDocTemplate(
        "hello.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles we'll use
    normal = styles['Normal']

    heading1 = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=18,
        fontName="Times-Roman",
        leading=22,
        spaceAfter=12,
        textColor=navy
    )

    body = ParagraphStyle(
        'Body',
        parent=normal,
        fontName="Times-Roman",
        fontSize=11,
        leading=14,
        spaceAfter=8,
        alignment=TA_JUSTIFY
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body,
        leftIndent=20,
        firstLineIndent=-20,
        bulletIndent=10,
        bulletFontName='Symbol',
        bulletFontSize=14,
        spaceAfter=6
    )

    number_style = ParagraphStyle(
        'Numbered',
        parent=body,
        leftIndent=25,
        firstLineIndent=-25,
        spaceAfter=6
    )

    definition_style = ParagraphStyle(
        'Definition',
        parent=body,
        leftIndent=40,
        firstLineIndent=-40,
        spaceAfter=10,
        backColor=lightgrey,
        borderWidth=0.5,
        borderColor=colors.grey,
        borderPadding=(6,6,6,6),
        borderRadius=4
    )

    centered = ParagraphStyle(
        'Centered',
        parent=body,
        alignment=TA_CENTER,
        fontSize=12,
        textColor=red,
        spaceBefore=12,
        spaceAfter=12
    )

    story = []

    # Title
    story.append(Paragraph("ReportLab Paragraph Features Demo", heading1))
    story.append(Spacer(1, 0.3*inch))

    # 1. Basic paragraph with inline styles
    story.append(Paragraph(
        "<b>Bold</b> text and <i>italic</i> text. "
        "Also <u>underlined</u> and <strike>strikethrough</strike>. "
        "Font change: <font name=Helvetica-Bold color=red size=14>important!</font>",
        body
    ))
    story.append(Spacer(1, 0.2*inch))

    # 2. Superscript, subscript, greek
    story.append(Paragraph(
        "Physics example: E = mc<font name=Symbol>2</font> "
        "→ <super>E = m c<super>2</super></super><br/>"
        "Math: <greek>a</greek><super>2</super> + <greek>b</greek><super>2</super> = <greek>c</greek><super>2</super>",
        body
    ))
    story.append(Spacer(1, 0.3*inch))

    # 3. Bulleted list (using <bullet>)
    story.append(Paragraph("Bullet List Examples:", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph(
        "<bullet>&bull;</bullet>This is a very long bullet point that should wrap nicely to the next line and demonstrate how indentation works.",
        bullet_style
    ))
    story.append(Paragraph(
        "<bullet>★</bullet>Another item with a different bullet character.",
        bullet_style
    ))
    story.append(Spacer(1, 0.2*inch))

    # 4. Numbered list using <seq>
    story.append(Paragraph("Numbered List with <seq>:", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph(
        "<seqreset id='item'/> <seq id='item'/>. First important step that wraps over multiple lines because the text is quite verbose.",
        number_style
    ))
    story.append(Paragraph(
        "<seq id='item'/>. Second step – with <b>bold</b> and <i>italic</i> inline.",
        number_style
    ))
    story.append(Paragraph(
        "<seq id='item'/>. Third step.",
        number_style
    ))
    story.append(Spacer(1, 0.3*inch))

    # 5. Definition list style (hanging indent + background)
    story.append(Paragraph("Definition-List Style:", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph(
        "<b>Python</b>   A high-level, interpreted programming language known for readability and versatility.",
        definition_style
    ))
    story.append(Paragraph(
        "<b>ReportLab</b>   A powerful PDF generation library for Python that supports Platypus flowables like Paragraph.",
        definition_style
    ))
    story.append(Spacer(1, 0.3*inch))

    # 6. Inline image + link + anchor
    story.append(Paragraph(
        "Inline image example (remote): "
        "<img src='https://i.imgur.com/T29gwIr.png' width='120' height='40' valign='middle'/> "
        "and a <link href='https://cbesync.com' color='blue'><u>hyperlink</u></link>.<br/>"
        "Or jump to <a href='#bottom' color='navy'>the bottom of the page</a>.",
        body
    ))
    story.append(Spacer(1, 0.4*inch))

    # Centered colored paragraph
    story.append(Paragraph(
        "This paragraph is centered and has red text!",
        centered
    ))

    # Anchor at bottom
    story.append(Paragraph("<a name='bottom'/>", body))  # invisible anchor

    story.append(PageBreak())

    # Bonus: Small table with a paragraph cell
    data = [
        [Paragraph("This cell contains a <b>Paragraph</b> with <font color=purple>colored</font> text and <super>superscript</super>.", body)],
        ["Just plain text cell"]
    ]

    t = Table(data, colWidths=[4.5*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (1,0), (1,0), HexColor('#f0f0f0')),
    ]))

    story.append(Paragraph("Example Table with Paragraph inside:", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    story.append(t)

    # Build the PDF
    doc.build(story)

    print("PDF created: paragraph_demo.pdf")
if __name__ == "__main__":
    student_report_paragraph_gen()