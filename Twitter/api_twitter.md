# API Twitter

En esta sección tenemos códigos y el paso a paso de configuración para el desarrollo de una aplicación que consuma datos de Twitter.

## Configuración inicial
Lo primero que debemos realizar es entrar a la página para [desarrolladores de Twitter](https://developer.twitter.com/en) y registrarnos, en el portal de desarrolladores podremos crear un nuevo proyecto:

![developer portal]('./Twitter/Imagenes/index_developers.JPG')

Presionar el botón `Create Project`
En esta pagína seguimos los pasos para crear una nueva aplicación:

1. Introducir nombre del proyecto
2. Caso de uso seleccionar el que mejor defina nuestra aplicación en nuestro caso es Estudiante
3. Agregar una descripción 
4. y por último seleccionar la opción de crear una nueva app
	1. Seleccionar el nombre de la aplicación
	2. Copia y guarda tus tokens en un lugar seguro, estos son los accesos de tu aplicación a Twitter, `NO LOS PUBLIQUES EN NINGUN LUGAR`

## Consumo de tweets usando Tweepy

El siguiente paso es instalar Tweepy en tu equipo o donde vayas a crear el productor de tweets en la máquina donde se ejecutará el productor
`> pip install tweepy`



