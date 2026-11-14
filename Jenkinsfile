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
        PATH+DOCKER = 'C:\\Users\\jurep\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin'
        DOCKER_CONFIG = 'C:\\Users\\jurep\\.docker'
        DOCKER_HOST = 'npipe:////./pipe/dockerDesktopLinuxEngine'
    }

    stages {
        stage('Obtener codigo') {
            steps {
                checkout scm
            }
        }

        stage('Verificar herramientas') {
            steps {
                bat 'docker --version'
                bat 'docker compose version'
            }
        }

        stage('Construir imagenes') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                bat 'docker compose run --rm --no-deps pedidos python -m unittest discover -s tests -v'
            }
        }

        stage('Validar comunicacion y resultado') {
            steps {
                bat 'docker compose up -d inventario'
                script {
                    def salida = bat(
                        returnStdout: true,
                        script: 'docker compose run --rm pedidos'
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
            bat 'docker compose down --remove-orphans'
        }
    }
}
