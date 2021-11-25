Esta es uno de los componentes core de la arquitectura pues recibe todos los request directamente del kinesis Data stream y los distribuye en diferentes componentes de la arquitectura. O también los transforma y los almacena tenemos en esta sección dos ejemplos;
1. [Creación funcón Lambda](#create-lambda)
2. [Lambda Function 1](#lambda1)
3. [Lambda Function 2](#lambda2)
4. [Instalar librerías en Lambda](#lambda-libraries)

## Creación de función Lambda <a name="create-lambda"></a>
Para crear una función lambda entra al sección de Lambda en AWS y selecciona la opción `Create Function` 
Escribimos el nombre, ambiente de ejecución Python 3.9 arquitectura x86_64 y el rol debemos crear un rol en IAM que tenga acceso a los servicios que utilizamos en la arquitectura. Presionamos el botón crear Función

## Lambda Function 1 <a name="lambda1"></a>
Este código correesponde a la función de nuestra arquitectura `transform to json` básicamente recibe un json de kinesis stream y se encarga de realizar llamar un servicio de comprehend y guardar tweets en las tablas de Dynamo de la sección anterior, algunas secciones importantes del código son las siguientes:
```Python
	dynamo_db = boto3.resource('dynamodb')
    comprehend =  boto3.client(service_name = 'comprehend')
    s3 = boto3.resource('s3')
    kinesis_client, stream_name = boto3.client('kinesis'), 'sentiment-outputstream'
    table = dynamo_db.Table('tweets_for_sentiment')
    table_sentiments = dynamo_db.Table('tweets_sentiment')
```
lo que hacemos es crear un cliente o un recurso a los elementos *recuerda que el rol encargado de ejecutar esta función debería tener acceso a los servicios de Comprehend, S3 y Kinesis* instanciamos dos objetos tablas que usaremos más adelante.
```Python
	decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]
```
parsear y decodificar los datos recibidos de Kinesis. Acto seguido podemos procesar cada registro de manera individual en un ciclo, en el cual creamos el objeto y obtenemos su calificación de sentimientos y lo distribuimos en los siguientes datos.
```Python
	sentiment_all = comprehend.detect_sentiment(Text = text, LanguageCode = 'es')
    sentiment = sentiment_all['Sentiment']
```
```Python
	kinesis_client.put_record(
	    StreamName=stream_name,
	    Data=json.dumps(dict_sentiment_),
	    PartitionKey="sentimentpartitionkey"
	)
	  
	#enviar datos a Kinesis
	with table.batch_writer() as batch_writer:
	  # write to dynamo
	  batch_writer.put_item(
	    Item = dict_tweet
	  )
```

## Lambda Function 2 <a name="lambda2"></a>
Esta función Lambda recibe datos de Kinesis Firehose que configuramos en el primer paso su función principal es tomar los datos de kinesis Firehose y transformalos en csv y almacenarlos en un bucket de manera organizada.
tiene secciones importantes:
```Python
	#tomar la fecha de ejecución actual
	now = datetime.now()
	year, month, day, hour = now.year, now.month, now.day, now.hour
```
estas variables serán importantes para crear el archivo y almacenarlo según su hora de ejecución,
```Python
	decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]
    
    key = f'tweets_json/{year}/{month}/{day}/{hour}/tweets.csv'
    local_file_name = '/tmp/test.csv'
```
va a crear un archivo local temporal y lo almacenara en nuestro bucket de s3
```Python
    try:
		#archivo existe
	except ClientError:
    	#archivo no existe
    	pass
```

