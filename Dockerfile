FROM ubuntu:latest
WORKDIR /app
RUN apt-get update && apt-get install -y python3.11 python3.11-dev && apt-get install -y python3-pip 
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#COPY . .
COPY llama.py \
     main.py\
     test_request.py\
    ./

#COPY dir1 dir2 ./
CMD ["uvicorn", "main:app", "--reload"]