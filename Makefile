app_name = wsharp07/micovid

build:
	@docker build -t $(app_name) .

run:
	docker run --detach -p 8003:80 --env-file=.env $(app_name)

kill:
	@echo 'Killing container...'
	@docker ps | grep $(app_name) | awk '{print $$1}' | xargs docker kill
