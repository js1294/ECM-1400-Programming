import pylint.lint

pylint_opts = ["covid_api.py", "weather_api.py", "news_api.py", "controlled_assessment3.py"]
pylint.lint.Run(pylint_opts)
