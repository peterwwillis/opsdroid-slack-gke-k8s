# opsdroid-slack-gke-k8s

## Summary

This repository contains all you need to deploy an OpsDroid chat bot connected to Slack, running in Kubernetes, with tools to use Google Cloud Kubernetes Engine (GKE). It also assumes you'll use Google Cloud Container Registry.

Look through the various files to change your bot settings, container name, GCP project, etc.

## Description

Opsdroid is a chat bot that connects to Slack and interacts with users. It does not have the full functionality of Slack, but it can do basic chat things (talk to users in DM or in a channel). By adding custom Python code, you can control what the bot does and execute arbitrary code from the bot.

The code that you add to Opsdroid to make it do things are called *Skills*. A *Skill* is just a Python package that hooks into Opsdroid. Opsdroid requires asynchronous functions, so it's not quite as easy as pie, but there are lots of examples to work from. (See **Notes** section below)

All you need to do to add functionality to Opsdroid is to add an Opsdroid *Skill* to the [config.yaml](./config.yaml) file. The *Skill* code can be hosted in remote repositories, or simply copied into the [skills/](skills/) directory. (See [skills/ping.py](skills/ping.py) for the simplest example) (note: you'll need to add an SSH key to access private repositories)

## Opsdroid setup

- Create a Slack bot called **opsdroid-slack-gke-k8s** in Slack.com for use with a *socket-based bot*, with enough OAuth scopes to do whatever you want.
- Configure Opsdroid to load the Slack connector. Credentials are loaded via environment variables.
- A Docker container is pulled containing the Opsdroid software.
- Build a new container on that base, only adding the [skills/](skills/) directory and [config.yaml](./config.yaml).

---

## Development workflow: CI/CD

## Building
1. Open a new branch in Git and push your code.
1. A CI/CD job will run that will build and push a container (ex. `gcr.io/my-project/image:$ENV-$BRANCH-$USERNAME`).

### Testing

Currently no testing functionality. The following needs to be added to this repo:

1. Create a new 'test bot' in Slack
1. Modify [k8s-manifests/deployment.yaml](k8s-manifests/deployment.yaml) to change the namespace to something like the Docker image name. Also add a k8s secret manifest to create the bot credentials in the new namespace.
1. Modify the CI/CD job to deploy the test bot based on a specific Git tag

### Deploying

1. Merge your changes to the `main` branch
1. Pull the `main` branch
1. Add a new semantic version Git tag prefixed with `v` (`git tag vX.X.X`)
1. Push the tag (`git push --tags`)
1. This will trigger a job that will build and push an image (ex. `gcr.io/my-project/image:$ENV-vX.X.X`).
1. Then a job will run that will deploy this to Kubernetes

---

## Development workflow: Local development

## Prep

1. Create file `.myenv` with a Slack bot configuration. Example:
   
   ```
   SLACK_APP_TOKEN=xapp-1-hfihusdifhlshdflhjslhdjflsjkhdflksjhdflksjhdfl
   SLACK_BOT_TOKEN=xoxb-2-ksjhdflksjhflkhjslkfjhlkjshdfsdkfjlksjhdfkhjsd
   ```

2. Set up your local `gcloud` tool to authenticate to Google Cloud.
3. Set up your local `kubectl` configuration to authenticate to a GKE cluster.
4. Install the `devspace` tool

## Bulding

1. Run `make deploy` to build images with Devspace

## Testing

1. Run `make dev` to drop into the Devspace development environment
2. Run `make opsdroid` inside the dev environment to run Opsdroid itself


---

## Adding a *Skill*
1. Find or create a new *Skill*
   1. You can re-use an existing skill by referring to its [Git repository](https://docs.opsdroid.dev/en/stable/configuration.html#git-repository). Currently we do not add a deploy key to our Opsdroid deployment, so this will only work with public repositories.
   2. Create a new python package in the [skills/](skills/) directory. Refer to existing ones or the [official documentation](https://docs.opsdroid.dev/en/stable/skills/index.html). If you add a `requirements.txt` file to your package, dependencies are installed automatically by Opsdroid at runtime (!!).
2. Edit the [config.yaml](./config.yaml) file to add the new skill.
3. Deploy the new code/configuration.


---

# Notes
- Developing opsdroid skills
  - Example skills:
    - https://gitlab.com/Sleuth56/imageofthehour/-/blob/main/Skill/__init__.py
    - https://gitlab.com/Sleuth56/Matrix-Community-Manager/-/tree/master/Skill
    - https://github.com/whateverany-scratch/opsdroid-minecraft-skill/blob/main/__init__.py
    - https://github.com/opsdroid/skill-cloudhealth/blob/master/__init__.py
    - https://github.com/kadasz/skill-ssh
    - https://github.com/codexlynx/opsdroid-skill-docker-daemon
    - https://github.com/alibahramiyan/opsdroid-k8s-skills
