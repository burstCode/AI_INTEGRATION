from flask import Flask, render_template, request, redirect, url_for

import config
from models.medical_ticket import MedicalTicket
from database.database_manager import DatabaseManager
from assistants.medical_assistent import MedicalAssistant
from bot import Bot

app = Flask(__name__)
db_manager = DatabaseManager()
bot = Bot(
    config.ENDPOINT,
    config.GITHUB_TOKEN,
    config.MODEL_NAME
)
assistant = MedicalAssistant(bot, db_manager)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        registration_result = assistant.create_ticket(symptoms)
        if registration_result == 0:
            return redirect(url_for('tickets_list'))
        else:
            pass

    return render_template('index.html')

@app.route('/tickets_list')
def tickets_list():
    tickets = db_manager.get_tickets_sorted()
    return render_template('tickets_list.html', tickets_list=tickets)

@app.route('/update_status/<int:medical_ticket_id>', methods=['POST'])
def update_status(medical_ticket_id):
    new_status = request.form['status']
    db_manager.update_ticket_status(medical_ticket_id, new_status)
    return redirect(url_for('tickets_list'))

if __name__ == '__main__':
    app.run(debug=True)
