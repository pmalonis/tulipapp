### Set up sagemaker endpoint
The Sagemaker endpoint that serves the Llama 2 model is relatively expensive, so you may not want it running all the time. To start the endpoint, take the following steps:

* Go to the AWS console.
* Open the "Services" menu in the upper left corner and select Sagemaker.
* On the left side, select Domains.
* Select llama-endpoint.
* Under User profiles, there should be one profile.
* Delete any old endpoint configurations. Go to the menu on the left side, expand the Inference section and select Endpoint configurations. Delete any configurations for the llama-2-7b-chat model.
* Click the Launch button to the right of the user profile, then select Studio. A Sagemaker Studio JupyterLab tab should open.
* In the Sagemaker Studio tab, under SageMaker JumpStart on the left side, select "Models, notebooks, solutions."
* Search for the Llama-2-7b-chat model and select it.
* Click deploy. Deploying the model will take several minutes.
* Verify that the endpoint is in service. Go to the menu on the left side, expand the Inference section and select Endpoints to see a list of endpoints currently in service.

Also see the Medium post [How to use Llama 2 with an API on AWS to power your AI apps](https://archive.is/0ISPh).

To stop the endpoint, go to the endpoint console as in the last step above, and delete the endpoint that is in service.

### Rebuilding elastic beanstalk environment

The app is hosted on the AWS Elastic Beanstalk service.

When the app has not been in use for serveral days, the Elastic Beanstalk service may enter a "Suspended" state. You can check this by going to the AWS console, opening the Services menu in the upper left corner, selecting Elastic Beanstalk, selecting Environments in the left side menu, and checking the status for the environment "tulipapp3-dev."

If the environment status is Suspended, you can rebuild the environment using the following steps:

* Go to the AWS console.
* Open the "Services" menu in the upper left corner and select Elastic Beanstalk.
* Select Environments in the left side menu.
* Select the environment "tulipapp3-dev".
* Under the Actions menu, select Rebuild Environment.


### Deploying to Elastic Beanstalk

This section describes how to build the Elastic Beanstalk envirnoment from source. Make sure to delete the old Elastic Beanstalk environments before completing these steps.

Install the Elastic Beanstalk Command Line Interface: https://github.com/aws/aws-elastic-beanstalk-cli-setup.


cd to the repository root directory, and enter the following commands:

```
	eb init
```
If you haven't yet added your aws key to the command line interface, you will need to do so for this command to work. 

You also may encounter the following error:

```
	Signature expired: 20230803T224417Z is now earlier than 20230803T233030Z (20230803T233530Z - 5 min.)
```	

```
	sudo ntpdate ntp.ubuntu.com
```

When prompted with 
```
	"Continue with codecommit?"
```
Select "no."


Next, create the Elastic Beanstalk environment, using the following command:

```
	eb create
```
Select the default options for every prompt. Select no spot fleet requests.
	

The environment will then be created.

Next, you need to enable communicating with the app through https, in order for the Carrd site to access it. Complete the following steps:

* Go the AWS Elastic Beanstalk console and select the environment
* In the left side menu, select "Configuration" 
* Under "Instance traffic and scaling" section, click "Edit"
* Under "Listeners," click "Add listener"
* For "Listener port," use 443
* Under listener protocal, select https
* Under "SSL certificate" select the certificate beginning with *dataarticles
* Click "Save"

Then wait for the configuration to update.


### Adding new datasets

The code for finetuning the TCube model and segmenting the temperature anomaly dataset is in TCube/Train-Predict-Temp.ipynb. This code can be modified to add a new dataset.