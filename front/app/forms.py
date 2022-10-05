from flask_wtf import Form
from wtforms import StringField,DateField
from wtforms.validators import DataRequired

class studentForm(Form):
    first_name = StringField('Prénom', validators=[DataRequired()])
    family_name = StringField('Nom', validators=[DataRequired()])
    birth_date = DateField('Date de naissance', validators=[DataRequired()])
