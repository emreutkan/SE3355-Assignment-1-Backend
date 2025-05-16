

# SE3355 Assignment 1 Backend

This repository contains the backend implementation for the Group 1 News Portal project assigned in SE3355 course. This backend provides API endpoints that serve news items, currency exchange rates, and weather forecast data to support the frontend news portal application.

## Deployment

The application is deployed on Azure Web App Services at:

https://se3355a1b-dpd2gycrcegubjaz.polandcentral-01.azurewebsites.net/

### Swagger
API documentation is available via Swagger UI at `/swagger/` when the application is running.

https://se3355a1b-dpd2gycrcegubjaz.polandcentral-01.azurewebsites.net/swagger


## Project Overview

This backend application is built with Flask and provides three main API endpoints:
- News API: Provides news items for the slider component
- Finance API: Provides currency exchange rates for the finance menu
- Weather API: Provides 5-day weather forecast data

## Tech Stack

- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Documentation**: Swagger/Flasgger
- **CORS Handling**: Flask-CORS

## Project Structure

```
├── app.py                # Main application entry point
├── database/
│   ├── config.py         # Database configuration
│   └── database.py       # Database connection and initialization
├── models/
│   └── models.py         # SQLAlchemy models for News, Weather, and Currency
├── routes/
│   ├── finance.py        # Currency API endpoints
│   ├── news.py           # News API endpoints
│   └── weather.py        # Weather API endpoints
├── services/
│   └── weather_service.py # Service for fetching weather data
└── newsImages/           # Directory for storing news images
```

## API Endpoints

### News API

```
GET /api/news
```
Returns a list of news items with title, image URL, and link to the full article.

### Finance API

```
GET /api/currencies
```
Returns a list of currencies with name, code, value, change, and last updated timestamp.

### Weather API

```
GET /api/weather
```
Returns a 5-day weather forecast with date, high/low temperatures, condition, and icon.


## Database Initialization

The database is automatically initialized with sample data when the application starts. You don't need to run any additional commands to set up the database.



## Frontend Repository

The frontend part of this project is implemented separately. You can find the frontend repository at:
https://github.com/emreutkan/se3355-assignment-1
