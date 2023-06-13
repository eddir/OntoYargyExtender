# OntologyFiller

## Description

This is a web application that allows users to fill in an ontology with data from an unstructured text. The
application is based on the [OntologyExtender](https://github.com/W1nterFox/OntologyExtender) library. 

The application is composed of two main components: the web interface and the filler. Each component
was isolated in a Docker container. Communication between the components is done via REST API calls and message queues.

## Installation

### Requirements

- Docker
- Docker Compose

### Steps

1. Clone the repository with `git clone https://github.com/eddir/OntologyFiller.git`
2. Run `docker-compose up` in the root directory of the project
3. Open `http://localhost:8888` in your browser
4. Enjoy!

## Usage

### Web Interface

On first access, the web interface will ask the user to log in. The default credentials are `admin` for the username 
and `admin` for the password. You can manage users from the `Users` page.

The web interface is the main component of the application. It allows users to upload a text file and select an ontology
to fill in. 

![Web Interface](/.github/images/screen1.png)

After the user uploads a file, the application will start processing it. The user will receive a notification when the
processing is finished. Once the processing is finished, the user can download the filled ontology.

![Web Interface](/.github/images/screen2.png)

### Filler

The filler is the component that does the actual processing of the text file. It is based on the
[OntologyExtender](https://github.com/W1nterFox/OntologyExtender) library. The filler is a command line application
written in Python. It can be used as a standalone application or as a Docker container. Once the filler is started, it
will wait for a message containing the path to the text file to process. After the processing is finished, the filler
will send a message containing the path to the filled ontology.

This component uses NLP techniques to extract information from the text file. The extracted information is then used to
fill in the ontology. The filler uses the [Yargy parser](https://github.com/natasha/yargy) to extract information from
the text file and the [OntologyExtender](https://github.com/W1nterFox/OntologyExtender) library to fill in the ontology
with the extracted information and to generate the filled ontology in OWL format. You can use Protégé or any other
ontology editor to view the filled ontology.

Filler requires a predefined rule set to be able to extract information from the given text file. The rule set is
defined in a DSL file, which contains a set of rules that describe specific domain concepts. The DSL file is written in
the [Yargy DSL](https://habr.com/ru/articles/349864/) language. The DSL file must be placed in the `ontologyExtender/app
/parser.py` directory. The filler will automatically load the DSL file when it starts. You can find an example of a DSL
file in the `ontologyExtender/app/parser.py` directory. As an example, the following DSL file describes the concept of
a knowledge base of SSTU teachers bios.

## Configuration

The application can be configured by editing the `.env` file. The following options are available:

- `HTTP_PORT` - the port on which the web interface will be available
- `HTTPS_PORT` - the port on which the web interface will be available
- `SECRET_KEY` - the secret key used by the web interface
- `DEBUG` - whether the web interface should be in debug mode or not
- `APP_DOMAIN` - the domain on which the web interface will be available
- `COMPANY_NAME` - the name of the company that owns the web interface
- `PUSHER_APP_ID` - the ID of the Pusher application used by the web interface
- `PUSHER_APP_KEY` - the key of the Pusher application used by the web interface
- `PUSHER_APP_SECRET` - the secret of the Pusher application used by the web interface
- `PUSHER_CLUSTER` - the cluster of the Pusher application used by the web interface

## Web services

- User web interface - `https://localhost:8888`
- PGAdmin - `http://localhost:8008`
- Kafdrop - `http://localhost:8888`

## Built With

- [Docker](https://www.docker.com/) - Containerization platform
- [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container Docker applications
- [Yargy parser](https://github.com/natasha/yargy) - Rule-based information extraction library
- [OntologyExtender](https://github.com/w1nterfox/ontologyextender) - Library for extending ontologies with information
  extracted from unstructured text
- [Nginx](https://www.nginx.com/) - Web server for proxying requests
- [Kafka](https://kafka.apache.org/) - Message broker for communication between components
- [PostgreSQL](https://www.postgresql.org/) - Database for storing user data
- [Pusher](https://pusher.com/) - Service for sending notifications to the web interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was developed as part of my bachelor's thesis. Special thanks to my supervisor, Dr. Tatiana Shulga for her
guidance and support.