# AWS Model Deployment

Deploy a [Tensorflow Serving](https://www.tensorflow.org/tfx/guide/serving) model via [AWS beanstalk](https://aws.amazon.com/elasticbeanstalk/).

# Install dependencies

(Run this from an environment such as conda.)

```console
pip install -r requirements.txt
```

# Train the model

Train a 5-star rating classifcation model on Amazon product reviews.

```console
python -m train_model
```

# Create version zip archive

This archive will contain the trained model as well as our deployment configuration files.

```console
python -m create_package
```

# Deploy in AWS

Navigate to http://aws.amazon.com/ and open the AWS console.

First we create a new environment in AWS beanstalk.

![beanstalk logo](docs/images/beanstalk_logo.png)

We will select the web server environment.

![tier](docs/images/tier.png)

We use the docker platform.

![platform](docs/images/platform.png)

We upload the previously created version archive.

![appliction code](docs/images/application_code.png)

Now wait for the environment to become available.
This can take up to 10 minutes.

Once it's up we can navigate to the instance and the page should show:

```
Sentiment Model Server
```

# Start Demo

Now we can start our demo server locally and make calls to the deployed model.

# Define a variable with our endpoint URL

**Impotant:** We will have to change the URL below to match our instance.

### Linux / bash

```bash
export ENDPOINT_URL="http://sentiment-env.eba-hviumu6m.eu-central-1.elasticbeanstalk.com"
```

### Windows

```bash
set ENDPOINT_URL="http://sentiment-env.eba-hviumu6m.eu-central-1.elasticbeanstalk.com"
```

## Start streamlit

```bash
streamlit run app.py
```

![demo](docs/images/demo.png)
