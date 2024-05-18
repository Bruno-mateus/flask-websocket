from flask import Flask, jsonify,request,send_file, render_template
from repository.database import db
from models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234'

db.init_app(app)

@app.route("/payments/pix", methods=["POST"])
def paymentMethod():
    data = request.get_json();
    if 'value' not in data :
        return jsonify({"message":"Invalid value"})
    
    expiration_date = datetime.now() + timedelta(minutes=30)
    payment = Payment()
    payment.value = data['value']
    payment.expiration_date = expiration_date
    
    ## create pix with qr code
    pix = Pix()
    pix_created = pix.create_payment()
    
    payment.bank_payment_id = pix_created["bank_payment_id"]
    payment.qr_code = pix_created["qr_code_path"]
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify({"message":"The payment has benn created","payment":payment.to_dict()})

@app.route('/payments/pix/qrcode/<filename>', methods=['GET'])
def get_qr_code_img(filename):
    return send_file(f'./static/img/{filename}.png',mimetype='image/png')

@app.route("/payments/pix/confirmation", methods=["POST"])
def pix_confirmation():
    return jsonify({"message":"The payment has confirmed"})

@app.route("/payments/pix/<int:payment_id>", methods=['GET'])
def payment_pix_page(payment_id):
    ##recebendo o pagamento solicitado
    payment= Payment.query.get(payment_id)
    return render_template('payment.html',id=payment.id, value=payment.value,qrcode= payment.qr_code,host="http://127.0.0.1:5000")


if __name__ == '__main__':
    app.run(debug=True)