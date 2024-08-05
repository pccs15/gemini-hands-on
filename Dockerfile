FROM python:3.12.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

WORKDIR /app

COPY ./ /app/
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py"]
