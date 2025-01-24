# sample-maven-project
sample maven project

# Jenkins-SetUp
You will need to configure Maven as a global build tool.
In the Jenkins web interface, go to:
Manage Jenkins -> Tools -> Maven installations -> Add Maven.
Use Maven version as 3.5.4
Select the Save button.

# Setting up the Jenkins Job
Create a freestyle job and configure it as follows:

Under Source Code Management, select Git and enter the following URL:
https://github.com/rashuchatla/sample-maven-project
MAKE SURE TO SET THE Branch Specifier to */main.

# Build Steps

1. Add a build step using Invoke Top-Level Maven Target.
Select the Maven version you configured in the previous step.
For the goal, enter package

2. Select Add build step -> Execute shell.
   Enter: java -jar target/gs-maven-0.1.0.jar

Save the job and start the build.




