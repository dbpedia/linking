FROM tomcat:8.5-jdk12-openjdk-oracle

ADD OntoSimilarity/ /home/OntoSimilarity
WORKDIR /home/OntoSimilarity

RUN yum install -y wget
RUN wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
RUN yum install -y apache-maven
RUN mvn package
RUN rm -rf /usr/local/tomcat/webapps/*
RUN cp target/OntoSimilarity-0.0.1-SNAPSHOT.war /usr/local/tomcat/webapps/ROOT.war

#ADD docker/tomcat-users.xml /usr/local/tomcat/conf/
#ADD docker/context.xml /usr/local/tomcat/webapps/manager/META-INF/

EXPOSE 8080

CMD ["/usr/local/tomcat/bin/catalina.sh", "run"]
