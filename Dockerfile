FROM abhisheksp/distalgo:pynacl-docker
WORKDIR /app
ADD . /app
EXPOSE 9002
ENV PORT=9002
ENV LOG_FILE_PATH='/app/logs/replica.log'
ENV LOG_LEVEL='info'
# find a better way
CMD ["./run_replica.sh"]

