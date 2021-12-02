El proceso de creación de una tabla de Dynamo es muy sencillo sin embargo mostramos las tablas necesarias en nuestro proceso:

para crear una tabla de Dynamo vamos a nuestra tabla de Dynamo en AWS vamos a la consola y seleccionamos la opción de Dynamo una vez en la pantalla de Dynamo veremos el siguiente menú:
![Menú de Dynamo](../Imagenes/creates_dynamo_tables_step1.JPG "Menu Principal")
Seleccionamos la opción de tablas, el siguiente paso es
![Crear tabla](../Imagenes/creates_dynamo_tables_step2.JPG "Crear tabla")
presionar el botón `Create Table`
y seguiremos la configuración base en la configuración avanzada podemos configurar el tamaño de los lotes de entrada pero esto está relacionado con la cantidad de peticiones para nuestra tabla. La mejor opción es crear la tabla y analizar las métricas de lectura y escritura para poder determinar si es necesario escalar o no.
![Menu Tablas](../Imagenes/creates_dynamo_tables_step3.JPG "Menu tabla")
por utimo cramos la tabla y en nuestr menu de tablas podemos observar las tablas creadas hay que tener en cuenta estos nombres porque los veremos en nuestra sección de Lambda y Kinesis en algunos casos.
![Tablas](../Imagenes/creates_dynamo_tables_step4.JPG "Tablas")
podemos analizar la capacidad de nuestra tabla observando las métricas que poseen y de esta manera determinar si es necesario escalar de acuerdo a las métricas de uso, por ejemplo:
![Métricas](../Imagenes/creates_dynamo_tables_step5.JPG "Métricas")
los contenidos de esta tabla se pueden ver utilizando distintos medios pero para mostrar que nuestra tabla ya recibe datos mostramos la siguiente imagen:
![Contenido](../Imagenes/creates_dynamo_tables_step6.JPG "Contenido")