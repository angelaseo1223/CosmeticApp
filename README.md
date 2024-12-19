# Personalized Beauty Product Recommendation System


This application aimed to allow users to find beauty products according to their skin type, price-range, any special needs. The system provides personalized product recommendations, ingredient safety and effectiveness scores, exclusive product discovery, shopping bag functionality and a beauty routine tracker.

Dataset: 💄 Top Beauty & Cosmetics Products Worldwide 2024  https://www.kaggle.com/datasets/waqi786/most-used-beauty-cosmetics-products-in-the-world


## Steps to Run the Code:

### 1. Prepare All Files
Make sure all project files are in one folder, including `main.py`, `templates`, `static`, and any necessary CSV files containing product data.

### 2. Install Dependencies
To install the required dependencies, create a virtual environment and install the necessary libraries.

1. **Create a virtual environment** (optional, but recommended):
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   Use the `requirements.txt` file (or manually install the dependencies listed below):
   ```bash
   pip install -r requirements.txt
   ```
   Or, you can install the required dependencies directly:
   ```bash
   pip install Flask pandas tkcalendar
   ```

### 3. Run the Application
To start the program, run `main.py`:

```bash
python main.py
```

when the app is running it will be connect with  the provided URL (usually `http://127.0.0.1:5000/` for local Flask development) to access the app.

### 4. Interacting with the Features

1. **Personalized Recommendations**:
   - Choose your skin type, budget range, and product category.
   - Click "Get Recommendations" to see personalized beauty products based on your inputs.

2. **Ingredient Safety and Effectiveness Scores**:
   - Choose a main ingredient to check its safety and effectiveness score.
   - View the recommended products that include the selected ingredient.

3. **Exclusive Product Discovery**:
   - Filter products by country of origin and packaging type.
   - Check unique products that may not be found through traditional searches.

4. **Shopping Bag**:
   - Select products you want to purchase and add them to your shopping bag.
   - View your total spending and manage your selections.
   - The shopping bag saves user selections even if the page is refreshed.

5. **Beauty Routine Tracker**:
   - Input your skin type and budget.
   - Get personalized recommendations for each step of your beauty routine, including cleansers, serums, moisturizers, and sunscreens.

## Dependencies:

- `Flask` (for backend framework)
- `pandas` (for handling product data)
- `tkcalendar` (for date selection in forms)

To install the dependencies, run:
```bash
pip install Flask pandas tkcalendar
```

### Additional Information:
- Python version: 3.10.5 (use a virtual environment for best practices)
- Make sure you have the `cosmetics.csv` file containing the product data for the app to work properly.

---

