# :lock: Django Sandbox

## :dart: Overview

This project is a sandbox for learning and playing with Django.

## :white_check_mark: Prerequisites

- Docker

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

## :dna: Project Structure

The project uses:

- Django 5.1.6
- Poetry 2.0.1 for dependency management
- Docker for containerization
