from django import forms
from .models import Postulante

class PostulanteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'type': 'date',  # Esto puede activar el selector de fechas del navegador
            'class': 'bg-gray-50 border border-gray-300 rounded-md py-2 px-3 text-gray-700'
        })
    )
    class Meta:
        model = Postulante
        fields = [
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'dni',
            'correo',
            'genero',
            'celular',
            'fecha_nacimiento',
            'lugar_nacimiento',
            'lugar_nacimiento_distrito',
            'lugar_nacimiento_provincia',
            'lugar_nacimiento_departamento',
            'tutor_apellidos',
            'tutor_nombres',
            'tutor_parentesco',
            'nombre_ies',
            'tipo_institucion',
            'anio_egreso',
            'direccion_institucion',
            'institucion_distrito',
            'institucion_provincia',
            'institucion_departamento',
            'programa_postula_primera_opcion',
            'programa_postula_segunda_opcion',
            'enterado_proceso_admision',
            'codigo_voucher',
            'dni_file',
            'certificado_file',
            'recibo_file',
        ]