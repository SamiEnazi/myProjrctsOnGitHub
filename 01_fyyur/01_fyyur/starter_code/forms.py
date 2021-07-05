from datetime import datetime
import app
from flask.helpers import flash
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, BooleanField,SubmitField,SelectMultipleField ,IntegerField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError ,Length

class ShowForm(FlaskForm):
    artist_id = IntegerField(
        'artist_id',
        validators=[DataRequired()]
    )
    def validate_artist_id(self, artist_id):
        if app.db.session.query(app.Artist).filter_by(id=artist_id.data).first() is None:
            raise ValidationError('Artist does not exist!')
    venue_id = IntegerField(
        'venue_id',
        validators=[DataRequired()]
    )
    def validate_venue_id(self, venue_id):
        if app.db.session.query(app.Venue).filter_by(id=venue_id.data).first() is None:
            raise ValidationError('Venue does not exist!')
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.utcnow()
    )
    submit = SubmitField('submit')

class VenueForm(FlaskForm):
    
    choices_state=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone',validators=[DataRequired()]
    )
    def validate_phone(self, phone):
        state = request.form['state']
        phoneStr = phone.data
        validated = False
        for item in codes:
            for numbers in item['code']:
                if str(numbers) in phoneStr[3:6] and item['name'] == state:
                    validated = True
                    print('True')
        print(request.form['state'])
        if not validated: 
            raise ValidationError('Not validated Phone for state')

    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField (
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' ,default=False)

    seeking_description = StringField(
        'seeking_description'
    )
    submit = SubmitField('submit')



class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired()]
    )
    
    def validate_phone(self, phone):
        state = request.form['state']
        phoneStr = phone.data
        validated = False
        for item in codes:
            for numbers in item['code']:
                if str(numbers) in phoneStr[3:6] and item['name'] == state:
                    validated = True
                    print('True')
        print(request.form['state'])
        if not validated: 
            raise ValidationError('Not validated Phone for state')

    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField (
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[DataRequired(),URL()]
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' ,default=False)

    seeking_description = StringField(
            'seeking_description'
     )
    submit = SubmitField('submit')


codes = [
    {
        'name': 'AL',
        'code': [205, 251, 256, 334, 938]
    }
    ,
    {
        'name': 'AK',
        'code': [907]
    }
    ,
    {
        'name': 'AZ',
        'code': [480, 520, 602, 623, 928]
    }
    ,
    {
        'name': 'AR',
        'code': [479, 501, 870]
    }
    ,
    {
        'name': 'CA',
        'code': [209, 213, 279, 310, 323, 408, 415, 424, 442, 510, 530, 559, 562, 619, 626, 628, 650, 657, 661, 669,
                 707, 714, 747, 760, 805, 818, 820, 831, 858, 909, 916, 925, 949, 951]
    }
    ,
    {
        'name': 'CO',
        'code': [303, 719, 720, 970]
    }
    ,
    {
        'name': 'CT',
        'code': [203, 475, 860, 959]
    }
    ,
    {
        'name': 'DE',
        'code': [302]
    }
    ,
    {
        'name': 'DC',
        'code': [202]
    }
    ,
    {
        'name': 'FL',
        'code': [239, 305, 321, 352, 386, 407, 561, 727, 754, 772, 786, 813, 850, 863, 904, 941, 954]
    }
    ,
    {
        'name': 'GA',
        'code': [229, 404, 470, 478, 678, 706, 762, 770, 912]
    }
    ,
    {
        'name': 'HI',
        'code': [808]
    }
    ,
    {
        'name': 'ID',
        'code': [208, 986]
    }
    ,
    {
        'name': 'IL',
        'code': [217, 224, 309, 312, 331, 618, 630, 708, 773, 779, 815, 847, 872]
    }
    ,
    {
        'name': 'IN',
        'code': [219, 260, 317, 463, 574, 765, 812, 930]
    }
    ,
    {
        'name': 'IA',
        'code': [319, 515, 563, 641, 712]
    }
    ,
    {
        'name': 'KS',
        'code': [316, 620, 785, 913]
    }
    ,
    {
        'name': 'KY',
        'code': [270, 364, 502, 606, 859]
    }
    ,
    {
        'name': 'LA',
        'code': [225, 318, 337, 504, 985]
    }
    ,
    {
        'name': 'ME',
        'code': [207]
    }
    ,
    {
        'name': 'MT',
        'code': [406]
    }
    ,
    {
        'name': 'NE',
        'code': [308, 402, 531]
    }
    ,
    {
        'name': 'NV',
        'code': [702, 725, 775]
    }
    ,
    {
        'name': 'NH',
        'code': [603]
    }
    ,
    {
        'name': 'NJ',
        'code': [201, 551, 609, 640, 732, 848, 856, 862, 908, 973]
    }
    ,
    {
        'name': 'NM',
        'code': [505, 575]
    }
    ,
    {
        'name': 'NY',
        'code': [212, 315, 332, 347, 516, 518, 585, 607, 631, 646, 680, 716, 718, 838, 845, 914, 917, 929, 934]
    }
    ,
    {
        'name': 'NC',
        'code': [252, 336, 704, 743, 828, 910, 919, 980, 984]
    }
    ,
    {
        'name': 'ND',
        'code': [701]
    }
    ,
    {
        'name': 'OH',
        'code': [216, 220, 234, 330, 380, 419, 440, 513, 567, 614, 740, 937]
    }
    ,
    {
        'name': 'OK',
        'code': [405, 539, 580, 918]
    }
    ,
    {
        'name': 'OR',
        'code': [458, 503, 541, 971]
    }
    ,
    {
        'name': 'MD',
        'code': [240, 301, 410, 443, 667]
    }
    ,
    {
        'name': 'MA',
        'code': [339, 351, 413, 508, 617, 774, 781, 857, 978]
    }
    ,
    {
        'name': 'MI',
        'code': [231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 947, 989]
    }
    ,
    {
        'name': 'MN',
        'code': [218, 320, 507, 612, 651, 763, 952]
    }
    ,
    {
        'name': 'MS',
        'code': [228, 601, 662, 769]
    }
    ,
    {
        'name': 'MO',
        'code': [314, 417, 573, 636, 660, 816]
    }
    ,
    {
        'name': 'PA',
        'code': [215, 223, 267, 272, 412, 445, 484, 570, 610, 717, 724, 814, 878]
    }
    ,
    {
        'name': 'RI',
        'code': [401]
    }
    ,
    {
        'name': 'SC',
        'code': [803, 843, 854, 864]
    }
    ,
    {
        'name': 'SD',
        'code': [605]
    }
    ,
    {
        'name': 'TN',
        'code': [423, 615, 629, 731, 865, 901, 931]
    }
    ,
    {
        'name': 'TX',
        'code': [210, 214, 254, 281, 325, 346, 361, 409, 430, 432, 469, 512, 682, 713, 726, 737, 806, 817, 830, 832,
                 903, 915, 936, 940, 956, 972, 979]
    }
    ,
    {
        'name': 'UT',
        'code': [385, 435, 801]
    }
    ,
    {
        'name': 'VT',
        'code': [802]
    }
    ,
    {
        'name': 'VA',
        'code': [276, 434, 540, 571, 703, 757, 804]
    }
    ,
    {
        'name': 'WA',
        'code': [206, 253, 360, 425, 509, 564]
    }
    ,
    {
        'name': 'WV',
        'code': [304, 681]
    }
    ,
    {
        'name': 'WI',
        'code': [262, 414, 534, 608, 715, 920]
    }
    ,
    {
        'name': 'WY',
        'code': [307]
    }
]
