from flask import Flask, render_template, request, session, redirect
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'


try:
    df = pd.read_csv('cosmetics.csv')
    df.columns = df.columns.str.strip()  
except FileNotFoundError:
    print("Error: 'cosmetics.csv' file not found!")
    df = pd.DataFrame()  

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    skin_types = df['Skin_Type'].dropna().unique().tolist() if not df.empty else []
    categories = df['Category'].dropna().unique().tolist() if not df.empty else []

    products = []
    skin_type = budget_min = budget_max = category = None

    if request.method == 'POST':
        skin_type = request.form.get('skin_type', None)
        budget_min = request.form.get('budget_min', None)
        budget_max = request.form.get('budget_max', None)
        category = request.form.get('category', None)

        if budget_min:
            budget_min = float(budget_min)
        if budget_max:
            budget_max = float(budget_max)

        filtered_products = df[
            (df['Skin_Type'] == skin_type) &
            (df['Price_USD'] >= budget_min) &
            (df['Price_USD'] <= budget_max)
        ]
        if category:
            filtered_products = filtered_products[filtered_products['Category'] == category]

        filtered_products['Tag'] = ''
        filtered_products.loc[filtered_products['Rating'] >= 4.8, 'Tag'] = 'Top Rated '
        filtered_products.loc[filtered_products['Number_of_Reviews'] > 500, 'Tag'] += 'Best Seller '
        filtered_products.loc[filtered_products['Price_USD'] <= 30, 'Tag'] += 'Budget-Friendly'

        products = filtered_products.sort_values(
            by=['Rating', 'Number_of_Reviews'], 
            ascending=[False, False]
        ).head(5).to_dict(orient='records')

    return render_template(
        'recommendations.html',
        skin_types=skin_types,
        categories=categories,
        products=products,
        skin_type=skin_type,
        budget_min=budget_min,
        budget_max=budget_max,
        category=category
    )



@app.route('/ingredient_scores', methods=['GET', 'POST'])
def ingredient_scores():
    main_ingredients = df['Main_Ingredient'].dropna().unique().tolist() if not df.empty else []

    ingredient_effectiveness = {
        'Hyaluronic Acid': 95,
        'Vitamin C': 90,
        'Retinol': 88,
        'Salicylic Acid': 85,
        'Niacinamide': 87,
        'Aloe': 80,
        'Glycerin': 78,
        'Peptides': 92,
        'Ceramides': 89,
        'Green Tea': 83
    }

    selected_ingredient = None
    effectiveness_score = None
    safety_score = None
    products = []

    if request.method == 'POST':
        selected_ingredient = request.form.get('main_ingredient', None)
        effectiveness_score = ingredient_effectiveness.get(selected_ingredient, 70)  

        filtered_products = df[df['Main_Ingredient'] == selected_ingredient]

        if not filtered_products.empty:
            safety_score = filtered_products['Rating'].mean()

            products = filtered_products.sort_values(by='Rating', ascending=False).head(5).to_dict(orient='records')

    return render_template(
        'ingredient_scores.html',
        main_ingredients=main_ingredients,
        selected_ingredient=selected_ingredient,
        effectiveness_score=effectiveness_score,
        safety_score=safety_score,
        products=products
    )


@app.route('/exclusive_discovery', methods=['GET', 'POST'])
def exclusive_discovery():
    countries = df['Country_of_Origin'].dropna().unique().tolist() if not df.empty else []
    packaging_types = df['Packaging_Type'].dropna().unique().tolist() if not df.empty else []

    selected_country = None
    selected_packaging = None
    products = []

    if request.method == 'POST':
        selected_country = request.form.get('country', None)
        selected_packaging = request.form.get('packaging', None)

        filtered_products = df[
            (df['Country_of_Origin'] == selected_country) &
            (df['Packaging_Type'].str.contains(selected_packaging, case=False, na=False))
        ]

        products = filtered_products.sort_values(
            by='Rating', ascending=False
        ).head(5).to_dict(orient='records')

    return render_template(
        'exclusive_discovery.html',
        countries=countries,
        packaging_types=packaging_types,
        selected_country=selected_country,
        selected_packaging=selected_packaging,
        products=products
    )


@app.route('/routine_tracker', methods=['GET', 'POST'])
def routine_tracker():
    routine_steps = ['Cleanser', 'Toner', 'Serum', 'Moisturizer', 'Sunscreen']

    skin_types = df['Skin_Type'].dropna().unique().tolist() if not df.empty else []
    products_by_step = {}

    skin_type = budget_min = budget_max = None

    if request.method == 'POST':
        skin_type = request.form.get('skin_type', None)
        budget_min = float(request.form.get('budget_min', 0))
        budget_max = float(request.form.get('budget_max', 1000))

        for step in routine_steps:
            filtered_products = df[
                (df['Skin_Type'] == skin_type) &
                (df['Price_USD'] >= budget_min) &
                (df['Price_USD'] <= budget_max) &
                (df['Category'].str.contains(step, case=False, na=False))
            ]

            if not filtered_products.empty:
                top_product = filtered_products.sort_values(
                    by='Rating', ascending=False
                ).head(1).to_dict(orient='records')
                if top_product:
                    products_by_step[step] = top_product[0]

    return render_template(
        'routine_tracker.html',
        skin_types=skin_types,
        routine_steps=routine_steps,
        products_by_step=products_by_step,
        skin_type=skin_type,
        budget_min=budget_min,
        budget_max=budget_max
    )





@app.route('/shopping_bag', methods=['GET', 'POST'])
def shopping_bag():
    if 'shopping_bag' not in session:
        session['shopping_bag'] = []

    skin_types = df['Skin_Type'].dropna().unique().tolist()
    categories = df['Category'].dropna().unique().tolist()

    selected_skin_type = request.args.get('skin_type', None)
    selected_category = request.args.get('category', None)
    filtered_products = pd.DataFrame()

    if selected_skin_type or selected_category:
        filtered_products = df.copy()
        if selected_skin_type:
            filtered_products = filtered_products[filtered_products['Skin_Type'] == selected_skin_type]
        if selected_category:
            filtered_products = filtered_products[filtered_products['Category'] == selected_category]

    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = float(request.form['product_price'])
        session['shopping_bag'].append({'Product_Name': product_name, 'Price': product_price})
        session.modified = True

    total_cost = sum(item['Price'] for item in session['shopping_bag'])

    return render_template(
        'shopping_bag.html',
        skin_types=skin_types,
        categories=categories,
        selected_skin_type=selected_skin_type,
        selected_category=selected_category,
        filtered_products=filtered_products.to_dict(orient='records'),
        shopping_bag=session['shopping_bag'],
        total_cost=total_cost
    )

@app.route('/clear_shopping_bag')
def clear_shopping_bag():
    session['shopping_bag'] = []
    session.modified = True
    return redirect('/shopping_bag')

if __name__ == '__main__':
    app.run(debug=True)
