# Proyecto 2 - Bases de Datos II
### Integrantes
## Jean Pierre Sotomayor Cavero   100%

## Angel Mucha Huaman             100%

## Juan Torres                    100%


## Introducción
La exploración y extracción de información en documentos de texto involucra un proceso algorítmico fascinante y, en ciertos aspectos, intrincado. En la actualidad, se dispone de una amplia gama de técnicas y algoritmos diseñados para llevar a cabo búsquedas en archivos textuales, priorizando la precisión y la eficiencia. En este contexto, nos sumergiremos en la aplicación del método de indexación invertida para la búsqueda de textos en el conjunto de datos de ArXiv, una plataforma de distribución de archivos de código abierto.

## Objetivo
Este proyecto se centra en la óptima construcción de un índice invertido para facilitar tareas de búsqueda y recuperación en documentos de texto. Implicará el desarrollo de un sistema backend-frontend, utilizando código en Python para el backend y una interfaz gráfica de usuario (GUI) intuitiva como frontend. El objetivo primordial consistirá en comparar el rendimiento computacional de nuestra propia implementación del índice invertido con la de los sistemas de gestión de bases de datos PostgreSQL. La GUI resultante permitirá visualizar los resultados en los tres escenarios, y a partir de estos datos, se llevará a cabo un análisis de los tiempos de ejecución para evaluar la eficiencia de nuestro índice invertido.

### Descripción del dominio de datos
El conjunto de datos disponible en (https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs) contiene una amplia variedad de información sobre más de 18,000 canciones de Spotify, que incluye detalles como el artista, álbum, características de audio (por ejemplo, volumen), letras, el idioma de las letras, géneros y subgéneros.

Inicialmente, el conjunto de datos original fue utilizado en la tercera semana del proyecto TidyTuesday y solo comprendía características de audio y géneros. Para enriquecer la información, se agregaron las letras a través de la biblioteca Genius en R, y se incorporó el idioma de las letras utilizando la biblioteca langdetect en Python. Sin embargo, es importante tener en cuenta que aproximadamente solo la mitad de las canciones originales se encuentran disponibles en este conjunto de datos, ya que las letras no pudieron recuperarse para muchas de ellas.

