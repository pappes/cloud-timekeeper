#! /usr/bin/bash

zip -r get_remaining_time.zip lambdas/function/get_remaining_time.py requirements.txt

gcloud functions deploy get_remaining_time \
    --runtime python312 \
    --trigger-http \
    --memory 128MB \
    --region australia-southeast1 \
    --source get_remaining_time.zip



zip -r set_remaining_time.zip lambdas/function/set_remaining_time.py requirements.txt

gcloud functions deploy set_remaining_time \
    --runtime python312 \
    --trigger-http \
    --memory 128MB \
    --region australia-southeast1 \
    --source set_remaining_time.zip

