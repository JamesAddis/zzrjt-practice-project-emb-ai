
# build requirements
ARG BUILD_TAG="3.11-slim"
ARG RUNNER_TAG="3.11-slim"
ARG PUID="1000"
ARG PGID="1000"

FROM python:${BUILD_TAG} AS build

# setup permissions for folders (so they can be copied to scratch)
RUN mkdir /etc/practice-project
RUN mkdir /etc/practice-project/config.d
RUN mkdir /etc/practice-project/secrets.d
RUN mkdir -p /var/log/practice-project
RUN useradd -u $PUID -g $PGID practice-project
RUN chmod 640 /etc/practice-project
RUN chmod 640 /etc/practice-project/config.d
RUN chmod 640 /etc/practice-project/secrets.d
RUN chmod 660 /var/log/practice-project
RUN chown root:practice-project /etc/practice-project
RUN chown root:practice-project /var/log/practice-project

# install
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --upgrade pyinstaller

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy and Compile app as a separate step: Only re-execute this step when source code changed
FROM build-venv AS build-app
COPY . /src
WORKDIR /src
RUN /venv/bin/pyinstaller --onefile --name "app" main.py
# update
RUN chmod 750 dist/*.exe
RUN chown root:practice-project  dist/*.exe
COPY /src/src/config.default /etc/practice-project/config
COPY /src/src/config.default.d/* /etc/practice-project/config.d/
RUN chmod 640 /etc/practice-project/config
RUN chown root:practice-project /etc/practice-project/config
RUN chown root:practice-project /etc/practice-project/config.d/*

# Copy the app into a distroless image
FROM scratch
# copy configuration/logs structure with permissions already set
COPY --from=build-app /etc/practice-project/config /etc/practice-project/config
COPY --from=build-app /etc/practice-project/config.d /etc/practice-project/config.d
COPY --from=build-app /etc/practice-project/secrets.d /etc/practice-project/secrets.d
COPY --from=build-app /var/log/practice-project /var/log/practice-project
COPY --from=build-app /src/dist/app.exe /usr/share/practice-project
USER $PUID:$PGID
ENTRYPOINT ["/usr/share/practice-project"]


