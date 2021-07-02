FROM python:3.9

# Update the package list and install chrome
# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

ENV CHROMEDRIVER_VERSION 90.0.4430.24
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# RUN apt-get install -y google-chrome-stable=${CHROMEDRIVER_VERSION}-1

# Set up Chromedriver Environment variables


# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH
# update config to not run as root
# RUN sed -i 's|exec -a "$0" "$HERE/chrome" "$@"|exec -a "$0" "$HERE/chrome" "$@" --no-sandbox --user-data-dir |g' /opt/google/chrome/google-chrome

COPY requirements.txt /app/
RUN pip3 --default-timeout=600 install -r /app/requirements.txt

EXPOSE 22
EXPOSE 5000/tcp

ENV PORT 5000

COPY app.py /app/
COPY logger.py /app/
ADD pints /app/pints
ADD metrics /app/metrics
ADD static /app/static
ADD dbt /app/dbt

CMD cd app && exec gunicorn -t 900 --bind :$PORT --workers $WORKERS --threads 1 --preload app:app