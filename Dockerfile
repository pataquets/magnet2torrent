FROM python:3

WORKDIR /usr/src/app/

# Install dependencies
COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r ./requirements.txt

# Build and install app
COPY . /usr/src/app/
RUN python ./setup.py install

ENTRYPOINT [ "magnet2torrent" ]
