# Containerized Vector Store using Langchain
This is a repo for a containerized app that allows you to chat with data stored in a given set of documents via an LLM. This repo uses langchain for prompt writing, fastapi for api functionality, huggingface via a langchain module for document embedding, ChromaDB via a langchain module for storing document embeddings, and llama-cpp-python as the model interface.

## Build the image
Docker must be installed on your computer. When using an Analytica computer, you might have to call R3 and get added to the Docker users list, even if docker desktop is installed. 

With the docker engine running, from the root directory of this repo, run:

```
 docker build -t vectorstore:version0 .
```

You can name/tag the image however you'd like. Building might take around 10 minutes. 

## Prior to running the built image
Required folder structure of the repo, create whatever folders are needed prior to building:

repo  
  |---Dockerfile, README.md, llama.py, etc.  
  |---bind  
      |---model  
          put your model here  
      |---documents  
          put your documents here (txt and pdf)  
      |---vectorstore  
          leave empty, container will populate  

Prior to running the image, you need a model to use which is llama-cpp compliant. This must be stored in the bind/model folder relative to this repo. Create this folder if it does not exist. This repo was tested with this model:

https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF/blob/main/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf 

You can download it from this url. It is around 5 GB. 

You must also have some documents to vectorize and chat with. These must be stored in bind/documents. This repo supports text and pdf documents. "pdf" and "txt" extensions are necessary and must be lower case. Documents stored in the above folder will automatically be vectorized upon running the built image. The vectorstore will be saved to bind/vectorstore. Upon subsequent image runs your documents should be removed from bind/documents and the image will use the stored vectorstore. This repo does not support adding new documents to an existing vector store, but this is possible. 

Some documents are stored in the repo if you wish to use these. They are about mushrooms and pentaquarks. 

## Run
The following command will create a container from the built image: 

```
docker run --mount type=bind,source=/absolute/path/to/folder/bind,target=/app/persist  vectorstore:version0
```

You must include the absolute path to your "bind" directory that contains the model and documents for the mount option, relative paths will not work. This can be obtained with the pwd command while in the bind directory. 

An api will be set up running on the container at http://127.0.0.1:8000. If you want, you can forward this port to you local computer port using the -p 8000:8000 option (or something similar) in the run command and query the api that way. However, doing so might cause you to run into security issues on an Analytica computer. See main.py for api routing info. Alternatively, you can just use the docker exec command as detailed in the next section. 

A container printout with "INFO: Application startup complete." indicates the api is running. It may take two or three minutes for the container to execute the startup code and vectorize documents. More documents will lengthen the startup time. 

## Chat
With the container running, after the api has successfully deployed, run

```
docker ps
```

in a different terminal to get the name of your container. Then insert it into the command below, along with a relevant question.


```
docker exec -w /app container_name python3 test_request.py --question "What mushrooms are deadly?"
```

The api will return an answer as well as a list of text snippets retrieved from the vector store. These will be cited by their respective documents. The container itself will also print out the prompt formatted by langchain. 

## Notes
The behavior of the LLM can be changed in the llama.py file (e.g., temperature, etc.). A rebuild (that should only take a few seconds) will be needed to implement the changes.

How the documents are split and stored, as well as how many are used in the response, can be modified in the llama.py file.

Restarting a stopped container has not been tested, but should be feasible. You can always delete the old, stopped container and run a new one from the built image. 

Different models, as well as different document splits, will yield differing quality of results.
