# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

##
# 環境変数定義
##
# ENV HOST = "datareportsprojects:us-central1:kirinz-live-database"
ENV HOST="10.72.48.3"
ENV DB_USER="develop"
ENV DB_PASS=">ENdOi\cIXok}Gs3"
ENV DB_NAME="kirinz-ive-datas"

##
# ライブラリ系読み込み
##
RUN pip install --upgrade pip 
RUN pip install six
RUN pip install pandas
RUN pip install requests
RUN pip install --user poetry
RUN pip install packaging
RUN pip install --upgrade db_dtypes
RUN pip install pyarrow
RUN pip install numpy==1.22.4
RUN pip3 install cmake

###
# 日本のカレンダー判定用
###
RUN pip install jpholiday


###
# GCP関連環境構築
###
RUN pip install google-api-python-client
RUN pip install google-cloud-logging

###
# スプレッドシート用環境構築
###
RUN pip install gspread
RUN pip install google-auth google-auth-oauthlib google-auth-httplib2
RUN pip install oauth2client

###
# mysql実行用
###
RUN pip install mysql-connector-python

# cloudSQL用
#RUN pip install google-cloud-sql-connector

# cloud strage用環境構築 一旦不要
#RUN pip install google-cloud-storage
#RUN pip install requests pillow
#RUN mkdir csv

# bigquery関連
RUN pip install --upgrade google-cloud-bigquery

CMD pip list
CMD export -p

####
# Install production dependencies.
####
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

CMD python main.py
