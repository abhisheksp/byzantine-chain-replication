FROM python:3
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN apt-get -qq update
RUN apt-get install net-tools
EXPOSE 9002
ENV PORT=9002

# find a better way
CMD ["./run_replica.sh"]

