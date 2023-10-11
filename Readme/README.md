# Open Source Classifieds Web and Mobile Application Backend

The Open Source Classifieds Web and Mobile Application Backend is a comprehensive backend solution built using Python, Django, Django Rest Framework (DRF), Poetry, Docker, Redis, and Celery. This project aims to provide a robust and scalable backend infrastructure for open-source classifieds web and mobile applications, enabling users to create, manage, and browse classified listings seamlessly.

## Features

- **User Management:** Secure user authentication and registration system.
- **Listing Management:** Create, edit, and delete classified listings with various attributes.
- **Search and Filtering:** Efficient search functionality with filters and sorting options.
- **Image Handling:** Upload, store, and manage images associated with listings.
- **Messaging:** Enable communication between users interested in listings.
- **Notifications:** Real-time notifications for actions related to listings.
- **Backend Scalability:** Utilize Redis and Celery for handling background tasks and improving performance.
- **API Documentation:** Well-documented API endpoints for seamless integration with web and mobile frontends.
- **Dockerization:** Easy deployment and scalability using Docker containers.
- **Version Management:** Dependency management and version specification using Poetry.

## Technologies Used

- Python
- Django
- Django Rest Framework (DRF)
- Poetry (Dependency Management)
- Docker (Containerization)
- Redis (Caching and Background Tasks)
- Celery (Asynchronous Task Queue)

## Instructions for Running the Project

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/murtazox04/kelishamiz-backend.git
   cd kelishamiz-backend

   ```

2. **Set Up Virtual Environment (Recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   ```

3. **Install Dependencies:**

   ```bash
   pip install poetry
   poetry install

   ```

4. **Environment Variables:**

   ```bash
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   REDIS_URL=redis://localhost:6379/0

   ```

5. **Run Migrations:**

   ```bash
   python manage.py migrate

   ```

6. **Start Celery Worker (in a separate terminal):**

   ```bash
   celery -A your_project_name worker -l info

   ```

7. **Run the Development Server:**

   ```bash
   python manage.py runserver

   ```

8. **Access API Documentation:**

   Visit http://127.0.0.1:8000/docs/ for the interactive API documentation provided by DRF.

## Running with Docker

If you prefer to use Docker for running the project, follow these steps:

1. **Build Docker Image:**

   ```bash
   docker build -t kelishamiz-backend .

   ```

2. **Run Docker Container:**

   ```bash
   docker run -p 8000:8000 --env-file .env kelishamiz-backend
   ```

# Contributing

We welcome contributions to enhance the functionality and features of the backend. Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

# License

This project is licensed under the [MIT License](LICENSE).

For detailed design architecture, please refer to the [Figma Design](<https://www.figma.com/file/X4ODCwpCZ117AUsrqpQ85f/E'lonlar-sayti-(Copy)?type=design&node-id=2%3A2&mode=design&t=GVNEei7KwNuTrEDI-1>).

For any questions or support, please contact us at murtazox04@gmail.com. We appreciate your interest in the project and look forward to your contributions!
