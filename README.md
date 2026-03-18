

# 🚀 DailyDiet Challenge

**A modern RESTful API for meal tracking, built with Flask and SQLite. Designed for clarity, scalability, and best practices.**

---

## ✨ Highlights
- Clean and modular codebase
- Automated tests for all main features (pytest)
- Follows RESTful principles
- Easy to extend for new features or database engines
- Ready for deployment and CI/CD integration

## 📋 Features
- Create, list, update, and delete meals
- Filter meals by date and by diet status (in/out of diet)
- Validation for required fields and data formats
- Error handling with clear messages

## 🛠️ Technologies Used
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite (default, easily switchable to MySQL/PostgreSQL)
- pytest (for automated testing)

## 🚀 Getting Started
1. **Clone the repository:**
	```bash
	git clone <repo-url>
	cd dailyDiet_challenge
	```
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Create the database:**
	```bash
	python create._db.py
	```
4. **Run the application:**
	```bash
	python app.py
	```

## 🧪 Running Tests
- All main API routes and model methods are covered by automated tests.
- To run the tests:
	```bash
	pytest test_app.py
	```

## 📚 API Endpoints

### Create meal
`POST /meals`
Body JSON:
```json
{
  "name": "Lunch",
  "description": "Rice and beans",
  "date_time": "dd/mm/yyyy HH:MM",
  "in_diet": true
}
```

### List meals
`GET /meals`

### Get meal by ID
`GET /meals/<id>`

### Update meal
`PUT /meals/<id>`
Body JSON:
```json
{
  "name": "Updated Lunch",
  "description": "Salad",
  "in_diet": false
}
```

### Delete meal
`DELETE /meals/<id>`

### Get meals by date
`GET /meals/date/<dd-mm-yyyy>`

### Get meals by diet status
`GET /meals/diet/<true|false>`

## 🏆 Best Practices
- Modular structure (models, utils, config, routes)
- Consistent error handling and validation
- Test coverage for all main flows
- Easy to add authentication, migrations, or new endpoints

## 💡 How to Extend
- Add authentication (JWT, OAuth)
- Integrate with Flask-Migrate for database migrations
- Switch to MySQL/PostgreSQL by updating `config.py`
- Add new endpoints or business rules as needed

## 📦 Deployment
- Ready for Dockerization and cloud deployment
- Can be integrated with CI/CD pipelines for automated testing

## 👨‍💻 About the Author
- Developed for Rocketseat Python Module 4 Challenge
- Open to feedback and collaboration

---

