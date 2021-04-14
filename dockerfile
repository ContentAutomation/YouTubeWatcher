FROM selenium/standalone-firefox
# Switch to root to install tor
USER root
# Update apt lists, install tor and remove apt caches afterwards
RUN apt-get -qq update \
    && apt-get -qq install tor \
    && rm -rf /var/lib/apt/lists/*
# Copy the supervisor config for starting tor, see http://supervisord.org/configuration.html for docs
COPY ./tor.conf /etc/supervisor/conf.d/tor.conf
# Switch back to the unprivileged selenium user
USER seluser