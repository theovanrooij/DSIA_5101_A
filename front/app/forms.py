from flask_wtf import Form
from wtforms import StringField,DateField
from wtforms.validators import DataRequired

class studentForm(Form):
    first_name = StringField('Prénom', validators=[DataRequired()])
    family_name = StringField('Nom', validators=[DataRequired()])
    birth_date = DateField('Date de naissance', validators=[DataRequired()])

class teacherForm(Form):
    first_name_teacher = StringField('Prénom', validators=[DataRequired()])
    family_name_teacher = StringField('Nom', validators=[DataRequired()])
    birth_date_teacher = DateField('Date de naissance', validators=[DataRequired()])
