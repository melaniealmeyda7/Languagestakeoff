import sys

class PDFReport:
    def __init__(self, filename, width=595.28, height=841.89):
        self.filename = filename
        self.width = width
        self.height = height
        self.pages_stream = []
        self.cur = []
        self.page_num = 0
        self.y = 0
        self.margin_x = 36
        self.content_w = self.width - 2 * self.margin_x

    def new_page(self):
        if self.cur:
            self.pages_stream.append('\n'.join(self.cur))
            self.cur = []
        self.page_num += 1
        self.y = self.height - 40
        self.draw_header()

    def draw_header(self):
        # Top banner background
        self.rect(self.margin_x, self.height - 62, self.content_w, 36, fill=(0.04, 0.28, 0.52), stroke=None)
        self.text(self.margin_x + 12, self.height - 46, "POLYGLOT MAP  -  PORTAL OFICIAL DE BOOTCAMPS", font="F2", size=13, rgb=(1, 1, 1))
        self.text(self.width - self.margin_x - 170, self.height - 45, "bootcampidiomas.polyglotmap.com", font="F1", size=8.5, rgb=(0.7, 0.88, 1))
        
        # Subtle bar
        self.rect(self.margin_x, self.height - 65, self.content_w, 3, fill=(0.01, 0.73, 0.83), stroke=None)
        self.y = self.height - 85

    def draw_footer(self, total_pages=3):
        # Bottom bar
        self.rect(self.margin_x, 34, self.content_w, 1, fill=(0.8, 0.85, 0.9), stroke=None)
        self.text(self.margin_x, 22, "Polyglot Map - Credenciales Oficiales de Acceso  |  Uso exclusivo de la academia y estudiantes", font="F1", size=8, rgb=(0.4, 0.45, 0.5))
        page_str = f"Pagina {self.page_num} de {total_pages}"
        self.text(self.width - self.margin_x - 65, 22, page_str, font="F2", size=8, rgb=(0.3, 0.35, 0.4))

    def rect(self, x, y, w, h, fill=None, stroke=None, line_width=0.5):
        if line_width:
            self.cur.append(f"{line_width:.2f} w")
        if stroke:
            self.cur.append(f"{stroke[0]:.3f} {stroke[1]:.3f} {stroke[2]:.3f} RG")
        if fill:
            self.cur.append(f"{fill[0]:.3f} {fill[1]:.3f} {fill[2]:.3f} rg")
            op = "B" if stroke else "f"
        else:
            op = "S"
        self.cur.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op}")

    def text(self, x, y, text_str, font="F1", size=9, rgb=(0.1, 0.1, 0.1)):
        # WinAnsiEncoding safe mapping
        t = (text_str
             .replace("—", "-")
             .replace("·", "-")
             .replace("•", "*")
             .replace("“", "\"")
             .replace("”", "\"")
             .replace("’", "'")
             .replace("\\", "\\\\")
             .replace("(", "\\(")
             .replace(")", "\\)"))
        t_latin = t.encode('latin-1', 'replace').decode('latin-1')
        self.cur.append("BT")
        self.cur.append(f"/{font} {size:.1f} Tf")
        self.cur.append(f"{rgb[0]:.3f} {rgb[1]:.3f} {rgb[2]:.3f} rg")
        self.cur.append(f"{x:.2f} {y:.2f} Td")
        self.cur.append(f"({t_latin}) Tj")
        self.cur.append("ET")

    def draw_section_title(self, title, subtitle=None, badge_color=(0.04, 0.58, 0.42)):
        self.rect(self.margin_x, self.y - 18, self.content_w, 22, fill=(badge_color[0]*0.15 + 0.85, badge_color[1]*0.15 + 0.85, badge_color[2]*0.15 + 0.85), stroke=badge_color, line_width=1)
        self.rect(self.margin_x, self.y - 18, 4, 22, fill=badge_color, stroke=None)
        self.text(self.margin_x + 12, self.y - 12, title, font="F2", size=10.5, rgb=badge_color)
        self.y -= 26
        if subtitle:
            self.text(self.margin_x + 2, self.y - 2, subtitle, font="F1", size=8.5, rgb=(0.35, 0.4, 0.45))
            self.y -= 14

    def draw_table(self, col_defs, rows, header_bg=(0.04, 0.28, 0.52)):
        # col_defs: list of (col_name, width, align)
        row_height = 17
        header_height = 19

        # Draw header
        hx = self.margin_x
        self.rect(self.margin_x, self.y - header_height, self.content_w, header_height, fill=header_bg, stroke=None)
        for name, w, align in col_defs:
            self.text(hx + 6, self.y - 13, name, font="F2", size=8.5, rgb=(1, 1, 1))
            hx += w
        self.y -= header_height

        # Draw rows
        for idx, row in enumerate(rows):
            if self.y < 55:
                self.new_page()
                # Re-draw table header
                hx = self.margin_x
                self.rect(self.margin_x, self.y - header_height, self.content_w, header_height, fill=header_bg, stroke=None)
                for name, w, align in col_defs:
                    self.text(hx + 6, self.y - 13, name, font="F2", size=8.5, rgb=(1, 1, 1))
                    hx += w
                self.y -= header_height

            bg = (0.97, 0.98, 0.99) if idx % 2 == 1 else (1, 1, 1)
            self.rect(self.margin_x, self.y - row_height, self.content_w, row_height, fill=bg, stroke=(0.88, 0.90, 0.93), line_width=0.4)
            rx = self.margin_x
            for col_idx, cell in enumerate(row):
                name, w, align = col_defs[col_idx]
                is_bold = (col_idx == 1 and len(row) <= 4) or (col_idx in (2, 3) and "PM-" in str(cell) or "DOC-" in str(cell))
                font = "F2" if is_bold else "F1"
                color = (0.05, 0.2, 0.4) if "DOC-" in str(cell) or "PM-" in str(cell) else (0.1, 0.12, 0.15)
                # If cell is password, highlight with small font
                font_sz = 8.5
                self.text(rx + 6, self.y - 12, str(cell), font=font, size=font_sz, rgb=color)
                rx += w
            self.y -= row_height
        self.y -= 12

    def save(self):
        if self.cur:
            self.pages_stream.append('\n'.join(self.cur))
            self.cur = []

        total_pages = len(self.pages_stream)
        # Re-inject footers into each page stream
        final_pages = []
        for p_idx, stream_text in enumerate(self.pages_stream):
            self.page_num = p_idx + 1
            self.cur = [stream_text]
            self.draw_footer(total_pages=total_pages)
            final_pages.append('\n'.join(self.cur))

        objects = []
        cat_id = 1
        pages_id = 2
        font_reg_id = 3
        font_bold_id = 4
        
        objects.append(None) # 1
        objects.append(None) # 2
        objects.append('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>') # 3
        objects.append('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>') # 4

        page_ids = []
        for page_content in final_pages:
            stream_bytes = page_content.encode('latin-1')
            stream_obj = f'<< /Length {len(stream_bytes)} >>\nstream\n{page_content}\nendstream'
            content_id = len(objects) + 1
            objects.append(stream_obj)

            page_obj = f'''<<
  /Type /Page
  /Parent {pages_id} 0 R
  /MediaBox [0 0 {self.width:.2f} {self.height:.2f}]
  /Contents {content_id} 0 R
  /Resources <<
    /Font <<
      /F1 {font_reg_id} 0 R
      /F2 {font_bold_id} 0 R
    >>
  >>
>>'''
            p_id = len(objects) + 1
            objects.append(page_obj)
            page_ids.append(p_id)

        objects[0] = f'<< /Type /Catalog /Pages {pages_id} 0 R >>'
        kids_str = ' '.join(f'{pid} 0 R' for pid in page_ids)
        objects[1] = f'<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>'

        with open(self.filename, 'wb') as f:
            f.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
            offsets = []
            for i, obj in enumerate(objects):
                offsets.append(f.tell())
                f.write(f'{i+1} 0 obj\n{obj}\nendobj\n'.encode('latin-1'))
            xref_offset = f.tell()
            f.write(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode('latin-1'))
            for off in offsets:
                f.write(f'{off:010d} 00000 n \n'.encode('latin-1'))
            f.write(f'trailer\n<< /Size {len(objects)+1} /Root {cat_id} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n'.encode('latin-1'))
        print(f"Generated {self.filename} ({total_pages} pages)")

teachers = [
    ("Claudia Garcia Conqui", "Ingles A2 (Pre-intermedio)", "claudia.garcia", "DOC-CLA845", "Mie y Vie 10:30am-12:00pm", "meet.jit.si/bootcampingles"),
    ("Jonathan Lima (Brasil, Rio Janeiro)", "Portugues do Zero (Iniciantes)", "jonathan.lima", "DOC-JON629", "Mar y Jue 7:00pm-8:30pm", "meet.jit.si/bootcampportugues"),
]

students = [
    ("1", "Jefferson Miguel Pena Serrano", "jefferson.pena", "PM-JEF842"),
    ("2", "Yeny Fernanda Diaz Longa", "yeny.diaz", "PM-YEN519"),
    ("3", "Gianfranco Jeisson Gil Cabanillas", "gianfranco.gil", "PM-GIA734"),
    ("4", "Piero Alvaro Valdez Solis", "piero.valdez", "PM-PIE628"),
    ("5", "Adriana Chavez", "adriana.chavez", "PM-ADR395"),
    ("6", "Britani Quispe", "britani.quispe", "PM-BRI471"),
    ("7", "Daniela Bonilla", "daniela.bonilla", "PM-DAN963"),
    ("8", "Gaylim Gonzales", "gaylim.gonzales", "PM-GGZ286"),
    ("9", "Melanie Almeyda", "melanie.almeyda", "PM-MEL754"),
    ("10", "Ana De La Cruz", "ana.delacruz", "PM-ANA482"),
    ("11", "Rosa Chavez Callo", "rosa.chavez", "PM-RCC538"),
    ("12", "Julissa Perez Leon", "julissa.perez", "PM-JUL641"),
    ("13", "Ana Martha Chacon Ramos", "ana.chacon", "PM-AMC719"),
    ("14", "Alessandra Morales", "alessandra.morales", "PM-ALE825"),
    ("15", "Katherine Maria Isabel Tiburcio M.", "katherine.tiburcio", "PM-KAT394"),
    ("16", "Rosa Margarita Tocuyo", "rosa.tocuyo", "PM-RMT467"),
    ("17", "Magda Juana Luna Herrera Vda. Mansilla", "magda.luna", "PM-MAG318"),
    ("18", "Estela Esther Noemi Miranda Moreno", "estela.miranda", "PM-EST942"),
    ("19", "Mirna Paola Ferrer Delgado", "mirna.ferrer", "PM-MIR561"),
    ("20", "Carmen Luisa Polo Linares", "carmen.polo", "PM-CLP834"),
    ("21", "Maria Aida Carolina Miranda Moreno", "maria.miranda", "PM-MCM279"),
    ("22", "Christian Edinson Uceda Castaneda", "christian.uceda", "PM-CHR615"),
    ("23", "Sandra Ines Contti Chavez", "sandra.contti", "PM-SAN487"),
    ("24", "Laly Arce Chumpitassi", "laly.arce", "PM-LAL726"),
    ("25", "Vanessa Guerrero Castaneda", "vanessa.guerrero", "PM-VGC391"),
    ("26", "Percy Giancarlo Rios Parravicini", "percy.rios", "PM-PER852"),
    ("27", "Vanessa Rebeca Marin Fernandez", "vanessa.marin", "PM-VRM614"),
    ("28", "Cynthia Jav", "cynthia.jav", "PM-CYN529"),
    ("29", "Carmen Herrera Baldeon", "carmen.herrera", "PM-CHB738"),
    ("30", "Aracely Milagros Roman Loja", "aracely.roman", "PM-ARA943"),
    ("31", "Olga Teresa Poicon Ormeno", "olga.poicon", "PM-OLG739"),
    ("32", "Javier Alfaro", "javier.alfaro", "PM-JAV831"),
    ("33", "Elva Yakelin Yto Quispe", "elva.yto", "PM-EYQ528"),
]

viajeros = [
    ("1", "viajero 1", "PM1-K9X4", "11", "viajero 11", "PM11-W7A3"),
    ("2", "viajero 2", "PM2-R7M2", "12", "viajero 12", "PM12-C2E8"),
    ("3", "viajero 3", "PM3-T4P8", "13", "viajero 13", "PM13-M6Y5"),
    ("4", "viajero 4", "PM4-L6W3", "14", "viajero 14", "PM14-P9U2"),
    ("5", "viajero 5", "PM5-N2Q9", "15", "viajero 15", "PM15-X3B7"),
    ("6", "viajero 6", "PM6-B8V5", "16", "viajero 16", "PM16-V8N4"),
    ("7", "viajero 7", "PM7-H3C7", "17", "viajero 17", "PM17-Q5L9"),
    ("8", "viajero 8", "PM8-F5J2", "18", "viajero 18", "PM18-J2R6"),
    ("9", "viajero 9", "PM9-D9G4", "19", "viajero 19", "PM19-G7T3"),
    ("10", "viajero 10", "PM10-Z4S6", "20", "viajero 20", "PM20-S4K8"),
]

for out_path in [
    "/Users/melaniealmeyda/.gemini/antigravity/scratch/viaje-linguistico-portal/Credenciales_Polyglot_Map_Bootcamp.pdf",
    "/Users/melaniealmeyda/.gemini/antigravity/brain/7cdb6207-c655-4f3f-a523-a085fa5fad5e/Credenciales_Polyglot_Map_Bootcamp.pdf"
]:
    pdf = PDFReport(out_path)
    pdf.new_page()

    # Intro overview
    pdf.text(pdf.margin_x, pdf.y, "LISTADO GENERAL DE ACCESOS Y CREDENCIALES OFICIALES", font="F2", size=13, rgb=(0.04, 0.28, 0.52))
    pdf.y -= 14
    pdf.text(pdf.margin_x, pdf.y, "Enlace de Ingreso al Portal: https://bootcampidiomas.polyglotmap.com/", font="F1", size=9.5, rgb=(0.2, 0.25, 0.3))
    pdf.y -= 22

    # Section 1: Teachers
    pdf.draw_section_title("1. DOCENTES OFICIALES (VISTA EXCLUSIVA DOCENTE)", 
                           subtitle="Visualizan unicamente su propio temario de 8 semanas, horario y enlace de clase virtual.",
                           badge_color=(0.04, 0.58, 0.42))
    teacher_cols = [
        ("Docente", 110, "left"),
        ("Bootcamp Asignado", 115, "left"),
        ("Usuario", 75, "left"),
        ("Contrasena", 65, "left"),
        ("Horario Oficial", 90, "left"),
        ("Sala Virtual", 68, "left")
    ]
    pdf.draw_table(teacher_cols, teachers, header_bg=(0.04, 0.48, 0.35))

    # Section 2: Students
    pdf.draw_section_title("2. ESTUDIANTES INSCRITOS (31 ALUMNOS CON NOMBRE PROPIO)", 
                           subtitle="Pueden ingresar con su usuario con punto (ej. magda.luna) o con su nombre y apellido.",
                           badge_color=(0.02, 0.45, 0.75))
    student_cols = [
        ("#", 28, "left"),
        ("Nombre del Estudiante", 260, "left"),
        ("Usuario de Acceso", 130, "left"),
        ("Contrasena", 105, "left"),
    ]
    pdf.draw_table(student_cols, students, header_bg=(0.02, 0.38, 0.65))

    # Section 3: Travelers
    if pdf.y < 180:
        pdf.new_page()
    pdf.draw_section_title("3. CUENTAS ADICIONALES (VIAJERO 1 AL VIAJERO 20)", 
                           subtitle="Cuentas estandar asignables a estudiantes o monitores adicionales.",
                           badge_color=(0.35, 0.25, 0.75))
    viajero_cols = [
        ("#", 25, "left"),
        ("Usuario", 130, "left"),
        ("Contrasena", 105, "left"),
        ("#", 25, "left"),
        ("Usuario", 130, "left"),
        ("Contrasena", 108, "left"),
    ]
    pdf.draw_table(viajero_cols, viajeros, header_bg=(0.32, 0.22, 0.65))

    pdf.save()
