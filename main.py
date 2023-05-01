from flask import Flask, request, render_template
import random
import string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def essa():
    if request.method == 'POST':
        try:
            min_length = int(request.form.get('min_length'))
        except ValueError:
            error = 'Please enter the length of your password first!'
            return render_template('index.html', error=error)
        has_numbers = True if request.form.getlist('digits') else False
        has_specials = True if request.form.getlist('specials') else False
        to_file = True if request.form.getlist('saving') else False
        file_name = str(request.form.get('file_name'))
        password = password_generator(min_length, file_name, to_file, has_numbers, has_specials)
        return render_template('result.html', password=password)
    else:
        return render_template('index.html')

def password_generator(min_length, file_name, to_file, numbers=True, special_chars=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    available_characters = letters

    if numbers:
        available_characters += digits
    if special_chars:
        available_characters += special

    pwd = ""
    meets_criteria = False
    has_digit = False
    has_special = False

    while not meets_criteria or len(pwd) < min_length:
        chosen = random.choice(available_characters)
        pwd += chosen

        if chosen in digits:
            has_digit = True
        if chosen in special:
            has_special = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_digit
        elif special_chars:
            meets_criteria = meets_criteria and has_special

    if to_file:
        with open(f'{file_name}', 'a') as f:
            f.write(f'Generated password: {pwd} \n')

    return pwd


if __name__ == '__main__':
    app.run(debug=True)