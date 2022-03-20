NAME ?= petelealiieej

all:	build test run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/isspdt:midterm .

run:
	docker run --name "ISSPDT" -d -p 5015:5000 ${NAME}/isspdt:midterm

test:
	docker run --rm ${NAME}/isspdt:midterm pytest /app/

push:
	docker push ${NAME}/isspdt:midterm
