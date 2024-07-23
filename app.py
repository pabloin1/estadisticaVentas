from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, Ventas
from sqlalchemy import func
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

app.config.from_object(Config)
db.init_app(app)

@app.route('/sales/weekly', methods=['GET'])
def get_weekly_sales():
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    weekly_sales = db.session.query(func.count(Ventas.id)).filter(Ventas.createdAt >= week_ago).scalar()
    return jsonify({"weekly_sales": weekly_sales})

@app.route('/sales/probability', methods=['GET'])
def get_sales_probability():
    today = datetime.today()
    two_weeks_ago = today - timedelta(days=14)
    
    # Get sales grouped by day
    sales_by_day = db.session.query(
        func.dayofweek(Ventas.createdAt).label('day_of_week'),
        func.sum(Ventas.precio_Fn).label('total_sales')
    ).filter(Ventas.createdAt >= two_weeks_ago).group_by('day_of_week').all()

    # Initialize probabilities for all days of the week
    probabilities = {i: 0 for i in range(1, 8)}

    # Add weight to Monday (which is day 2 in DAYOFWEEK)
    weight_factor = 2  # Adjust this factor to increase or decrease the effect on Monday
    total_sales = sum([sales.total_sales for sales in sales_by_day])
    
    if total_sales > 0:
        # Populate probabilities with actual sales data
        for sales in sales_by_day:
            if sales.day_of_week == 2:  # Monday
                probabilities[sales.day_of_week] = (sales.total_sales * weight_factor) / total_sales
            else:
                probabilities[sales.day_of_week] = sales.total_sales / total_sales

        # Normalize the probabilities to ensure they sum up to 1
        total_probability = sum(probabilities.values())
        probabilities = {day: prob / total_probability for day, prob in probabilities.items()}

    return jsonify({"sales_probabilities": probabilities})


if __name__ == '__main__':
    app.run(debug=True)
