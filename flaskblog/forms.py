from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,IntegerField,PasswordField, SubmitField, BooleanField,DateField,RadioField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class ConsentForm(FlaskForm):
    consent1 = BooleanField('I confirm that I have read the Participant Information Sheet (version 1), dated (May 2020) for the above study. I have had the opportunity to consider the information and ask questions about the study.',validators=[DataRequired()])
    consent2 = BooleanField('I confirm that I have had such questions answered satisfactorily.',validators=[DataRequired()])
    consent3 = BooleanField('I understand that my participation is voluntary and I may withdraw at any time without reason, and without affecting my subsequent treatment or legal rights.',validators=[DataRequired()])
    consent4 = BooleanField('Subject to clause 4 below, I understand that all data collected will be confidential, anonymised and subject to the provisions of the Data Protection Act 2018 (as amended from time to time).',validators=[DataRequired()])
    consent5 = BooleanField('I understand that data from the study may be reviewed by members of the research team, or by regulatory authorities where relevant to the research. I give permission for this access.',validators=[DataRequired()])
    consent6 = BooleanField('I understand that the outcomes of this research may be disseminated at appropriate national and international conferences and may be published in scientific journals for wider reading. All data in presented in this way will be anonymised.',validators=[DataRequired()])
    consent7 = BooleanField('I agree to take part in this study.',validators=[DataRequired()])

    #date = DateField('Date',format="%m/%d%Y")

    initials = StringField('Initials: ',
                        validators=[DataRequired(),Length(min=1)])
    submit = SubmitField('Next Page')


class PersonalForm(FlaskForm):
    gender = SelectField('Please select your biological sex:',choices=[('Select','Select'),('Male', 'Male'), ('Female', 'Female')],
                        validators=[DataRequired()])
    age = IntegerField('Please state you age in years:',
                        validators=[validators.required()])
    education = SelectField('Please tick your highest level of education that you have received, below:',
    choices=[('Select','Select'),('1', 'Early childhood education(3 years and below)'), ('2', 'Primary education '), ('3', 'Secondary education or equivalent'), ('4', 'Bachelor’s degree or equivalent'), ('5', 'Master’s degree or equivalent'), ('6', 'Doctorate degree or equivalent')],
                        validators=[DataRequired()])
    country = StringField('Please state, your country of residence, below:',
                        validators=[DataRequired()])
    stay = IntegerField('How many years have you been residing in this country?',
                        validators=[DataRequired()])
    ethinicity = StringField('Please state your ethnicity?',
                        validators=[DataRequired()])
    job = StringField('Please state your current or most recent job occupation, below:',
                        validators=[DataRequired()])

    society = SelectField(' Do you have any history of substance abuse?',
    choices=[('Select','Select'),('Yes', 'Yes'), ('No', 'No')],
                        validators=[DataRequired()])

    submit = SubmitField('Next Page')

    def validate_gender(self, gender):
        if gender.data=="Select":
            raise ValidationError('Select your gender.')

    def validate_education(self, education):
        if education.data=="Select":
            raise ValidationError('Select your education.')

    def validate_society(self, society):
        if society.data=="Select":
            raise ValidationError('Select your history.')

class QuestionnaireForm(FlaskForm):
    radio = RadioField('Please tick your highest level of education that you have received, below:',
    choices=[('Select','Select'),('1', 'Early childhood education(3 years and below)'), ('2', 'Primary education '), ('3', 'Secondary education or equivalent'), ('4', 'Bachelor’s degree or equivalent'), ('5', 'Master’s degree or equivalent'), ('6', 'Doctorate degree or equivalent')]
    )
