запускать докером:
``
docker build -t mtu_finder -f Dockerfile .
``
``
docker run --rm -p 80:80 -it mtu_finder
``
``
python3 main.py <name>
``