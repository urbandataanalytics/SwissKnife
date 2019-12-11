# SwissKnife

[![Build Status](http://datasrv.urbandataanalytics.com:8080/job/SwissKnife_master_test/badge/icon)](http://datasrv.urbandataanalytics.com:8080/job/SwissKnife_master_test/)

Librería de utilidades y funcionalidades comunes creada por el equipo de Data Engineering de UDA Real Estate.

## Dockerfile

El dockerfile está diseñado para ejecutar los tests (no tendria sentido dockerizar una librería). Ejecutando la imagen construída, obtendremos directamente el resultado de nosetests.xml por consola, de tal forma que si la queremos en un fichero, deberíamos hacer lo siguiente:

```bash
sudo docker run swissknife:latest > nosetests.xml
```

## Cómo obtener el Entorno de Ejecución actual

El objeto se encuentra localizado en **SwissKnife.info.CURRENT_ENVIRONMENT**. Devuelve un objeto del tipo *ExecutionEnvironment*.

Dicho objeto se trata de un enumerado con los siguientes valores:

- PRO  -> "preo"
- PRE  -> "pre"
- DEV  -> "dev"
- TEST -> "test

Adicionalmente, tiene los siguientes métodos que simplifican conocer cual entorno de ejecución es sin tener que hacer comparaciones
directas con el enumerado:

- is_pro()  -> bool
- is_pre()  -> bool
- is_dev()  -> bool
- is_test() -> bool

El valor es tomado de la variable de entorno "ENV" que puede tener los valores "pro", "pre", "dev" y "test". Se permite que el texto esté en 
mayúscula total o parcialmente. Si dicha variable no existe o tiene un valor incorrecto, la aplicación devolverá un ExecutionEnvironment
con el valor por defecto, *DEV*.

## How to install

- basic install:
  ```bash
    pip install UDASwissKnife
  ```
- Install with an extra. For example, _avro_:
  ```bash
    pip install UDASwissKnife[avro]
  ```
- Install several extras. For example, _avro_ and _gcloud_:
  ```bash
    pip install UDASwissKnife[avro,gcloud]
  ```

- Install all extras:
```bash
pip install UDASwissKnife[all]
```

## Basic libraries

    - info

## Extra libraries

    - avro: Includes AvroWriter.
    - gcloud: Includes GCloudStreaming.