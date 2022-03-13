import os, sys

def getPHPTemplate(method):
    return"""<?php

function arrayValuesEqual(array $array1, array $array2): bool
{
    return array_diff($array1, $array2) === array_diff($array2, $array1);
}

header_remove();
header("Content-type: application/json; charset=utf-8");

if ($_SERVER['REQUEST_METHOD'] !== '%s') {
    http_response_code(405);
    echo json_encode("The request has to be a %s request");
    return false;
};

if ($_SERVER['HTTP_ACCEPT'] !== 'application/json') {
    http_response_code(415);
    echo json_encode("The request body has to be JSON");
    return false;
}

// TODO: Add service functionality below
return true;""" % (method, method)


def getXMLTemplate():
    return"""<orchestration>
    <services>
        <service>
            <name>get_example</name>
            <target_url>http://localhost:8000</target_url>
            <method>GET</method>
        </service>
        <service>
            <name>post_example</name>
            <target_url>http://localhost:8001</target_url>
            <method>POST</method>
            <parameters>
                <parameter>
                    <name>input_1</name>
                    <type>float</type>
                </parameter>
            </parameters>
        </service>
    </services>
    <define>
        <variable>
            <name>a</name>
            <type>float</type>
        </variable>
    </define>
    <operations>
        <operation>
            <service_name>post_example</service_name>
            <inputs>
                <input>
                    <alias>input_1</alias>
                    <value>
                        <variable>a</variable>
                    </value>
                </input>
            </inputs>
        </operation>
    </operations>
</orchestration>"""

def getDockerFileContents(newServiceName):
    return "FROM php:7.4-apache\nCOPY ./%s /var/www/html/" % (newServiceName)

def getDockerComposeService(newServiceName, port):
    return """
  %s:
    build:
      context: .
      dockerfile: %s/Dockerfile
    ports:
      - %d:80
    volumes:
      - ./%s:/var/www/html/\n""" % (newServiceName, newServiceName, port, newServiceName)

if __name__ == "__main__":
    dirs = os.listdir( "." )


    if "orchestration.xml" not in dirs:
        xmlTemplate = open("./orchestration.xml", "w")
        xmlTemplate.write(getXMLTemplate())
        xmlTemplate.close()

    if "docker-compose.yaml" not in dirs:
        dockerComposeFile = open("./docker-compose.yaml", "w")
        dockerComposeFile.write("version: '3.1'\n\nservices:\n")
        dockerComposeFile.close()
    newServiceName = input("Please enter new service name\n")
    if newServiceName in dirs:
        print ("This service already exists")
        exit(1)


    os.mkdir(newServiceName)
    dockerFile = open(newServiceName + "/Dockerfile", "w")
    dockerFile.write(getDockerFileContents(newServiceName))
    dockerFile.close()


    serviceMethod = input("Please enter the desired web service method (POST/GET)\n")
    while serviceMethod not in ["GET", "POST", "get", "post"]:
        print ("Incorret service method: " + serviceMethod)
        serviceMethod = input("Please enter the desired web service method (POST/GET)\n")

    phpFile = open(newServiceName + "/index.php", "w")
    phpFile.write(getPHPTemplate(serviceMethod))
    phpFile.close()

    dockerComposeConfirm = input("Would you like to add this service to the docker-compose file? (Y/n)\n")
    while dockerComposeConfirm not in ["Y", "N", "yes", "no", "YES", "NO", "y", "n"]:
        print ("Not a valid response: " + dockerComposeConfirm)
        dockerComposeConfirm = input("Would you like to add this service to the docker-compose file? (Y/n)\n")

    if dockerComposeConfirm in ["N", "n", "no", "NO"]:
        print("New service template generated. Please make sure you add it to docker-compose.yaml manually")
        exit(0)

    port = input("Which port should the service be exposed on? (Integer)\n")
    while not port.isnumeric():
        print ("Not a valid port: " + port)
        port = input("Which port should the service be exposed on? (Integer)\n")

    dockerComposeFile = open("./docker-compose.yaml", "a")
    dockerComposeFile.write(getDockerComposeService(newServiceName, int(port)))
    dockerComposeFile.close()

    print ("New service template generated. Successfully added to docker-compose.yaml")

    

    