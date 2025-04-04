from django.db import models
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.
class Postulante(models.Model):    
    """Model definition for Postulante."""
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    CARRERAS_CHOICES = (
        ('C', 'Contabilidad'),
        ('EM', 'Explotación Minera'),
        ('CC', 'Construcción Civil'),
    )

    # TODO: Define fields here
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno  = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    correo = models.EmailField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    celular = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(auto_now=False, auto_now_add=False)
    lugar_nacimiento = models.CharField(max_length=100)
    lugar_nacimiento_distrito = models.CharField(max_length=100, verbose_name='Distrito')
    lugar_nacimiento_provincia = models.CharField(max_length=100, verbose_name = 'Provincia')
    lugar_nacimiento_departamento = models.CharField(max_length=100, verbose_name = 'Departamento')
    tutor_apellidos = models.CharField(max_length=100, blank=True)
    tutor_nombres = models.CharField(max_length=100, blank=True)
    tutor_parentesco = models.CharField(max_length=100, blank=True)
    nombre_ies = models.CharField(max_length=100)
    tipo_institucion = models.CharField(max_length=20, choices=(('Publica', 'Publica'), ('Privada', 'Privada')))
    anio_egreso = models.CharField(verbose_name = 'Año_egreso', max_length=4)
    direccion_institucion = models.CharField(max_length=255)
    institucion_distrito = models.CharField(max_length=100)
    institucion_provincia = models.CharField(max_length=100)
    institucion_departamento = models.CharField(max_length=100)
    programa_postula_primera_opcion = models.CharField(max_length=2, choices=CARRERAS_CHOICES)
    programa_postula_segunda_opcion = models.CharField(max_length=2, choices=CARRERAS_CHOICES)
    enterado_proceso_admision = models.CharField(max_length=100, verbose_name= '¿Cómo se entero del proceso de admisión?')
    codigo_voucher = models.CharField(max_length=15, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # DATOS DE PAGO Y DOCUMENTOS (guardamos las rutas o URLs de Google Drive)
    # DATOS DE PAGO Y DOCUMENTOS (archivos que se subirán a Google Drive vía gdstorage)

    dni_file = models.FileField(upload_to='postulantes/dni/', storage=gd_storage)
    certificado_file = models.FileField(upload_to='postulantes/certificado/', storage=gd_storage)
    recibo_file = models.FileField(upload_to='postulantes/recibo/', storage=gd_storage)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"