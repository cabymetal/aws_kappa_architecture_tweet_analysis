# aws_lambda_architecture_tweet_analysis
Proceso de montaje de una arquitectura Kappa para análisis de sentimientos en aws, en el año 2021

En este repositorio se almacena código y pasos de creación de una arquitectura kappa para el análisis de tweets en aws

# Caso de uso

La idea de este proyecto es llevar un proceso de consumo de datos vivos en este caso **Twitter** a AWS y montar toda una arquitectura que nos pueda ayudar al análisis de estos datos.

# 1 - Elección de una arquitectura de referencia

Para la implementación de esta arquitectura pensamos en dos opciones [Lambda](https://databricks.com/glossary/lambda-architecture) y [Kappa](https://hazelcast.com/glossary/kappa-architecture/) para nuestro caso decidimos utilizar la arquitectura **Lambda** porque nos permitía tener una opción de batch processing y otra de speed processing. En cada una de las carpetas de este repositorio se muestran las secciones del proceso

## consumo de la api de Twitter
podemos ver el paso a paso de configuración y códigos relacionados en la carpeta Twitter. además de un breve contexto de cada uno. Es el primer paso de este ejercicio en el cual tomamos datos de tweeter utilizando las llaves de una aplicación registrada.

