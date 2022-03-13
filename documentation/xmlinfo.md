# MiniProject SOA

## XML Info

The Mini SOA tool relies on a python3 script that reads a custom XML schema which describes how to orchestrate the different services on the local network. By default the script will look for a file named `orchestration.xml`. If this is not present or the `-f` option is used at start, the script will ask for a specific file name.

## Schema

### Orchestration

The schema starts and ends with the `<orchestration></orchestration>` tags. All details of the deisred application must be inside these tags.

### Services

For the orchestration to work the script must be aware of what services are available. For this reason all required services for a given orhestration are given within the `<services></services>` tags. 

**Service**

The `<service></service>` tags describe a single service as the name suggest. It requires the following tags as children:

- `<name></name>:` A unique name that the script will assign to the service.
- `<target_url></target_url>:` The URL which the service is available at
- `<method></method>:` The HTTP method required by the service. As of now it is either `GET` or `POST`
- `<parameters></parameters>:` A list of parameters that the service requires in the request body 

**Parameter**

The `<parameter></parameter>` tags describe a single input to a service. They require the following children tags to be present:

- `<name></name>:` The name of the parameter, which corresponds to the web service's required parameter name. 
- `<type></type>:` The type of the parameter. As of now it can be `string`, `int` or `float`

### Variables

To allow for user entered variables the orchestration XML schema allows for declaration of any number of input variables. These should be placed within the `<variables></variables>` tags.

**Variable**

The `<variable></variable>` tags describe a single user input variable to the python script. They require the following children tags to be present:

- `<name></name>:` The unique name of the variable. 
- `<type></type>:` The type of the variable. As of now it can be `string`, `int` or `float`

### Operations

Operations are the core part of the MiniProject SOA toolkit. An operation is a single request to one of the available services. An operation must consist of a service, and any number of inputs (even 0 in the case of a `GET` type service). Operations in this schema must be declared in reverse order, for example if the last operation is a division, that has to be declared first. Operations live between the `<operations></operations>` tags.

**Operation**

A single operation is described by the `<operation></operation>` tags. Within the operation the following children should be present:

- `<servince_name></service_name>:` This tag refers to the unique service name given to a service in the `Service` schema
- `<inputs></inputs>:` A list of inputs to the service. This can be ommited if the service doesn't require any input.

### Inputs

As mentioned earlier in this document, the `Operations` require inputs. Inputs are descirbed within the `<inputs></inputs>` tags. As this is a list they can have any number if input instances.

**Input**

A single input is described with the `<input></input>` tags. They need the following children:

- `<alias></alias>:` The name of the input referring to what the web service requires as its input.
- `<value></value>:` The value of the input

**Value** 

The value of an input is described in the `<value></value>` tag pair. The details can be of three type:

- `Variable:` This is described in the `<i_variable></i_variable>` tags. Its content should refer to a user defined variable in the variables section
- `Operation:` An operation input is an `<operation></operation>` tag pair. Such operations are nested and their ouput is used as the input.
- `Conditional:` As the name suggest it is a conditional value. It is described in the next section

**Conditional**

The conditional value lives in the `<conditional></conditional>` tag pairs. The children in this should be the following:

- `<compare_value></compare_value>:` This is the value the expression has to be evaluated against. This has the same three type as the `Value` above
- `<condition></condition>:` A boolean condition expression (eg. `> 7`)
- `<then></then>:` The result when the condition is true
- `<else></else>:` The result when the condition is false

**Result**

Within the `<then></then>` and `<else></else>` tags there should be a `<result></result>` tag which should contain a `Value` that can be of the three value types.




