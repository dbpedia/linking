FROM maven:latest AS mvnontosimdocker

# image layer
WORKDIR /app
ADD pom.xml /app
COPY . /app

RUN mvn -v
RUN mvn package


#RUN pwd
#RUN ls -l
#RUN ls -l target


FROM tomcat:9.0-jre8-alpine

COPY --from=mvnontosimdocker /app/target/OntoSimilarity.war $CATALINA_HOME/webapps/OntoSimilarity.war


#RUN pwd
#RUN ls -l
#RUN ls -l webapps/

EXPOSE 8080

CMD ["catalina.sh", "run"]