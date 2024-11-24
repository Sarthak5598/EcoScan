# ECOSCAN

## Overview
ECOSCAN is a Django-based web application aimed at promoting sustainability through voucher redemptions, image processing powered by OpenAI Vision, and fostering eco-friendly collaborations. Hosted on https://rakrsa.pythonanywhere.com , the platform integrates modern frontend and backend technologies to deliver an engaging user experience.

---

## How to Host Locally

Follow these steps to run the project locally on your machine:

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set Up Environment Using Poetry**:
   - Ensure you have Poetry installed. If not, install it from [Poetry's documentation](https://python-poetry.org/docs/).
   - Create a virtual environment and install dependencies:
     ```bash
     poetry install
     poetry shell
     ```

3. **Migrate Database Files**:
   - Apply migrations to set up the database:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

4. **Run the Server**:
   - Start the development server:
     ```bash
     python manage.py runserver
     ```
   - Access the application at `http://127.0.0.1:8000/`.

---

## Tech Stack

### Frontend:
- **Django Templates**: For dynamic HTML rendering.
- **Bootstrap**: Used to ensure responsive and aesthetically pleasing UI components.

### Backend:
- **Django**: Handles application logic, database interactions, and routing.

### Image Processing:
- **OpenAI Vision**: Provides advanced image recognition and processing capabilities.

### Hosting:
- **PythonAnywhere**: Reliable and efficient platform for deploying and hosting the application.

---

## Future Improvements

1. **OpenAI Model Training**:
   - Train an OpenAI model for more consistent and reliable responses.

2. **Employee-Side Features**:
   - Expand functionality to improve the employee experience and manage tasks efficiently.

3. **Collaboration with Ecoscan and Reewild**:
   - Integrate food discounts based on the number of clothes donated.
   - Enable single delivery for donations and food services to streamline processes.

4. **Backend Scalability**:
   - Scale the backend to handle larger user loads efficiently. This could involve optimizing database queries, using caching mechanisms, and considering distributed systems or cloud hosting solutions.

5. **Enhanced Carbon Scoring Model**:
   - Improve the carbon scoring model by incorporating more detailed data, such as the carbon footprint of donated items, transportation logistics, and the environmental impact of various donation types.

6. **Improved User Experience**:
   - Enhance the user experience by providing additional insights, such as sustainability comparisons between different donation actions, personalized recommendations, and progress tracking.

7. **External API Integration**:
   - Integrate the solution with external APIs to provide real-time data, such as live carbon footprint statistics, donation tracking, or food availability, further enhancing the app's relevance and user engagement.

---

We look forward to enhancing ECOSCAN and making sustainability more accessible and rewarding for everyone! 🌿
