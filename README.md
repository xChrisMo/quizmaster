# QuizMaster - Modern Trivia Application

A full-stack trivia quiz application built with Flask backend and React frontend, featuring a modern minimalist design.

## 🚀 Features

- **Modern UI**: Clean, minimalist design with gradient backgrounds and smooth animations
- **Quiz Functionality**: Interactive trivia quizzes with multiple categories
- **Question Management**: Add, edit, and delete questions through the web interface
- **Category Filtering**: Browse questions by different categories
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

### Backend
- **Flask**: Python web framework
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing
- **Gunicorn**: Production WSGI server

### Frontend
- **React**: JavaScript library for building user interfaces
- **CSS3**: Modern styling with gradients and animations
- **Fetch API**: For backend communication

## 📁 Project Structure

```
├── backend/
│   ├── flaskr/
│   │   └── __init__.py          # Flask app initialization
│   ├── models.py                # Database models
│   ├── requirements.txt         # Python dependencies
│   └── test_flaskr.py          # Backend tests
├── frontend/
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/          # React components
│   │   └── stylesheets/         # CSS files
│   └── package.json            # Node.js dependencies
├── Procfile                    # Heroku deployment configuration
└── setup-trivia.sh            # Database setup script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd quizmaster-app
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   # Start PostgreSQL service
   brew services start postgresql@14
   
   # Run the setup script
   ./setup-trivia.sh
   ```

4. **Start the backend server**
   ```bash
   export FLASK_APP=flaskr
   export FLASK_ENV=development
   flask run
   ```

5. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   export NODE_OPTIONS="--openssl-legacy-provider"
   npm start
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🌐 Deployment

### Heroku Deployment

1. **Create Heroku app**
   ```bash
   heroku create your-quizmaster-app
   ```

2. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Initialize database**
   ```bash
   heroku run "python -c 'from backend.models import setup_db; from backend.flaskr import create_app; app = create_app(); app.app_context().push(); setup_db(app)'"
   ```

## 📊 API Endpoints

- `GET /categories` - Get all categories
- `GET /questions` - Get paginated questions
- `GET /categories/{id}/questions` - Get questions by category
- `POST /questions` - Create a new question
- `DELETE /questions/{id}` - Delete a question
- `POST /quizzes` - Start a new quiz

## 🎨 Design Features

- **Gradient Backgrounds**: Modern color schemes
- **Card-based Layout**: Clean question and category displays
- **Smooth Animations**: Hover effects and transitions
- **Responsive Grid**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable fonts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Flask documentation and community
- React documentation and ecosystem
- Modern CSS techniques and best practices
