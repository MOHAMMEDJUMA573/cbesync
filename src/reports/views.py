from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import io
import uuid
import requests
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.colors import black, navy, red, yellow, lightgrey, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, Image, TableStyle
from reportlab.lib.units import inch
from django.http import FileResponse
from django.contrib.staticfiles import finders
from django.conf import settings
from reportlab.pdfgen import canvas

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

def create_student_page(elements, styles, student, logo_buffer):
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
    term = Paragraph(f"&nbsp; CLASS: <b> <font color=#d90000 size=11 > GRADE 7 NORTH </font>  <br/> </b>&nbsp NAME: <b> <font color=#d90000 size=11 > {student['name']} </font>  </b>", text1)
    elements.append(term) 
    # first part
    table_data = [['LEARNING AREA', 'SCORE', 'POINTS', 'PERFORMANCE LEVEL']]
    for subj, (score, points, level) in zip(student['subjects'], student['scores']):
        table_data.append([subj, str(score), str(points), level])
    table_data.append(['TOTAL', str(student['total_score']), str(student['total_points']), student['general_level']])
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
    row1p1 = Paragraph(f"TOTAL: <font color=#d90000 size=11 > <b> {student['total_score']} </b> </font>", text2)
    row1p2 = Paragraph(f"OUT OF: <b> 900 </b>", text2)
    row2p1 = Paragraph(f"POSITION: <font color=#d90000 size=11 > <b> {student['position']} </b> </font> " if 'position' in student else "", text2)
    row2p2 = Paragraph(f" OUT OF: <b> 18 </b>", text2)
    row3p1 = Paragraph(f"GENERAL PERFORMANCE LEVEL: <font color=#d90000 size=11 > {student['general_level']} </font>", text2)
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

def student_report1_generator(request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=10, bottomMargin=36)
    styles = getSampleStyleSheet()
    elements = []
    logo_buffer = fetch_logo(request)

    # Subjects list (common for all)
    subjects = [
        'SKILLS IN ENGLISH', 'KISWAHILI', 'MATHEMATICS', 'RELIGIOUS EDUCATION',
        'INTEGRATED SCIENCE', 'SOCIAL STUDIES', 'AGRICULTURE AND NUTRITION',
        'CREATIVE ARTS & SPORTS', 'PRE- TECHNICAL'
    ]

    # Student data from the document
    students = [
        {
            'name': 'JUMA MWAZUKA CHAKA',
            'scores': [(39, 2, 'A.E.1'), (68, 3, 'M.E.1'), (44, 2.5, 'M.E.2'), (63, 3, 'M.E.1'),
                       (84, 3.5, 'E.E.2'), (32, 2, 'A.E.1'), (70, 3, 'M.E.1'), (18, 1, 'B.E.1'),
                       (54, 2.5, 'M.E.2')],
            'total_score': 493.5, 'total_points': 22.5, 'general_level': 'M.E.2', 'position': 1
        },
        {
            'name': 'JOHN BASHISHI MANGISI',
            'scores': [(54, 2.5, 'M.E.2'), (72, 3, 'M.E.1'), (46, 2.5, 'M.E.2'), (63, 3, 'M.E.1'),
                       (72, 3, 'M.E.1'), (34, 2, 'A.E.1'), (72, 3, 'M.E.1'), (20, 1, 'B.E.1'),
                       (38, 2, 'A.E.1')],
            'total_score': 492, 'total_points': 22, 'general_level': 'M.E.2', 'position': 2
        },
        {
            'name': 'BORA CHIRIMA',
            'scores': [(21, 1.5, 'A.E.2'), (46, 2.5, 'M.E.2'), (68, 3, 'M.E.1'), (47, 2.5, 'M.E.2'),
                       (72, 3, 'M.E.1'), (36, 2, 'A.E.1'), (70, 3, 'M.E.1'), (18, 1, 'B.E.1'),
                       (46, 2.5, 'M.E.2')],
            'total_score': 444, 'total_points': 21, 'general_level': 'M.E.2', 'position': 3
        },
        {
            'name': 'HALIMA WANINI',
            'scores': [(35, 2, 'A.E.1'), (64, 3, 'M.E.1'), (48, 2.5, 'M.E.2'), (60, 3, 'M.E.1'),
                       (50, 2.5, 'M.E.2'), (32, 2, 'A.E.1'), (52, 2.5, 'M.E.2'), (22, 1.5, 'A.E.2'),
                       (32, 2, 'A.E.1')],
            'total_score': 414.5, 'total_points': 21, 'general_level': 'M.E.2', 'position': 4
        },
        {
            'name': 'ESTHER NDUKU MWONGELA',
            'scores': [(27, 1.5, 'A.E.2'), (46, 2.5, 'M.E.2'), (28, 1.5, 'A.E.2'), (43, 2.5, 'M.E.2'),
                       (50, 2.5, 'M.E.2'), (20, 1, 'B.E.1'), (34, 2, 'A.E.1'), (38, 2, 'A.E.1'),
                       (34, 2, 'A.E.1')],
            'total_score': 335.5, 'total_points': 17.5, 'general_level': 'A.E.1', 'position': 5
        },
        {
            'name': 'CHAKA TSUMA JULO',
            'scores': [(31, 2, 'A.E.1'), (42, 2.5, 'M.E.2'), (8, 0.5, 'B.E.2'), (20, 1, 'B.E.1'),
                       (32, 2, 'A.E.1'), (18, 1, 'B.E.1'), (32, 2, 'A.E.1'), (38, 2, 'A.E.1'),
                       (32, 2, 'A.E.1')],
            'total_score': 266, 'total_points': 15, 'general_level': 'A.E.2', 'position': 7
        },
        {
            'name': 'NDURYA MASINDA',
            'scores': [(25, 1.5, 'A.E.2'), (30, 1.5, 'A.E.2'), (24, 1.5, 'A.E.2'), (53, 2.5, 'M.E.2'),
                       (48, 2.5, 'M.E.2'), (12, 1, 'B.E.1'), (28, 1.5, 'A.E.2'), (14, 1, 'B.E.1'),
                       (18, 1, 'B.E.1')],
            'total_score': 265, 'total_points': 14, 'general_level': 'A.E.2', 'position': 8
        },
        {
            'name': 'BINTI DZAME CHAKA',
            'scores': [(18, 1, 'B.E.1'), (20, 1, 'B.E.1'), (22, 1.5, 'A.E.2'), (53, 2.5, 'M.E.2'),
                       (50, 2.5, 'M.E.2'), (14, 1, 'B.E.1'), (44, 2.5, 'M.E.2'), (33, 2, 'A.E.1'),
                       (30, 1.5, 'A.E.2')],
            'total_score': 297.5, 'total_points': 15.5, 'general_level': 'A.E.1', 'position': 6
        },
        {
            'name': 'ISIAH MAZERA ANDREW',
            'scores': [(24, 1.5, 'A.E.2'), (22, 1.5, 'A.E.2'), (20, 1, 'B.E.1'), (40, 2, 'A.E.1'),
                       (32, 2, 'A.E.1'), (20, 1, 'B.E.1'), (22, 1.5, 'A.E.2'), (28, 1.5, 'A.E.2'),
                       (30, 1.5, 'A.E.2')],
            'total_score': 250, 'total_points': 13.5, 'general_level': 'A.E.2', 'position': 9
        },
        {
            'name': 'GLORIA SAFARI MTINDI',
            'scores': [(19, 1, 'B.E.1'), (28, 1.5, 'A.E.2'), (30, 1.5, 'A.E.2'), (33, 2, 'A.E.1'),
                       (40, 2, 'A.E.1'), (10, 0.5, 'B.E.2'), (32, 2, 'A.E.1'), (20, 1, 'B.E.1'),
                       (24, 1.5, 'A.E.2')],
            'total_score': 248, 'total_points': 13, 'general_level': 'A.E.2', 'position': 10
        },
        {
            'name': 'OMAR MALEJA',
            'scores': [(33, 2, 'A.E.1'), (28, 1.5, 'A.E.2'), (16, 1, 'B.E.1'), (33, 2, 'A.E.1'),
                       (50, 2.5, 'M.E.2'), (14, 1, 'B.E.1'), (26, 1.5, 'A.E.2'), (18, 1, 'B.E.1'),
                       (14, 1, 'B.E.1')],
            'total_score': 244.5, 'total_points': 13.5, 'general_level': 'A.E.2', 'position': 12
        },
        {
            'name': 'MASUDI HAMISI SAIDI',
            'scores': [(23, 1.5, 'A.E.2'), (30, 1.5, 'A.E.2'), (24, 1.5, 'A.E.2'), (33, 2, 'A.E.1'),
                       (36, 2, 'A.E.1'), (18, 1, 'B.E.1'), (36, 2, 'A.E.1'), (18, 1, 'B.E.1'),
                       (16, 1, 'B.E.1')],
            'total_score': 246.5, 'total_points': 13.5, 'general_level': 'A.E.2', 'position': 11
        },
        {
            'name': 'BINTI KAWENDO WANINI',
            'scores': [(18, 1, 'B.E.1'), (20, 1, 'B.E.1'), (16, 1, 'B.E.1'), (27, 1.5, 'A.E.2'),
                       (40, 2, 'A.E.1'), (18, 1, 'B.E.1'), (18, 1, 'B.E.1'), (14, 1, 'B.E.1'),
                       (20, 1, 'B.E.1')],
            'total_score': 200.5, 'total_points': 10.5, 'general_level': 'A.E.2', 'position': 13
        },
        {
            'name': 'CHINGAMBA MWAYOGWE GUNI',
            'scores': [(24, 1.5, 'A.E.2'), (8, 0.5, 'B.E.2'), (20, 1, 'B.E.1'), (37, 2, 'A.E.1'),
                       (20, 1, 'B.E.1'), (10, 0.5, 'B.E.2'), (16, 1, 'B.E.1'), (26, 1.5, 'A.E.2'),
                       (16, 1, 'B.E.1')],
            'total_score': 185.5, 'total_points': 10, 'general_level': 'B.E.1', 'position': 15
        },
        {
            'name': 'MCHEKWISHA ZUHURU NYUNDO',
            'scores': [(21, 1.5, 'A.E.2'), (4, 0.5, 'B.E.2'), (26, 1.5, 'A.E.2'), (17, 1, 'B.E.1'),
                       (18, 1, 'B.E.1'), (16, 1, 'B.E.1'), (16, 1, 'B.E.1'), (34, 2, 'A.E.1'),
                       (20, 1, 'B.E.1')],
            'total_score': 180.5, 'total_points': 10.5, 'general_level': 'B.E.1', 'position': 16
        },
        {
            'name': 'HAMISI TSUMA',
            'scores': [(18, 1, 'B.E.1'), (28, 1.5, 'A.E.2'), (26, 1.5, 'A.E.2'), (23, 1.5, 'A.E.2'),
                       (24, 1.5, 'A.E.2'), (18, 1, 'B.E.1'), (8, 0.5, 'B.E.2'), (24, 1.5, 'A.E.2'),
                       (14, 1, 'B.E.1')],
            'total_score': 192.5, 'total_points': 11, 'general_level': 'A.E.2', 'position': 14
        },
        {
            'name': 'BAKARI NGEMA NGUMBAO',
            'scores': [(1, 0.5, 'B.E.2'), (12, 1, 'B.E.1'), (1, 0.5, 'B.E.2'), (1, 0.5, 'B.E.2'),
                       (30, 1.5, 'A.E.2'), (14, 1, 'B.E.1'), (18, 1, 'B.E.1'), (24, 1.5, 'A.E.2'),
                       (26, 1.5, 'A.E.2')],
            'total_score': 134.5, 'total_points': 9, 'general_level': 'B.E.1', 'position': 18
        },
        {
            'name': 'CHIZI MEJUMAA NDAO',
            'scores': [(20, 1, 'B.E.1'), (2, 0.5, 'B.E.2'), (10, 0.5, 'B.E.2'), (10, 0.5, 'B.E.2'),
                       (10, 0.5, 'B.E.2'), (8, 0.5, 'B.E.2'), (32, 2, 'A.E.1'), (24, 1.5, 'A.E.2'),
                       (18, 1, 'B.E.1')],
            'total_score': 140.5, 'total_points': 8, 'general_level': 'B.E.1', 'position': 17
        },
        {
            'name': 'AVERAGE',
            'scores': [(25.06, 1.5, 'A.E.2'), (31.67, 2, 'A.E.1'), (26.5, 1.5, 'A.E.2'), (36.44, 2, 'A.E.1'),
                       (42.11, 2.5, 'M.E.2'), (19.11, 1, 'B.E.1'), (34.78, 2, 'A.E.1'), (23.94, 1.5, 'A.E.2'),
                       (26.78, 1.5, 'A.E.2')],
            'total_score': 279.5, 'total_points': 15.5, 'general_level': 'A.E.1'
        }
    ]

    for student in students:
        student['subjects'] = subjects  # Add subjects to each
        create_student_page(elements, styles, student, logo_buffer)

    # Remove the last PageBreak
    if elements and isinstance(elements[-1], PageBreak):
        elements.pop()

    doc.build(elements)
    buffer.seek(0)

    filename = f"full_student_report_{uuid.uuid4().hex[:8]}.pdf"
    if request:  # For Django
        return FileResponse(buffer, as_attachment=True, filename=filename)
    else:  # Standalone save
        with open(filename, "wb") as f:
            f.write(buffer.getvalue())
        print(f"PDF saved as {filename}")

def student_report_table_generator(request=None):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate("hello.pdf", pagesize=A4)
    elements = []

    data = [
        ['Header 1', 'Header 2', 'Header 3', 'Longer Header 4'],
        ['Row 1 Col1', Paragraph("<b>Bold & <font color=red>red</font></b>", styles['Normal']), '123.45', 'extra'],
        ['Row 2', ' merged →', '', 'value'],
        ['Row 3', 'data', '999', 'last'],
        ['Footer', 'Total', '', '1,234.56'],
    ]

    t = Table(
        data,
        colWidths=[1.2*inch, 1.8*inch, 1*inch, 1.5*inch],
        rowHeights=None,               # auto
        repeatRows=1,                  # repeat header on split
        spaceBefore=12,
        spaceAfter=24,
        cornerRadii=[8, 8, 4, 4]       # rounded corners
    )

    style = TableStyle([
        # headers
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('ALIGN',      (0,0), (-1,0), 'CENTER'),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 12),

        # footer
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ('ALIGN',      (0,-1), (-1,-1), 'RIGHT'),
        ('FONTNAME',   (0,-1), (-1,-1), 'Helvetica-Bold'),

        # alternating rows
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.beige]),

        # lines
        ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
        ('BOX',        (0,0), (-1,-1), 1.5, colors.black),

        # span example
        ('SPAN',       (1,2), (2,2)),
        ('ALIGN',      (1,2), (2,2), 'CENTER'),
        ('VALIGN',     (1,2), (2,2), 'MIDDLE'),
        ('BACKGROUND', (1,2), (2,2), colors.lavender),

        # split decoration (only appears when table actually splits)
        ('LINEABOVE',  (0,'splitlast'), (-1,'splitlast'), 4, colors.purple),
        ('LINEBELOW',  (0,'splitfirst'), (-1,'splitfirst'), 4, colors.orange),
    ])

    t.setStyle(style)
    elements.append(t)
    doc.build(elements)

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