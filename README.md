# Mini Social Network (Dwitter)

A Django-based mini social networking platform inspired by Twitter. Users have profiles, can follow each other, and post short messages ("dweets") of up to 140 characters. The stack runs on PostgreSQL and is fully containerized with Docker Compose (a Redis service is also provisioned for future use).

## Features

- **Profiles:** every user automatically gets a profile when their account is created
- **Follow / unfollow:** asymmetric relationships (you can follow someone without them following you back)
- **Dweets:** short text posts, limited to 140 characters
- **Personal dashboard:** a feed showing dweets from the users you follow, plus a form to post your own
- **Profile pages:** each user's dweets, who they follow, and who follows them
- **Admin panel:** manage users, profiles, and dweets from Django admin
- **Bulma UI:** styled with the [Bulma](https://bulma.io/) CSS framework

## Tech Stack

| Component        | Technology                             |
| ---------------- | -------------------------------------- |
| Backend          | Django 6.1, Python 3.13                |
| Database         | PostgreSQL 18                          |
| Cache            | Redis (alpine), provisioned, not used yet |
| Frontend         | Django templates + Bulma 0.9.3 (CDN)   |
| Containerization | Docker & Docker Compose                |

## Project Structure

```
mini-social-network/
├── dwitter/                    # Main Django app
│   ├── migrations/             # Database migrations
│   ├── templates/
│   │   ├── base.html           # Base layout (Bulma)
│   │   └── dwitter/
│   │       ├── dashboard.html      # Feed + dweet form
│   │       ├── profile_list.html   # All users
│   │       └── profile.html        # Single profile, follow/unfollow
│   ├── admin.py                # Admin configuration
│   ├── forms.py                # DweetForm
│   ├── models.py               # Profile, Dweet
│   ├── urls.py                 # App routes
│   └── views.py                # dashboard, profile_list, profile
├── social/                     # Django project config (settings, root URLs)
├── Dockerfile
├── docker-compose.yml          # web + PostgreSQL + Redis
├── manage.py
└── requirements.txt
```

## Data Model

- **Profile**: one-to-one with Django's `User`. Has a many-to-many `follows` relation to other profiles (non-symmetrical; reverse name `followed_by`). A profile is created automatically via a `post_save` signal and follows itself by default, so your own dweets appear in your feed.
- **Dweet**: belongs to a `User`, with a `body` (max 140 characters) and a `created_at` timestamp.

## Routes

| URL                 | Name                 | Description                          |
| ------------------- | -------------------- | ------------------------------------ |
| `/`                 | `dwitter:dashboard`  | Your feed and the "new dweet" form   |
| `/profile_list/`    | `dwitter:profile_list` | All other users                    |
| `/profile/<id>`     | `dwitter:profile`    | A user's profile; follow / unfollow  |
| `/admin/`           | -                    | Django admin                         |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/anasyaghi9/mini-social-network.git
   cd mini-social-network
   ```

2. **Build and start the services**

   ```bash
   docker compose up --build
   ```

   The web container waits for PostgreSQL to pass its health check before starting.

3. **Apply database migrations** (in a second terminal)

   ```bash
   docker compose exec web python manage.py migrate
   ```

4. **Create a superuser**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. **Log in and start using the app**

   The app has no login page of its own yet, so sign in through the admin panel first:

   1. Open http://localhost:8000/admin/ and log in with your superuser.
   2. Create more users and dweets from the admin if you want sample data.
   3. Open http://localhost:8000/ to see your dashboard.

### Stopping the app

```bash
docker compose down        # stop containers
docker compose down -v     # stop containers and delete the database volume
```

## Services

| Service | Container         | Port | Description               |
| ------- | ----------------- | ---- | ------------------------- |
| `web`   | `social_django`   | 8000 | Django development server |
| `db`    | `social_postgres` | 5432 | PostgreSQL database       |
| `redis` | `social_redis`    | 6379 | Redis (not used yet)      |

## Configuration

Database settings are read from environment variables, defined in `docker-compose.yml`:

| Variable      | Default     | Description       |
| ------------- | ----------- | ----------------- |
| `DB_NAME`     | `social_db` | Database name     |
| `DB_USER`     | `postgres`  | Database user     |
| `DB_PASSWORD` | `postgres`  | Database password |
| `DB_HOST`     | `db`        | Database host     |
| `DB_PORT`     | `5432`      | Database port     |

> **Note:** The default credentials, `DEBUG = True`, and the `SECRET_KEY` in `settings.py` are for local development only. Move them to environment variables and change them before deploying anywhere public.

## Common Commands

```bash
# Create new migrations after changing models
docker compose exec web python manage.py makemigrations

# Open a Django shell
docker compose exec web python manage.py shell

# View logs
docker compose logs -f web
```

## Roadmap

- Login, logout, and registration pages
- Restrict views to authenticated users
- Automated tests
- Use Redis for caching (e.g. the feed)

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request

## License

No license has been specified yet. Add a `LICENSE` file (for example MIT) to define how others can use this project.

## Author

[@anasyaghi9](https://github.com/anasyaghi9)
