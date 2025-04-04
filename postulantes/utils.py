# postulantes/utils.py (continuación)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime



def generar_pdf_postulante(postulante):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
  
    #doc = SimpleDocTemplate(filename, pagesize=letter)
    doc = SimpleDocTemplate(f"confirmacion_registro_{postulante.dni}.pdf",
                            pagesize=A4
                            )
    # Configurar estilos
    styles = getSampleStyleSheet()
    #style_heading= styles['Heading1']
    #Obtener datos del formulario
    #nombres = request.POST.get('nombres', '')
    #apellido_pa = request.POST.get('apellido_paterno', '')
    #dni = request.POST.get('dni')
    content = []

    #logo_path = 'https://iestparib.edu.pe/wp-content/uploads/2023/08/cropped-logoweb.jpg'
    #imagen_logo = Image(logo_path, width=200, height=50)
    from reportlab.lib.units import cm, inch, mm
    #content.append(Paragraph(f, styles['Normal']))
    #content.append(Paragraph(f'Apellidos: {postulante.apellido_paterno}', styles['Normal']))
    #content.append(Paragraph(f'DNI: {postulante.dni}', styles['Normal']))
    #crear el nombre del archivo con el DNI del postulante
    #filename = f"documentos/ficha_{postulante.dni}.pdf"
    #Datos personales del postulante
    cabecera = ParagraphStyle(name='Cabecera',
                              parent=styles['Normal'],
                              alignment=TA_CENTER,
                              fontSize=8,
                              leading=10
                              )

    image1 = Image('https://iestparib.edu.pe/wp-content/uploads/2023/08/logo_ministerio_educacion.png', (291 / 8) * mm, (58 / 8) * mm)
    image2 = Image('https://iestparib.edu.pe/wp-content/uploads/2023/08/cropped-logoweb.jpg', (669 / 20) * mm, (280 / 20) * mm)
    logobj = [
        (
            image1,
            Paragraph("""INSTITUTO DE EDUCACIÓN SUPERIOR TECNOLÓGICO PÚBLICO<br/>
            "Alianza Renovada Ichuña Bélgica"<br/>
            Resolución Ministerial N° 0353-2004-ED<br/>
            Provincia General Sanchez Cerro - Distrito de Ichuña - Calle Tacna S/N
            """, cabecera),
            image2
        )
    ]
    logo_table = Table(logobj, [1.6 * inch, 3.7 * inch, 1.3 * inch])
    # logo_table.setStyle(PIE_TABLE)
    logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                    ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                                    ('ALIGN', (0, 1), (0, 1), 'CENTER'),
                                    # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                    # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ]))
    content.append(logo_table)
    
    datos_personales = [
        ['DNI:', 'Apellido Paterno', 'Apellido Materno', 'Nombres:'],
        [postulante.dni, postulante.apellido_paterno, postulante.apellido_materno,postulante.nombres],
        ['Correo:',  'N° Celular:', 'Fecha de Nacimiento', 'Género'],
        [postulante.correo, postulante.celular, postulante.fecha_nacimiento, postulante.genero]
    ]
   
    tabla_datos = Table(datos_personales, colWidths=[120, 120])

    # Ajustar el estilo de la tabla
    # Establecer estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, -1), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('BACKGROUND', (0, 2), (-1, 2), colors.grey),
                    ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ])

    tabla_datos.setStyle(style)


    datos_apoderado = [
        ['Apellidos', 'Nombres', 'Parentesco',''],
        [postulante.tutor_apellidos, 
         postulante.tutor_nombres, 
         postulante.tutor_parentesco, '']
    ]

    tabla_apoderado = Table(datos_apoderado, colWidths=[120, 120])

    # Ajustar el estilo de la tabla
    # Establecer estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, -1), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ])

    tabla_apoderado.setStyle(style)

    datos_lugar = [
        ['Lugar', 'Distrito', 'Provincia', 'Departamento'],
        [postulante.lugar_nacimiento, postulante.lugar_nacimiento_distrito, 
         postulante.lugar_nacimiento_provincia, postulante.lugar_nacimiento_departamento]
    ]

    tabla_lugar = Table(datos_lugar, colWidths=[120, 120])

    # Ajustar el estilo de la tabla
    # Establecer estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ])

    tabla_lugar.setStyle(style)

    datos_programa = [
        ['1ra opción', '2da opción', '¿Cómo se entero?', 'Cód. voucher'],
        [postulante.programa_postula_primera_opcion, postulante.programa_postula_segunda_opcion , 
         postulante.enterado_proceso_admision, postulante.codigo_voucher]
    ]

    tabla_programa = Table(datos_programa, colWidths=[120, 120])

    # Ajustar el estilo de la tabla
    # Establecer estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ])

    tabla_programa.setStyle(style)

    datos_informacion = [
        ['Colegio procedencia', '', 'Año egreso', 'Dirección'],
        [postulante.nombre_ies, '', 
         postulante.anio_egreso, postulante.direccion_institucion],
         ['Distrito', 'Provincia', 'Departamento', 'Tipo Inst.'],
         [postulante.institucion_distrito, postulante.institucion_provincia, postulante.institucion_departamento, postulante.tipo_institucion]
    ]

    tabla_información = Table(datos_informacion, colWidths=[120, 120])

    # Ajustar el estilo de la tabla
    # Establecer estilo de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('BACKGROUND', (0, 2), (-1, 2), colors.grey),
                    ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ])

    tabla_información.setStyle(style)

    #content.append(imagen_logo)
    content.append(Spacer(1, 4))
    content.append(Paragraph('Ficha de Postulante ', styles['Title']))
    content.append(Spacer(1, 4))
    content.append(Paragraph('<u>Datos Personales</u>', styles['Heading2']))
    content.append(Spacer(1, 4))
    content.append(tabla_datos)
    content.append(Paragraph('<u>Lugar de Nacimiento</u>', styles['Heading2']))
    content.append(Spacer(1, 4))
    content.append(tabla_lugar)
    content.append(Paragraph('<u>Información Académica</u>', styles['Heading2']))
    content.append(Spacer(1, 4))
    content.append(tabla_información)
    content.append(Paragraph('<u>Programa de Estudios al cual Postular</u>', styles['Heading2']))
    content.append(Spacer(1, 4))
    content.append(tabla_programa)
    content.append(Paragraph('<u>Datos del padre o Apoderado</u>', styles['Heading2']))
    content.append(Spacer(1, 4))
    content.append(tabla_apoderado)

    content.append(Spacer(1, 4))
    content.append(Paragraph("""Declaro bajo juramento que los datos que consigno en la presente FICHA DE POSTULANTE, son verídicos y me remito para la confrontación con los documentos originales.
                De no ser correctos pierdo la vacante de admisión y renuncio a todo derecho que pueda
                obtener.""", styles['Normal']))
    content.append(Spacer(1, 4))

     # Formatear la fecha en el formato deseado
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
    #locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    #elements.append(Paragraph(f"Ichuña, {today.strftime('%d de ')} Marzo del 2024", lugar_fecha))
    content.append(Paragraph(f"Fecha: {fecha_formateada}"))
    content.append(Spacer(1, 6))
    
    firma = [['__________________'],
             ['Firma']]
    firma_table = Table(firma)
    firma_table.setStyle(TableStyle([('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
                                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                     # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                     # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                     ]))
    content.append(firma_table)
    # Construir el PDF
    
    #doc.build([Paragraph(data, style_heading) for data in content])
    doc.build(content)
    #Abrir el pdf y leer su contenido
    with open(f"confirmacion_registro_{postulante.dni}.pdf", 'rb') as file:
        pdf_content = file.read()
     # Construir el PDF
    #doc.build(content)

    # Devolver el nombre del archivo PDF generado
    #return f"confirmacion_registro_{postulante.dni}.pdf"

    return pdf_content

def enviar_pdf_por_correo(postulante, pdf):
    subject = "Ficha de Postulación - IESTP ARIB"
    message = "Adjunto encontrarás tu ficha de postulación."
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [postulante.correo])
    email.attach(f'ficha_postulante_{postulante.dni}.pdf', pdf, 'application/pdf')
    email.send()