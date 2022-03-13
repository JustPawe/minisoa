import xml.etree.ElementTree as ET
from os.path import exists
import os, sys
import json
import requests

# ----------------------Classes---------------------#
class Parameter:
    def __init__(self, name, ptype):
        self.name = name
        self.ptype = ptype
    
    def getName():
        return self.name
    
    def getPType():
        return self.ptype


#------------------------------------------------------#
class Service:
    def __init__(self, name, targetUrl, method, parameters):
        if method == "POST" and parameters == None:
            print("A POST service must have parameters")
            exit(1)
        self.name = name
        self.targetUrl = targetUrl
        self.method = method
        self.parameters = parameters

    def getParameters():
        return self.parameters
    
    def getName():
        return self.name
    
    def getTargetUrl():
        return self.target_url

#-------------------------------------------------------#
class Condition:
    def __init__(self, conditionVal, expression, thenVal, elseVal):
        self.conditionVal = conditionVal
        self.expression = expression
        self.thenVal = thenVal
        self.elseVal = elseVal

#--------------------------------------------------------#

class InputVariable: 
    def __init__(self, iType, value):
        self.iType = iType
        self.value = value


#------------------------------------------------------#
class Input:
    def __init__(self, alias, inputValue):
        self.alias = alias
        self.inputValue = inputValue

#------------------------------------------------------#

class Operation:
    def __init__(self, serviceName, inputs):
        self.serviceName = serviceName
        self.inputs = inputs

    def getServiceName():
        return self.serviceName

    def getInput():
        return self.inputs

#------------------------------------------------------#

class Main:
    def incorrectXMLExit():
        print ("Incorrect XML Schema not found exiting")
        exit(1)


#--------------------------------Prep---------------------------#
#-------------------------------------Variables--------------------#
    def createVar(vtype, vname):
        if vtype == "string":
            return input("Please enter the value for " + vname + "\n")
        if vtype == "int":
            return int(input("Please enter the value for " + vname + "\n"))
        if vtype == "float":
            return float(input("Please enter the value for " + vname + "\n"))

    def defineVariables(variables):
        definedVars = {}
        for child in variables:
            varname = child.find("name").text
            vartype = child.find("type").text
            definedVars[varname] = Main.createVar(vartype, varname)
        return definedVars

#-----------------------------------Services-------------------------#

    def getParameters(parameters):
        if parameters == None:
            return None
        definedParameters = []
        for child in parameters:
            paramName = child.find("name").text
            paramType = child.find("type").text
            definedParameters.append(Parameter(paramName, paramType))
        return definedParameters

    def requiredServices(services):
        definedServices = {}
        for child in services:
            serviceName = child.find("name").text
            serviceTargetUrl = child.find("target_url").text
            serviceMethod = child.find("method").text
            parameters = Main.getParameters(child.find("parameters"))
            definedServices[serviceName] = Service(serviceName, serviceTargetUrl, serviceMethod, parameters)

        return definedServices

#---------------------Operations------------------------------------#

    def decodeOperationXML(operation):
        serviceName = operation.find("service_name").text
        inputs = Main.inputs(operation.find("inputs"))
        return Operation(serviceName, inputs)

    def getConditionalInput(value):
        compareVal = Main.getInputTypeAndValue(value.find("compare_value"))
        condition = value.find("condition").text
        thenVal = Main.getInputTypeAndValue(value.find("then/result"))
        elseVal = None
        if value.find("else/result") != None:
            elseVal = Main.getInputTypeAndValue(value.find("else/result"))
        return Condition(compareVal, condition, thenVal, elseVal)


    def getInputTypeAndValue(value):
        child = value[0]
        inputType = child.tag
        if inputType == "variable":
            return InputVariable(inputType, child.text)
        if inputType == "operation": 
            return InputVariable(inputType, Main.decodeOperationXML(child))
        if inputType == "conditional":
            return InputVariable(inputType, Main.getConditionalInput(child))
        

    def inputs(inputs):
        definedInputs = []
        for child in inputs:
            alias = child.find("alias").text
            opInput = Main.getInputTypeAndValue(child.find("value"))
            definedInputs.append(Input(alias, opInput))
        return definedInputs
            
    def operations(operations):
        definedOperations = []
        for child in operations:
            operation = Main.decodeOperationXML(child)
            definedOperations.append(operation)
        return definedOperations

#--------------------------------------EXECUTION-----------------------------------#
    def getJsonDataFromInputDictionary(inputs):
        return json.dumps(inputs)

    def checkIfServiceHasRequiredParams(inputKeys, service):
        parameters = service.parameters
        paramNames = []
        for parameter in parameters:
            paramNames.append(parameter.name)

        if (len(inputKeys) != len(paramNames)):
            return False
        
        inputKeys.sort()
        paramNames.sort()

        for i in range(0, len(inputKeys)):
            if inputKeys[i] != paramNames[i]:
                return False
        
        return True
        
    def jsonPostRequest(targetUrl, inputs):
        headers = {'Accept': 'application/json'}
        response = requests.post(targetUrl, data = inputs, headers=headers)
        return json.loads(response.text)

    def handleCondition(condition, services, variables):
        conditionVal = Main.calculateInput(condition.conditionVal, services, variables)
        expression = str(conditionVal) + condition.expression
        if eval(expression):
            return Main.calculateInput(condition.thenVal, services, variables)
        if condition.elseVal != None:
            return Main.calculateInput(condition.elseVal, services, variables)

    def calculateInput(opInput, services, variables):
        if opInput.iType == "variable":
            return variables[opInput.value]
        elif opInput.iType == "operation":
            return Main.executeOperation(opInput.value, services, variables)
        elif opInput.iType == "conditional":
            return Main.handleCondition(opInput.value, services, variables)

    def calculateInputs(inputs, services, variables):
        calculatedInputs = {}
        for opInput in inputs:
            calculatedInputs[opInput.alias] = Main.calculateInput(opInput.inputValue, services, variables)
        return calculatedInputs

    def executeOperation(operation, services, variables):
        inputs = Main.calculateInputs(operation.inputs, services, variables)
        service = services[operation.serviceName]
        if (not Main.checkIfServiceHasRequiredParams(list(inputs.keys()), service)):
            print ("Something went wrong")
            print ("Operation: " + operation.service_name)
            print ("Inputs: ")
            print (inputs)
            exit(1)

        if service.method == "POST":
            jsonData = Main.getJsonDataFromInputDictionary(inputs)
            decodedResponse = Main.jsonPostRequest(service.targetUrl, jsonData)
            return decodedResponse['result']
        




    def start(services, variables, operations):
        results = []
        for operation in operations:
            results.append(Main.executeOperation(operation, services, variables))

        for result in results:
            print(result)



#-------------------------------------------MAIN-------------------------------------#

    def argCheck(args):
        if len(sys.argv) == 1:
            return True
        if args[1] == "-f":
            return False
        return True

    def main():
        dirs = os.listdir( "." )

        args = sys.argv
        useDefault = Main.argCheck(args)
       
        filename = "orchestration.xml"
        
        if not useDefault or (filename not in dirs): 
            filename = input("Please enter the orchestration XML file name which is present in the root directory\n")

        if (not exists(filename)):
            print ("File not found. Exiting")
            exit(1)
        tree = ET.parse(filename)
        root = tree.getroot()
        if root.tag != "orchestration":
            Main.incorrectXMLExit()


        variables = {}
        services = {}
        operations = []
        for child in root:
            if child.tag == "define":
                variables = Main.defineVariables(child)
            if child.tag == "services":
                services = Main.requiredServices(child)
            if child.tag == "operations":
                operations = Main.operations(child)

        Main.start(services, variables, operations)
        

        


if __name__ == "__main__":
    Main.main()