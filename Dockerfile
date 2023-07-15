FROM python

COPY . .

RUN pip install -t requirements.txt

