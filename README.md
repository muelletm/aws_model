# aws_model

Deploy a model via AWS beanstalk

# Install dependencies

pip install -r requirements.txt

# Train the model

```console
python -m train_model
```

# Create package

```console
python -m create_package
```

# Deploy in AWS

First we create a new environment in AWS beanstalk.

![beanstalk logo](docs/images/beanstalk_logo.png)

![tier](docs/images/tier.png)

![platform](docs/images/platform.png)

![appliction code](docs/images/application_code.png)

Now wait for the environment to become available.

# Start Demo

```console
export ENDPOINT_URL="http://sentiment-env.eba-hviumu6m.eu-central-1.elasticbeanstalk.com"
streamlit run app.py
```

![demo](docs/images/demo.png)
