FROM maven:latest AS mvnontosimdocker

# build layer
WORKDIR /app
ADD pom.xml /app
COPY . /app

RUN mvn -v
RUN mvn package

# tomcat-server
FROM tomcat:9.0-jre8-alpine
RUN rm -rf /usr/local/tomcat/webapps/*
COPY --from=mvnontosimdocker /app/target/OntoSimilarity.war $CATALINA_HOME/webapps/ROOT.war

EXPOSE 8080

CMD ["catalina.sh", "run"]
