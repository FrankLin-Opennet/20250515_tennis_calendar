# Tennis Calendar Export Tool

This Python script automates the export of OpenNet tennis court bookings to a CSV file compatible with Google Calendar imports.

## Overview

The script fetches tennis court booking data from the SportDraw API for specified venues, members, and time periods, then converts it to a format that can be directly imported into Google Calendar.

## Features

- Retrieves court booking schedules from the SportDraw API
- Filters bookings by venue and member
- Converts 24-hour time format to 12-hour format for Google Calendar
- Exports data to CSV in Google Calendar import format

## Files

- [20250515_tennis_calendar.py](20250515_tennis_calendar.py): Main Python script that fetches data and exports to CSV
- [google_calendar_event.csv](google_calendar_event.csv): Output file containing calendar events in Google Calendar format

## Usage

1. Configure settings in the script:
   - `TEST_MODE`: Set to 1 for testing (limited data fetch)
   - `PLACE_DICT`: List of tennis venues
   - `YEAR_MONTH_LIST`: Time periods to fetch data for
   - `MEMBER_LIST`: Member information for filtering bookings

2. Run the script:
   ```bash
   python 20250515_tennis_calendar.py
   ```

3. Import the generated CSV file into Google Calendar

## Data Structure

The script organizes tennis bookings with these details:
- Subject: "OpenNet Tennis | [Venue] [Court] [Time] by [Member]"
- Date and time information
- Location: Tennis venue
- Description: Placeholder for additional information

## Requirements

- Python 3.x
- Pandas
- Requests