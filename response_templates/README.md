## Splunk OAR Response Plans
Our response templates for Splunk PS are based in yaml so that we can quickly capture in a human readable format with the customer.  We also will have a respository of tasks that we can quickly reuse for building custom response templates for customer out of band and then quickly process them into the product configuration.  We will provide reusable content that internal, partners and customer teams can use.  This process is flexible and will allow teams to quickly creat not only response templates for automation, but also for internal process documentation.
***
The Splunk OAR products have several components to make this content work in the UI and create it by hand. This project is using this basic structure to form the templates to be able to create additional documentaitonal products: 
Use Case Template, Phase, Task
### Response Templates
* The response template is the base and holds the phase for the response generally we follow the PICERL model developed by SANS and also aligns with the NIST 800-61R2 process but not exactly.
* Naming conventions is the use case that you are putting together. (e.g. Phishing Investigation)

**These response templates should have the Use case and the phases needed to bring the appropriate tasks for the use case**
The response should be located in the directory.

***
### Response Phase Templates
* The response phase templates organize the response tasks around phase and provides SLA mondular use cases
* Naming convention should map to a familar workflow phase processes like 

NIST 800-61r2, PICERL, custom built (e.g. vulnerability) and Information Technology . The following phase workflows have been built for you.
[PICERL](https://www.sans.org/reading-room/whitepapers/incident/incident-handlers-handbook-33901) | [NIST-61r2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf) | [Splunk](https://static.rainfocus.com/splunk/splunkconf18/sess/1522584681091001dUJr/finalPDF/SEC1233_HackingYourSOEL_Final_1538424831880001SlPY.pdf) | [Custom](https://www.us-cert.gov/sites/default/files/c3vp/crr_resources_guides/CRR_Resource_Guide-VM.pdf) | [IT](https://wiki.en.it-processmaps.com/index.php/Incident_Management)
----------          | ----------                 | ----------          | ----------         | ----------
P01 Preparation     | N01 Preparation            | SP01 Ingestion      | SP11 Training      | IT01 Incident
P02 Investigation   | N02 Detection              | SP02 Investigation  | SP12 Assessment    | IT02 Problem
P03 Containment     | N03 Analysis               | SP03 Contain        | SP13 Record        | IT03 Root Cause
P04 Eradication     | N04 Containment            | SP04 Notify         | SP14 Prioritize    | IT04 Workaround
P05 Recovery        | N05 Eradication & Recovery | SP05 Document       | SP15 Mitigate      | IT05 Change
P06 Lessons Learned | N06 Post-Incident          | ---                 | SP16 Effectiveness | IT06 Revision
---                 | ---                        | ---                 | SP17 Root Cause    | --- 

**Response phases should call out the phases and the tasks assigned to each phase as a modudular Phase-Task function.**
The response phases should be located in ```./response_template/response_phases/```

### Response Task Templates
* The response task is the direct action the analyst or responder needs to acocmplish as part of this process and has actions and playbooks assigned for automation support
The Response Task should be named RT + Phase ### + Task ## <name of the task> (e.g. TA0101 Practice your training)
  
**These tasks should include the actions and/or playbooks that help the customer align this work with their achievable task.**
The response tasks should be located in ```./response_template/response_tasks/```
  
Inspiration and similarites from this repo and project have been derived from the Atomic Red Team project - Atomic Threat Coverage - ATC RE&CT project: https://github.com/atc-project/atc-react. If you are using this project, you can share some of your capabilties in the same way.  This repo was built specifically to support Splunk OAR products
