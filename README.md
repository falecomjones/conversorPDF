Este projeto é um container que converte de documentos de PDF|RTF para TXT, com o processo sendo monitorado pelo Luigi (https://luigi.readthedocs.io/en/stable/). Neste repositório contém os arquivos que formam a imagem: Docker file, arquivos .py, parametros, etc. 

Para utilizá-lo siga os passos:

  ~> Instalar o docker (claro, :D ): https://docs.docker.com/install/linux/docker-ce/ubuntu/;
  
  ~> Baixar a imagem: docker image pull jonessarmento/luigimage:1.0;
  
  ~> Rodar o container com os parametros da AWS:
  
  Comando: docker container run -p 8082:8082 -e BUCKET='s3://bucket/' -e AWSID='TUAAWSID' -e AWSSECRET='TUAAWSSECRET' -e REGION='us-east-1' -e FILEOUTPUT='json' -t jonessarmento/luigimage:1.0;
  
  ~> Se tudo funcionar, um arquivo chamado "output_BUCKET_.tar.gz" será retornado no bucket que você passou. 
  
 Valeu!
