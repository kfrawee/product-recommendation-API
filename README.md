## Overview

In this assignment, you are asked to **build a REST API around a machine learning model that recommends banking products**. It is based on a solution to a Kaggle competition: the model is already engineered for you, you just need to run the training script to obtain the trained model, and then your work focuses on building from scratch an API that serves this model. Some bonus tasks to further test your API design and devops skills are also included.

## Goal

The goal of this assignment is for us to assess your API building skills, and the tasks in this assignment mirror the kind of work you would be doing at Genify as an Engineer. For example:

- Inherit the work of a Data Scientist, with some but for sure incomplete explanations on the model built
- Build a system with little specifications, but instead some business needs for you to enquire/think about and translate into system requirements
- Leverage some slightly messy references to earlier work
- Have limited opportunities to interact with the rest of the team given everyone’s time is precious

## Context on the problem

What this model solves relates to a sub-product of Genify. It helps banks recommend the right banking product (loan, deposit, credit card, etc.) to the right client at the right time. How these recommendations are delivered is equally important. Here, to do so, we opt for a REST API, and your task is to build it!

## How to run:
- Clone the repository:
    ```sh
    git clone https://github.com/kfrawee/product-recommendation-API
    ```
- Install requirements:
    ```sh
    pip install -r requirements.txt
    ```

- Train the model:
    - Navigate to `app\api\ml_models`.
    - After downloading and extracting the data to `data` directory. *Check `README.md` for guidance*
    - Run `train.py` to train and save the trained model to `output` directory.
- Run the server:
    ```sh
    python run.py
    ```
- Import Postman collection from `docs` directory to test the API.
- View the OpenAPI specefications by importing the swagger file under `docs` directory using [swagger editor](https://editor-next.swagger.io/).
- **NOTE:** Some endpoints are protected ( i.e. `DELETE /predict/<invocation_id>`, `GET /predict/`)
    - To create an Admin user and get a Bearer token, run:
        ```sh
        sh scripts/get-token-dev.sh
        ```
    - Add the token to the request headers.

You can use Docker Container:
- Build:
    ```sh
    docker build -t genify-api .
    ```
- Run:
    ```sh
    docker run -d -p 8080:8080 genify-api
    ```
- Or run:
    ```sh
    sh scripts/build-run-image.sh
    ```

---
## References
[1] overview of problem (Kaggle competition): [https://www.kaggle.com/c/santander-product-recommendation/overview](https://www.kaggle.com/c/santander-product-recommendation/overview)

[2] data (Kaggle competition): [https://www.kaggle.com/c/santander-product-recommendation/data](https://www.kaggle.com/c/santander-product-recommendation/data)

[3] reference Kaggle notebook: [https://www.kaggle.com/sudalairajkumar/when-less-is-more](https://www.kaggle.com/sudalairajkumar/when-less-is-more)

[4] details on ref. code: [https://www.kaggle.com/c/santander-product-recommendation/discussion/25579](https://www.kaggle.com/c/santander-product-recommendation/discussion/25579)

[5] Genify recommender system demo: [https://web.archive.org/web/20220524164933/https://jpweng.pythonanywhere.com/en/recosysdemo](https://web.archive.org/web/20220524164933/https://jpweng.pythonanywhere.com/en/recosysdemo)

[6] Genify PFM API: [https://docs.pfm.genify.ai/pfm-suite/v1/transaction-data-api](https://docs.pfm.genify.ai/pfm-suite/v1/transaction-data-api)