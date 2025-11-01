# Apache Flume 1.9.0 on OpenJDK 8
FROM openjdk:8-jre-slim

ENV FLUME_VERSION=1.9.0 \
    FLUME_HOME=/opt/flume \
    PATH=/opt/flume/bin:$PATH

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates bash tini; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir -p /opt; \
    curl -fsSL https://archive.apache.org/dist/flume/${FLUME_VERSION}/apache-flume-${FLUME_VERSION}-bin.tar.gz -o /tmp/flume.tgz; \
    tar -xzf /tmp/flume.tgz -C /opt; \
    mv /opt/apache-flume-${FLUME_VERSION}-bin ${FLUME_HOME}; \
    rm -f /tmp/flume.tgz; \
    adduser --disabled-password --gecos "" --home /opt/flume --uid 1000 flume || true

WORKDIR /opt/flume

# Default conf location
COPY flume.conf /opt/flume/conf/flume.conf

# Create data/logs mount point
RUN mkdir -p /data/logs && chown -R 1000:1000 /data /opt/flume

USER 1000

ENTRYPOINT ["tini", "--"]
CMD ["/opt/flume/bin/flume-ng", "version"]


