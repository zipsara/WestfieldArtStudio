from flask import Flask, render_template, request
from wtforms import Form, StringField, IntegerField, SelectField, FieldList, FormField, validators
from wtforms.validators import ValidationError

app = Flask(__name__)

class CoachingHoursForm(Form):
    hours = IntegerField('Week', [validators.Optional(), validators.NumberRange(min=0, max=5, message='Hours must be between 0 and 5')])

from wtforms import HiddenField

class ArtistForm(Form):
    hidden_tag = HiddenField()
    artist_name = StringField('Artist Name', [validators.Length(min=1, max=100)])
    skill_level = SelectField('Skill Level', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    class_level = SelectField('Class Level', choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')])
    number_of_exhibitions = IntegerField('Number of Exhibitions', [validators.NumberRange(min=0)])
    coaching_hours = FieldList(FormField(CoachingHoursForm), min_entries=4, max_entries=4)

    def validate_number_of_exhibitions(form, field):
        if form.skill_level.data == 'beginner' and field.data > 0:
            raise ValidationError('Beginner level cannot enter exhibitions')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ArtistForm(request.form)
    if request.method == 'POST' and form.validate():
        artist_name = form.artist_name.data
        skill_level = form.skill_level.data
        class_level = form.class_level.data
        number_of_exhibitions = form.number_of_exhibitions.data
        coaching_hours = [int(h['hours']) if h['hours'] else 0 for h in form.coaching_hours.data]

        class_cost = 0
        if class_level == 'basic':
            class_cost = 5000
        elif class_level == 'standard':
            class_cost = 7500
        else:
            class_cost = 10000

        coaching_cost = 5000 * sum(coaching_hours)
        exhibition_cost = 10000 * number_of_exhibitions
        total_cost = class_cost + coaching_cost + exhibition_cost

        return render_template('results.html',
                               artist_name=artist_name,
                               skill_level=skill_level,
                               class_level=class_level,
                               number_of_exhibitions=number_of_exhibitions,
                               coaching_hours=coaching_hours,
                               class_cost=class_cost,
                               coaching_cost=coaching_cost,
                               exhibition_cost=exhibition_cost,
                               total_cost=total_cost)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
