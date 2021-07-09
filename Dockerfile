FROM python:3 as base

WORKDIR /data
COPY ./poetry.toml /data
COPY ./pyproject.toml /data
RUN pip install poetry && poetry install

FROM base as production
RUN apt-get update && \
    apt-get install -y gunicorn
COPY ./todo_app /data/todo_app
EXPOSE 5000
ENTRYPOINT $(poetry env info --path)/bin/gunicorn --error-logfile /data/error.log -b 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development
EXPOSE 5000
ENTRYPOINT  poetry run flask run --host 0.0.0.0

FROM base as test
RUN poetry install && apt-get update && apt-get install wget gnupg unzip -y
COPY ./todo_app /data/todo_app
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# Install Chrome WebDriver
RUN apt-get update && apt-get install unzip -y
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
  && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && cp /opt/selenium/chromedriver . \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver
ENV PATH=$PATH:/data
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "pytest"]