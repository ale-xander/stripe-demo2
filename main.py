import stripe
import json
import logging
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
stripe.api_key = 'sk_test_vO7qaz9UCmO38BXJI1YO6mdF00HTTSrn1R'


@app.route('/')
def index():
    app.logger.info('index route')
    return render_template('index.html')

# Stripe checkout route
@app.route('/checkout', methods=['POST'])
def checkout():
    app.logger.info('checkout route')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'amount': 9999,
            'name': 'Severely overpriced backpack',
            'images': ['https://res.cloudinary.com/ale-xander/image/upload/c_scale,w_250/v1581716138/stripe/yellow_qsko2a.png'],
            'currency': 'USD',
            'quantity': 1
        }],
        success_url='http://localhost:5000/success?id={CHECKOUT_SESSION_ID}',
        cancel_url='http://localhost:5000/cancel',
    )
    return jsonify(session)

# route for the pmt confirmation
@app.route('/success')
def success():
    return render_template('success.html')

# route for le fail
@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

# route for retrieving the session
@app.route('/retrieve-session')
def retrieve_session():
    session = stripe.checkout.Session.retrieve(
        request.args['id'],
        expand=['payment_intent'],
    )
    return jsonify(session)


if __name__ == '__main__':
    app.run( port=5000)
