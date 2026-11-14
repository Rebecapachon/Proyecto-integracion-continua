pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DOCKER_CLI = 'C:\\Users\\jurep\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        DOCKER_CONFIG = 'C:\\Users\\jurep\\.docker'
        DOCKER_HOST = 'npipe:////./pipe/dockerDesktopLinuxEngine'
        PATH = "C:\\Users\\jurep\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    }

    stages {
        stage('Obtener codigo') {
            steps {
                checkout scm
            }
        }

        stage('Verificar herramientas') {
            steps {
                bat '"%DOCKER_CLI%" --version'
                bat '"%DOCKER_CLI%" compose version'
            }
        }

        stage('Construir imagenes') {
            steps {
                bat '"%DOCKER_CLI%" compose build'
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                bat '"%DOCKER_CLI%" compose run --rm --no-deps pedidos python -m unittest discover -s tests -v'
            }
        }

        stage('Validar comunicacion y resultado') {
            steps {
                bat '"%DOCKER_CLI%" compose up -d inventario'
                script {
                    def salida = bat(
                        returnStdout: true,
                        script: '"%DOCKER_CLI%" compose run --rm pedidos'
                    ).trim()
                    echo salida
                    if (!(salida =~ /"total"\s*:\s*189000/)) {
                        error('El pedido no produjo el total esperado de 189000.')
                    }
                }
            }
        }
    }

    post {
        always {
            bat '"%DOCKER_CLI%" compose down --remove-orphans'
        }
    }
}
