# Workflow for linking External datasets

This project proposal presents an approach for ontology alignment through the use of an unsupervised Recursive neural network.

### About the Project
In this workflow, we will explore reading and parsing the ontology and extracting all necessary information about concepts and instances, generating semantic vectors for each entity with different meta information like entity hierarchy, object property, data property, and restrictions and designing User Interface based system which will show all necessary information about the workflow.

### Quickstart
1. The project requires following tools to run:
	* `docker` : Installation instructions for ubuntu can be found [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
2. Clone the repository
	 `git clone https://github.com/dbpedia/linking.git`.
3. Before starting the application, please make sure there is enough space (atleast - 15GB Harddisk) and docker with memory atleast (free memory 10GB) are available. 
4. Deploy the application by following the steps in.

### Dataset:
Please download source, target ontology and reference file.
http://oaei.ontologymatching.org/2019/anatomy/

### Deployment
There are three different components available:
1. Web
2. Batch
3. OAEI

#### 1.a. Starting project [<b>WEB</b>]
- ./ontobuilt.sh prod start
- Do you want to build from scratch [Y/N] ? <br />
y
- --> What you want to build [WEB/BATCH/OAEI] ? <br />
web
- ----> Do you want to copy FastText pretrained model[Y/N] <br />
n (If you downloaded from git then file should be at the folder otherwise you have to give your local path)
- ----> Do you want to copy OntoModel pretrained model[Y/N] <br />
n (If you downloaded from git then file should be at the folder otherwise you have to give your local path)

It should have: <br/>
IMAGE:- <br/>
<table>
    <tr> 
        <td>  REPOSITORY  </td>
        <td>  TAG  </td>
        <td>  SIZE  </td>
    </tr>
    <tr> 
        <td>  ontosim_imgweb  </td>
        <td>   v1  </td>
        <td>  4.49GB  </td>
    </tr>
    <tr> 
        <td>  ubuntu  </td>
        <td>   18.04   </td>
        <td>  64.2MB </td>
    </tr>
</table>

CONTAINER:- <br/>
<table>
    <tr>
        <td> IMAGE </td>
        <td> COMMAND </td>
        <td> PORTS </td>
        <td> NAMES </td>
    </tr>
    <tr>
        <td> ontosim_imgweb:v1 </td>
        <td> supervisord </td>
        <td> 0.0.0.0:5000->5000/tcp, 0.0.0.0:8080->8080/tcp </td>
        <td> ontosim_app </td>
    </tr>
</table>

Browser: <br />
http://localhost:8080/OntoSimilarity/

Upload the source and target owl files.

#### 1.b. Stopping project [<b>WEB</b>]
- ./ontobuilt.sh prod stop

#### 1.c. Deleting project [<b>WEB</b>]
- ./ontobuilt.sh prod del


#### 2.a. Starting project [<b>BATCH</b>]
- ./ontobuilt.sh prod start
- Do you want to build from scratch [Y/N] ? <br />
y
- --> What you want to build [WEB/BATCH/OAEI] ? <br />
batch
- ----> Do you want to copy FastText pretrained model[Y/N] <br />
n (If you downloaded from git then file should be at the folder otherwise you have to give your local path)
- ----> Do you want to copy OntoModel pretrained model[Y/N] <br />
n (If you downloaded from git then file should be at the folder otherwise you have to give your local path)
- ------> Please Enter Source OWL file path <br />
provide full local path of owl file <br />
(e.g. /Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/anatomy-dataset/human.owl)
- ------> Please Enter Target OWL file path <br />
provide full local path of owl file <br />
(e.g. /Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/anatomy-dataset/mouse.owl)

It should have: <br/>
IMAGE:- <br/>
<table>
<tr> 
<td>  REPOSITORY  </td>
<td>  TAG  </td>
<td>  SIZE  </td>
</tr>
<tr> 
<td>  ontosim_imgbatch  </td>
<td>   v1  </td>
<td>  4.49GB  </td>
</tr>
<tr> 
<td>  ubuntu  </td>
<td>   18.04   </td>
<td>  64.2MB </td>
</tr>
</table>

CONTAINER:- <br/>
<table>
<tr>
<td> IMAGE </td>
<td> COMMAND </td>
<td> PORTS </td>
<td> NAMES </td>
</tr>
<tr>
<td> ontosim_imgbatch:v1 </td>
<td> supervisord </td>
<td> 0.0.0.0:5000->5000/tcp </td>
<td> ontosim_app </td>
</tr>
</table>

Check Output: <br />
docker exec -it ontosim_app bash <br />
cd /usr/ontosim/java/ontofiles/local <br />
cat result.rdf <br />

#### 2.b. Stopping project [<b>BATCH</b>]
- ./ontobuilt.sh prod stop

#### 2.c. Deleting project [<b>BATCH</b>]
- ./ontobuilt.sh prod del



