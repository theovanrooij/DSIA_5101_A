from flask_wtf import Form
from wtforms import StringField,DateField
from wtforms.validators import DataRequired

class studentForm(Form):
    family_name = StringField('Nom', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    birth_date = DateField('Date de naissance', validators=[DataRequired()])
    academic_level = StringField('Niveau scolaire', validators=[DataRequired()])
    class_student = StringField('Classe', validators=[DataRequired()])

class teacherForm(Form):
    family_name_teacher = StringField('Nom', validators=[DataRequired()])
    first_name_teacher = StringField('Prénom', validators=[DataRequired()])
    birth_date_teacher = DateField('Date de naissance', validators=[DataRequired()])

class subjectForm(Form):
    code_subject = StringField('Code de la matière/unité', validators=[DataRequired()])
    name_subject = StringField('Nom de la matière/unité', validators=[DataRequired()])