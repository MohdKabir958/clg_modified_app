from flask import Flask,Blueprint, render_template,request
from flask_login import login_required,current_user

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/account')
@login_required
def account():
    return render_template('account.html',user=current_user)


@main.route('/backend', methods=['GET','POST'])
def on_go():
    if request.method == 'POST':
        pdb_code = request.form.get('pdb_file[name]')
        # Process the pdb_code as needed
        return render_template('index.html')  # Example response

    return render_template('index.html')
