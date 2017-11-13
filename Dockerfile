FROM abhisheksp/distalgo:pynacl-docker
WORKDIR /app
ADD . /app
EXPOSE 9002
ENV PORT=9002

# find a better way
CMD ["./run_replica.sh"]

