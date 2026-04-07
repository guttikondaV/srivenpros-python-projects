# Weather App

This module contains the weather app. It fetches data from Open Weather API and
uses `.env`
files to store API Keys and other security info.

It then uses Rich to display data in a formatted table.

Also written are the test for the program in the `test_weather.py` file. It uses
`pytest` as a test runner and `unittest` for mocking and assertions