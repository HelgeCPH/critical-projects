.PHONY: cleandb


cleandb:
	rm -r neo4j/data/*

stopdb:
	docker stop depgraphneo4j
	docker rm depgraphneo4j