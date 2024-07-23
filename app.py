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
        func.count(Ventas.id).label('sales_count')
    ).filter(Ventas.createdAt >= two_weeks_ago).group_by('day_of_week').all()

    total_sales = sum([sales.sales_count for sales in sales_by_day])
    probabilities = {sales.day_of_week: sales.sales_count / total_sales for sales in sales_by_day}

    return jsonify({"sales_probabilities": probabilities})

if __name__ == '__main__':
    app.run(debug=True)
