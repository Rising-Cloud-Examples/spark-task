# spark-task
This guide will walk you through the simple steps needed to build and run an Apache Spark app on Rising Cloud.

# 1. Install the Rising Cloud Command Line Interface (CLI)
In order to run the Rising Cloud commands in this guide, you will need to install the Rising Cloud Command Line Interface. This program provides you with the utilities to setup your Rising Cloud Task or Rising Cloud Web Service, upload your application to Rising Cloud, setup authentication, and more. If you haven’t already, [click here](/docs/install) to for instructions to install Rising Cloud CLI.

# 2. Login to Rising Cloud Using the CLI
Using a command line console (called terminal on Mac OS X and command prompt on Windows) run the Rising Cloud login command. The interface will request your Rising Cloud email address and password.

```risingcloud login```

# 3. Initialize Your Rising Cloud Task

Create a new directory to place your project files in, then open this directory with your command line.

Using the command line in your project directory, run the following command replacing $TASK with your unique task name.

Your unique task name must be at least 12 characters long and consist of only alphanumeric characters and hyphens (-). This task name is unique to all tasks on Rising Cloud. A unique URL will be provided to you for sending jobs to your task.

If a task name is not available, the CLI will return with an error so you can try again.

```risingcloud init -s $TASK_URL```

This creates a **risingcloud.yaml** file in your project directory. This file can be used to configure the build script.

# 4. Configure your Rising Cloud Task

Configure your risingcloud.yaml

**TIP:** This guide demonstrates a basic installation of PySpark using pip. If your application is based in R, Java, or Scala, it will require different steps to install. Visit their website [here](https://spark.apache.org/docs/latest/) to read about other installation methods.

In the previous step, a risingcloud.yaml file should have generated in your project directory. Open that file and change the deps stage to:

```
deps: 
- apt update && apt upgrade -y
- apt install openjdk-11-jdk -y
- export JAVA_HOME=/usr/lib/jvm/openjdk-11-jdk-amd64
- apt install -y python3-pip
- pip3 install pyspark
```

And change the run step to:

```run: python3 my_script.py```

**Create Your Program**

For this example, we will modify the Pi Estimation example program provided by Apache Spark, and use as a Rising Cloud Task. This app will read the “samples” field from a JSON request, and return its Pi approximation in the “pi” field in a JSON response.

Create a new file in your project directory named **my_script.py**.  Paste the following into your new file and save.

```
import json
import random
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PiApproximator").getOrCreate()

request = {}
with open("request.json", 'r') as f:
    request = json.load(f)

NUM_SAMPLES = request["samples"]

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)) \
             .filter(inside).count()
response = {"pi": (4.0 * count / NUM_SAMPLES)}

with open("response.json", 'w+') as f:
    json.dump(response, f)
```


# 6. Build and Deploy Your Rising Cloud Task
Use the push command to push your updated risingcloud.yaml to your Task on Rising Cloud.

```risingcloud push```

Use the build command to zip, upload, and build your app on Rising Cloud.

```risingcloud build```

Use the deploy command to deploy your app as soon as the build is complete.  Change $TASK to your unique task name.

```risingcloud deploy $TASK```

Alternatively, you could also use a combination to push, build and deploy all at once.

```risingcloud build -r -d```

Rising Cloud will now build out the infrastructure necessary to run and scale your application including networking, load balancing and DNS.  Allow DNS a few minutes to propogate and then your app will be ready and available to use!

# 6. Queue Jobs for Your Rising Cloud Task

**Send jobs to your new app**

- Log into your Rising Cloud Team: <u>[https://my.risingcloud.com/](https://my.risingcloud.com/)</u>
- Select your task from the Dashboard.
- Click on Jobs in the left menu.
- Click New Job Request.  
- Send a blank request to your task, leave the curly brackets.

```{"status": 10000}```

Rising Cloud will take a few moments to spin-up your app, and proces your request.  In the future it will learn from the apps usage patterns to anticipate usage, making instances available in advance of need, while also spinning down instances when not needed.  

Click the twisty to open up your Job, and then click Arguements to see your Pi output

```^```

**Alternatively** you can use an API testing tool such as Postman or Insomnia

POST HTTP request, choose body type JSON:

```https://<your_task_url>.risingcloud.app/risingcloud/jobs```

Within the body of the POST type and SEND: 

```{"status": 10000}```

This should yield an HTTP response with a body that looks like:

```{“jobId”: “<id of job>”}```

To get the results of the job, make a GET HTTP request to your task:

```https://<your_task_url>.risingcloud.app/risingcloud/jobs/<id of job>```

should cause the “result” field in a completed Job Status to be similar to:

```
{
    "pi": 3.1232
}
```

Congratulations, you’ve successfully used Apache Spark on Rising Cloud!
