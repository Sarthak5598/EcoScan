# ECOSCAN

## Overview
ECOSCAN is a Django-based web application aimed at promoting sustainability through voucher redemptions, image processing powered by OpenAI Vision, and fostering eco-friendly collaborations. Hosted on [PythonAnywhere]([(https://rakrsa.pythonanywhere.com]), the platform integrates modern frontend and backend technologies to deliver an engaging user experience.

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

1. **Enhancing OpenAI Integration**:
   - Train a custom OpenAI model to ensure consistent and precise responses tailored to the platform's requirements.

2. **Expanding Employee Functionality**:
   - Add more tools and features to streamline the employee experience and improve operational efficiency.

3. **Collaborations with Reewild**:
   - **Integration Idea**:
     - Reewild focuses on food sustainability. By collaborating, ECOSCAN can offer food discounts in exchange for clothes donations.
   - **Streamlining Deliveries**:
     - Combine the process of clothes donation and food delivery into a single eco-friendly trip to reduce logistics costs and carbon footprints.

---

We look forward to enhancing ECOSCAN and making sustainability more accessible and rewarding for everyone! 🌿
