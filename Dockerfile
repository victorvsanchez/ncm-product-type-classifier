FROM python:3.7.10
ARG HOME="/home/dufry"
WORKDIR ${HOME}
COPY . ${HOME}
RUN chmod -R a+w ${HOME}
ENV GOOGLE_APPLICATION_CREDENTIALS="${HOME}/hvar-dufry-dev-46f2154886a2.json"
ENV SECRET=
ENV DUFRY_AUTHENTICATION_KEY=${SECRET}
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
RUN pip install --upgrade pip
RUN pip install -r ${HOME}/requirements.txt
CMD exec gunicorn --bind :${PORT} --workers 4 --threads 8 --timeout 0 main:app