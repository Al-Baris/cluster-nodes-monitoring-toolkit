IMAGE_NAME=docker.moresophy.com/contextsuite/monitoring/cxs-core-monitoring
TAG=latest

all: build push

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

push: build
	docker push $(IMAGE_NAME):$(TAG)

run:
	docker run -d -p 80:80 $(IMAGE_NAME):$(TAG)

clean:
	docker rmi $(IMAGE_NAME):$(TAG)

env:
	pip install -r requirements.txt
