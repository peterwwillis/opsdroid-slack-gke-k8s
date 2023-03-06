# First prepare the Google Cloud SDK and Kubectl,
# so we can authenticate, debug, etc.

FROM alpine:3.16 AS gcloud-sdk

ARG CLOUD_SDK_VERSION=414.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION

ENV PATH /google-cloud-sdk/bin:$PATH

RUN set -eux ; \
    apk --no-cache add curl python3 ; \
    curl -fsSL -o google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz \
        https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz ; \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz ; \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz ; \
    ln -s /lib /lib64 ; \
    gcloud config set core/disable_usage_reporting true ; \
    gcloud components install kubectl ; \
    gcloud --version


# Next we build our Opsdroid image (on top of the official Opsdroid image).
# Copy the gcloud tools above into this image.

FROM ghcr.io/opsdroid/opsdroid:v0.28.0 AS production

#COPY --from=gcloud-sdk /google-cloud-sdk /google-cloud-sdk

COPY skills /chatops/skills
COPY config.yaml /etc/opsdroid/configuration.yaml

# Technically the above is all we need to run Opsdroid.
# But to save time on start-up, we'll pre-install all the
# Python packages in each skill's `requirements.txt` file.
RUN set -x; cd /chatops/skills ; \
    for i in requirements.txt */requirements.txt ; do \
        [ -e "$i" ] || continue ; \
        pip install -r "$i" ; \
    done

RUN mkdir -p ~/.kube ~/.config/gcloud

ENV PATH=$PATH:/google-cloud-sdk/bin



#############################
######## Development image

FROM production AS development

USER root

COPY install_tooling.sh /tmp
RUN /tmp/install_tooling.sh

