# base image 
FROM tensorflow/tensorflow 
#  work directory 
WORKDIR /app
# run executes the next command
RUN pip install tensorflow-hub flask 
# copy the file content  github copilot
COPY model ./model
#Look above 
COPY labels.txt main.py teste.jpg ./

# les ports suivants sont accessible  par la hôte
EXPOSE 5000
#default command executed when running the container 
CMD python main.py

