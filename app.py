from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import joblib
import re
import random
from collections import defaultdict

app = Flask(__name__)
CORS(app)

df = pd.read_csv("Food.csv")
model = joblib.load("nutrition_predictor.pkl")

df['Food_Encoded'] = df['Food'].factorize()[0]
df['Cuisine_Encoded'] = df['Cuisine'].factorize()[0]
df['Category_Encoded'] = df['Category'].factorize()[0]

food_dict = {food.lower(): idx for idx, food in enumerate(df['Food'].unique())}

def predict_and_recommend(text):
  
    text = text.lower()
    food_qty = defaultdict(int)

    for food in df['Food'].str.lower():
        pattern = r'(\d+)?\s*' + re.escape(food)
        match = re.search(pattern, text)
        if match:
            qty = int(match.group(1)) if match.group(1) else 1
            food_qty[food] += qty

    if not food_qty:
        return None

    total_cal = total_pro = total_carbs = total_fat = 0
    recommendations = []

    for food, qty in food_qty.items():
        food_row = df[df['Food'].str.lower() == food].iloc[0]
        food_enc = food_row['Food_Encoded']
        cuisine_enc = food_row['Cuisine_Encoded']
        category_enc = food_row['Category_Encoded']

        X_input = pd.DataFrame(
            [[food_enc, cuisine_enc, category_enc]],
            columns=['Food_Encoded', 'Cuisine_Encoded', 'Category_Encoded']
        )
        pred = model.predict(X_input)[0]

        total_cal += pred[0] * qty
        total_pro += pred[1] * qty
        total_carbs += pred[2] * qty
        total_fat += pred[3] * qty

        # Alternatives (same cuisine & category)
        alternatives_list = df[
            (df['Cuisine_Encoded'] == cuisine_enc) &
            (df['Category_Encoded'] == category_enc) &
            (~df['Food'].str.lower().isin(food_qty.keys()))
        ]['Food'].tolist()
        random.shuffle(alternatives_list)
        alternatives = alternatives_list[:3]

        # Low-calorie foods
        low_cal_list = df[
            (df['Calories'] < food_row['Calories']) &
            (~df['Food'].str.lower().isin(food_qty.keys()))
        ]['Food'].tolist()
        random.shuffle(low_cal_list)
        low_cal = low_cal_list[:3]

        # High-protein foods
        high_pro_list = df[
            (df['Protein'] > food_row['Protein']) &
            (~df['Food'].str.lower().isin(food_qty.keys()))
        ]['Food'].tolist()
        random.shuffle(high_pro_list)
        high_pro = high_pro_list[:3]

        # Healthy additions (also include in your diet)
        fruits = df[
            (df['Category'] == 'Fruit') &
            (~df['Food'].str.lower().isin(food_qty.keys()))
        ]['Food'].tolist()
        juices = df[
            (df['Category'] == 'Juice') &
            (~df['Food'].str.lower().isin(food_qty.keys()))
        ]['Food'].tolist()
        snacks = df[
            (df['Category'] == 'Snack') &
            (~df['Food'].str.lower().isin(food_qty.keys()))
        ]['Food'].tolist()

        additions = []
        if fruits:
            additions.append(random.choice(fruits))
        if juices:
            additions.append(random.choice(juices))
        if snacks:
            additions.append(random.choice(snacks))

        recommendations.append({
            "food": food,
            "alternatives": alternatives,
            "low_calorie": low_cal,
            "high_protein": high_pro,
            "additions": additions  # <-- added here
        })

    nutrition_dict = {
        'foods': list(food_qty.keys()),
        'Calories': round(total_cal, 2),
        'Protein': round(total_pro, 2),
        'Carbs': round(total_carbs, 2),
        'Fat': round(total_fat, 2)
    }

    return {
        "nutrition": nutrition_dict,
        "recommendations": recommendations
    }


# -------------------------
# API Endpoint (POST)
# -------------------------
@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    result = predict_and_recommend(text)
    if not result:
        return jsonify({"error": "Food not recognized"}), 400
    return jsonify(result)

# -------------------------
# FRONTEND ROUTES (GET)
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/analyze")
def analyze_page():
    return render_template("analyze.html")

@app.route("/nutrients")
def nutrients_page():
    return render_template("nutrients.html")

@app.route("/tips")
def tips_page():
    return render_template("tips.html")

@app.route("/recipes")
def recipes_page():
    return render_template("recipes.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/api/recipes", methods=["GET"])
def recipes():
    query = request.args.get("q", "").lower()

    recipe_data = {
        "oats": ["Oats Banana Smoothie", "Overnight Oats", "Oats Upma"],
        "banana": ["Banana Pancakes", "Banana Smoothie Bowl"],
        "salad": ["Greek Salad", "Protein-Rich Veggie Salad"],
        "chicken": ["Grilled Chicken Salad", "Chicken Soup"],
        "juice": ["Detox Green Juice", "Carrot Beet Juice"]
    }

    matching = []
    for key, value in recipe_data.items():
        if query in key:
            matching.extend(value)

    if not matching:
        return jsonify({"recipes": []})

    return jsonify({"recipes": matching})

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
