from flask import Flask, render_template, request,redirect,url_for
from services.prediction import predict_price
from services.financial import calculate_noi, calculate_cap_rate, calculate_cashflow, calculate_roi, calculate_irr
from services.risk import monte_carlo_simulation, calculate_risk_score
from services.recommendation import generate_recommendation
from database import db, User, Analysis
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='templates')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route("/")
@login_required
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists!"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))

        return "Invalid Credentials"

    return render_template("login.html")

# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



@app.route("/analyze", methods=["POST"])
@login_required
def analyze():

    # =============================
    # GET USER INPUT
    # =============================

    bedrooms = int(request.form["bedrooms"])
    bathrooms = float(request.form["bathrooms"])
    sqft_living = int(request.form["sqft_living"])
    grade = int(request.form["grade"])
    condition = int(request.form["condition"])
    yr_built = int(request.form["yr_built"])
    lat = float(request.form["lat"])
    long = float(request.form["long"])
    year_sold = int(request.form["year_sold"])

    annual_rent = float(request.form["annual_rent"])
    annual_expenses = float(request.form["annual_expenses"])
    annual_loan_payment = float(request.form["annual_loan_payment"])
    years = int(request.form["years"])


    # =============================
    # PRICE PREDICTION
    # =============================

    property_data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "grade": grade,
        "condition": condition,
        "yr_built": yr_built,
        "lat": lat,
        "long": long,
        "year_sold": year_sold
    }

    predicted_price = predict_price(property_data)


    # =============================
    # FINANCIAL CALCULATIONS
    # =============================

    noi = calculate_noi(annual_rent, annual_expenses)
    cap_rate = calculate_cap_rate(noi, predicted_price)
    cashflow = calculate_cashflow(
        annual_rent,
        annual_expenses,
        annual_loan_payment
    )
    roi = calculate_roi(cashflow * years, predicted_price)
    irr = calculate_irr(predicted_price, cashflow, years)


    # =============================
    # RISK SIMULATION
    # =============================

    simulated = monte_carlo_simulation(roi / 100, 0.05)
    risk_result = calculate_risk_score(simulated)

    recommendation = generate_recommendation(
        roi,
        irr,
        risk_result["risk_level"]
    )


    # =============================
    # SAVE TO DATABASE
    # =============================

    new_analysis = Analysis(
        predicted_price=predicted_price,
        roi=roi,
        irr=irr,
        risk_level=risk_result["risk_level"],
        recommendation=recommendation,
        user_id=current_user.id
    )

    db.session.add(new_analysis)
    db.session.commit()


    # =============================
    # SHOW RESULT PAGE
    # =============================

    return render_template(
        "result.html",
        predicted_price=predicted_price,
        noi=noi,
        cap_rate=cap_rate,
        cashflow=cashflow,
        roi=roi,
        irr=irr,
        risk=risk_result,
        simulated_returns=simulated.tolist() if hasattr(simulated, "tolist") else simulated,
        recommendation=recommendation
    )
@app.route("/dashboard")
@login_required
def dashboard():

    user_analyses = Analysis.query.filter_by(user_id=current_user.id).all()

    return render_template("dashboard.html", analyses=user_analyses)
@app.route("/analysis-form")
@login_required
def analysis_form():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True,port=5001)