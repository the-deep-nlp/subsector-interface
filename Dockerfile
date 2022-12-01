FROM python:3.8-slim-buster

COPY requirements.txt app/
WORKDIR app/
RUN apt-get update && \
    apt-get -y install make && \
    apt-get -y install gcc && \
    apt-get -y install g++ && \
    apt-get -y install git && \
    apt-get -y install python3-pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . .
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]

#Streamlit parameters
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

