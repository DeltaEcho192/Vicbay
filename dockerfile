FROM python:3
RUN apt-get install sudo
WORKDIR /usr/scr/app
COPY chromedriver /usr/local/bin
RUN sudo apt-get install chromium-browser
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python","./vicbay.py" ]
