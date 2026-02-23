
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import io
import uuid
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, Image
from reportlab.lib.units import inch
from django.http import FileResponse

def fetch_logo():
    url = "http://localhost:8000/static/project/images/kenya.png"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '').lower()
        if 'svg' in content_type or response.text.startswith('<?xml') or response.text.startswith('<svg'):
            from cairosvg import svg2png
            png_bytes = svg2png(bytestring=response.content, output_width=150, output_height=180)
            return io.BytesIO(png_bytes)
        else:
            return io.BytesIO(response.content)
    except Exception as e:
        print(f"Failed to fetch/convert logo: {e}")
        return None  
    
def create_report_header(elements, styles, logo_buffer):
    if logo_buffer:
        logo = Image(logo_buffer, height=1.4*inch, width=3*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.1*inch))

    school = Paragraph("MWANGANI JUNIOR SCHOOL<br/>PO BOX 16-80405 KINANGO", styles['Title'])
    school.alignment = 1
    elements.append(school)
    elements.append(Spacer(1, 0.2*inch))

    term = Paragraph("END OF TERM 3, 2025", styles['Normal'])
    term.alignment = 1
    elements.append(term)
    elements.append(Spacer(1, 0.2*inch))

def create_student_page(elements, styles, student, logo_buffer):
    create_report_header(elements, styles, logo_buffer)

    grade_name = Paragraph(f"GRADE: SEVEN<br/>NAME: {student['name']}", styles['Normal'])
    elements.append(grade_name)
    elements.append(Spacer(1, 0.3*inch))

    # Table data
    table_data = [['LEARNING AREA', 'SCORE', 'POINTS', 'PERFORMANCE LEVEL']]
    for subj, (score, points, level) in zip(student['subjects'], student['scores']):
        table_data.append([subj, str(score), str(points), level])
    table_data.append(['TOTAL', str(student['total_score']), str(student['total_points']), student['general_level']])

    table = Table(
        table_data,
        colWidths=[250, 60, 60, 120],
        style=[
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
    )
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))

    # Summary
    position_text = f"POSITION: {student['position']} OUT OF: 18" if 'position' in student else ""
    summary = Paragraph(
        f"TOTAL : {student['total_score']} OUT OF: 900 {position_text}<br/>GENERAL PERFORMANCE LEVEL: {student['general_level']}",
        styles['Normal']
    )
    elements.append(summary)
    elements.append(Spacer(1, 0.2*inch))

    dates = Paragraph("CLOSING DATE: 24/10/2025 OPENING DATE: 5/1/2026", styles['Normal'])
    elements.append(dates)
    elements.append(Spacer(1, 0.3*inch))

    teacher_sig = Paragraph("CLASS TEACHER'S SIGNATURE: ....................................", styles['Normal'])
    elements.append(teacher_sig)
    elements.append(Spacer(1, 0.1*inch))

    principal_sig = Paragraph("PRINCIPAL'S SIGNATURE: ....................................", styles['Normal'])
    elements.append(principal_sig)

    elements.append(PageBreak())

def student_report1_generator(request=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    elements = []
    logo_buffer = fetch_logo()

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

if __name__ == "__main__":
    student_report1_generator()