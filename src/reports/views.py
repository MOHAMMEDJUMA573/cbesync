import io
import uuid
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
    
def create_report_header(elements, styles, logo_buffer):
    if logo_buffer:
        logo = Image(logo_buffer, height=1.2*inch, width=3*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.1*inch))
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

    school_p1 = Paragraph("MWANGANI JUNIOR SCHOOL", heading1)
    school_p2 = Paragraph("PO BOX 16-80405 KINANGO <br/> END OF TERM 3, 2025", heading2)
    elements.append(school_p1)
    elements.append(school_p2)
    elements.append(Spacer(1, 0.1*inch))

def create_student_page(elements, styles,logo_buffer, student_obj, class_passed):
    #header part
    create_report_header(elements, styles, logo_buffer)
    text1 = ParagraphStyle(
        name="Heading3",
        parent=styles['Heading3'],
        fontSize=12,
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        textColor=black
    )
    term = Paragraph(f"&nbsp; CLASS: <b> <font color=#d90000 size=11 > {class_passed.class_full_str} </font>  <br/> </b>&nbsp NAME: <b> <font color=#d90000 size=11 > {student_obj[0]} </font>  </b>", text1)
    elements.append(term) 
    # first part
    table_data = [['LEARNING AREA', 'SCORE', 'POINTS', 'PERFORMANCE LEVEL']]
    for result_passed in student_obj[1]:
        table_data.append([result_passed.result_subject.subject_name.upper(), result_passed.result_score, str(result_passed.result_p_level[1]), str(result_passed.result_p_level[0])])
    table_data.append(['TOTAL', str(student_obj[2].streport_t_score), str(student_obj[2].streport_points_score), "EE1" ])
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
    row1p2 = Paragraph(f"OUT OF: <b> 900 </b>", text2)
    row2p1 = Paragraph(f"POSITION: <font color=#d90000 size=11 > <b> { str(student_obj[2].streport_c_position)} </b> </font> ", text2)
    row2p2 = Paragraph(f" OUT OF: <b> 18 </b>", text2)
    row3p1 = Paragraph(f"GENERAL PERFORMANCE LEVEL: <font color=#d90000 size=11 > {"EE1"} </font>", text2)
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

    footer = Paragraph(
        "<a href='https://cbesync.com' color='blue'><u>www.cbesync.com</u></a> &nbsp;" "© 2026 cbesync from Eyerision"
    )
    elements.append(footer)
    elements.append(Spacer(1, 0*inch))
    elements.append(PageBreak())

def student_report1_generator(class_passed, exam_passed, request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=10, bottomMargin=36)
    styles = getSampleStyleSheet()
    elements = []
    logo_buffer = fetch_logo(request)
    # Student data from the document
    students_reports_dict = {}
    report_subjects = [
        str(s.subject_name)
        for s in class_passed.class_subjects.all().order_by('subject_name')
    ]
    report_students = [
        s
        for s in class_passed.student_profiles.all().order_by("student_first_name")
    ]
    for student in report_students:
        student_identifier = student.student_id
        student_full_name = f"{student.student_first_name} {student.student_middle_name} {student.student_last_name}"
        student_filtered_rez = [
            result
            for result in student.result_profiles.filter(result_examination=exam_passed).order_by('result_subject__subject_name')
        ]
        student_report_data = StudentEReportProfile.objects.get(
            streport_student = student,
            streport_examination=exam_passed
        )
        students_reports_dict.update({student_identifier:[student_full_name,student_filtered_rez, student_report_data]})
    
    for student_id, student_data in students_reports_dict.items():
        create_student_page(elements, styles, logo_buffer, student_data, class_passed)

    # Remove the last PageBreak
    if elements and isinstance(elements[-1], PageBreak):
        elements.pop()
    doc.build(elements)
    buffer.seek(0)
    filename = f"full_student_report_{uuid.uuid4().hex[:8]}.pdf"

    return FileResponse(buffer, as_attachment=True, filename=filename)


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