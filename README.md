# :beach_umbrella: Django Sandbox

## :dart: Overview

This project is a sandbox for learning and playing with Django.

## :white_check_mark: Prerequisites

- Docker
- Google OAuth Client Secrets file (`client_secrets.json`)

### Setting up Google OAuth Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
1. Create a new project or select an existing one
1. Go to Credentials &rarr; Create Credentials &rarr; OAuth Client ID
1. Configure the OAuth consent screen if not already done
1. Create a Web Application type credential with:
   - Authorized redirect URIs: `http://localhost:8080/google/oauth/callback`
1. Download the client secrets JSON file
1. Save it as `client_secrets.json` in the project root directory

## :zap: Getting Started

### :computer: Local Development Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Build and start the development environment:

   ```bash
   docker compose --profile dev up --build
   ```

   This will:
   - Build the Docker containers
   - Install all Python dependencies via Poetry
   - Start the Django development server

3. Access the application:

   - The Django application will be available at http://localhost:8080

### :magic_wand: Development Commands

- Start the development environment:

  ```bash
  docker compose --profile dev up --build
  ```

- Stop the development environment:

  ```bash
  docker compose --profile dev down
  ```

- View application logs:

  ```bash
  docker compose --profile dev logs -f
  ```

### :computer: API Usage

#### Get Google Calendar events:

  ```bash
  GOOGLE_ACCESS_TOKEN=<your_google_token> ./bin/get_calendar_events.sh
  ```

#### Get Access Token

> [!IMPORTANT]
> Make sure to generate an API key in the Settings page before proceeding.

```bash
curl -sX POST -H "Authorization: Token <your_api_key>" \
   http://localhost:8080/api/google/token/
```

## :dna: Project Structure

The project uses:

- Django 5.1.6
- Poetry 2.0.1 for dependency management
- Docker for containerization
