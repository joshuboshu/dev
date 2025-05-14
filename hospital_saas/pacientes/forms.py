from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'cedula', 'alergias', 'antecedentes']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilizar todos los campos
        for field in self.fields:
            # Campos de texto normales
            if field not in ['alergias', 'antecedentes']:
                self.fields[field].widget.attrs.update({
                    'class': 'input input-bordered w-full'
                })
            # Textareas
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'textarea textarea-bordered w-full h-24',
                    'rows': 3
                })
        
        # Personalización específica
        self.fields['fecha_nacimiento'].widget.attrs.update({
            'type': 'date',
            'class': 'input input-bordered w-full'
        })