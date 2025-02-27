#!/usr/bin/env python
"""
Performs basic cleaning on the data and saves the results in weights and Biases
"""
import argparse
import logging
import wandb
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact

    logger.info(f"Downloading artifact : {args.input_artifact}")
    artifact = run.use_artifact(args.input_artifact)
    artifact_local_path = artifact.file()

    ######################
    # YOUR CODE HERE     #
    ######################

    df = pd.read_csv(artifact_local_path)

    logger.info("Dropping outliers")

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()


    logger.info("convert last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("save updated dataframe")
    df.to_csv(args.output_artifact, index=False)

    logger.info(f"Logging artifact to W&B : {args.output_artifact}")
    artifact = wandb.Artifact(
        name = args.output_artifact,
        type = args.output_type,
        description = args.output_description
    )
    artifact.add_file(args.output_artifact)

    run.log_artifact(artifact)
    logger.info(f"artifact logged in W&B : {args.output_artifact}")

    logger.info(f"removing the local copy of the output artifact : {args.output_artifact}")
    os.remove(args.output_artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact, generated from the script",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="type of the output artificat produced",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int,
        help="minimum price, to filter the data",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=int,
        help="Maximum price to filter the data",
        required=True
    )


    args = parser.parse_args()

    go(args)
