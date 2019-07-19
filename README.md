# Workflow for linking External datasets

This project proposal presents an approach for ontology alignment through the use of an unsupervised mixed neural network.

### About the Project
In this workflow, we will explore reading and parsing the ontology and extracting all necessary information about concepts and instances, generating semantic vectors for each entity with different meta information like entity hierarchy, object property, data property, and restrictions and designing User Interface based system which will show all necessary information about the workflow.

### Quickstart
1. The project requires following tools to run:
	* `docker` : Installation instructions for ubuntu can be found [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
	* `docker-compose`: can be installed using `pip`.
		* `pip3 install docker compose` 
2. Clone the repository
	 `git clone https://github.com/dbpedia/linking.git`.
3. Deploy the application 
	`./ontobuilt.sh prod start`

For more options to start the application, read the [setup guide](https://github.com/dbpedia/linking/wiki/Setup_Guide).

### Wiki
The wiki for this project can be found [here](https://github.com/dbpedia/linking/wiki).

