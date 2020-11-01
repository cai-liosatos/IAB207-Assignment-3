from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields.html5 import DateField


#add the types of files allowed as a set
ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    phone_number=StringField("Phone Number:", validators=[InputRequired()])
    address=StringField("Address:", validators=[InputRequired()])
    #submit button
    submit = SubmitField("Register")

class ItemForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    # adding two validators, one to ensure input is entered and other to check if the 
    #description meets the length requirements

    category = SelectField('Category:', choices=[('CPU', 'CPU'), ('GPU','GPU'), ('Motherboard','Motherboard'), ('RAM','RAM'), ('Power Supply Unit','Power Supply Unit'), ('Cooling Fan','Cooling Fan')], validators=[InputRequired()])
    manufacturer = StringField('Manufacturer', validators=[InputRequired()])
    condition = SelectField('Condition:', choices=[('Brand New', 'Brand New'), ('Used', 'Used')], validators=[InputRequired()])
    #create a filefield that takes two validators - File required and File Allowed
    image = FileField('Image:', validators=[FileRequired(message='Image can not be empty'),
                                            FileAllowed(ALLOWED_FILE, message='Only support png, jpg, JPG, PNG, bmp')])
    finishdate =  DateField('Finish Date:', format='%Y-%m-%d', validators=[InputRequired()])
    postagedate = DateField('Estimated Delivery Time:', format='%Y-%m-%d', validators=[InputRequired()])
    startingprice = StringField('Starting Price:', validators=[InputRequired()])
    postageprice = StringField('Postage Price:', validators=[InputRequired()])
    currency = StringField('Currency ($)', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    submit = SubmitField("Submit")