NAME ?= petelealiieej

all:	data test build run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

data:
	wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
	wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA10.xml

build:
	docker build -t ${NAME}/isspdt:midterm .

run:
	docker run --name "ISSPDT" -d -p 5015:5000 ${NAME}/isspdt:midterm

test:
	pytest

push:
	docker push ${NAME}/isspdt:midterm
