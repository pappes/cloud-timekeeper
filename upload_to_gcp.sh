#! /usr/bin/bash

gcloud functions deploy get_remaining_time \
    --gen2 \
    --allow-unauthenticated \
    --runtime python312 \
    --trigger-http \
    --memory 128Mi \
    --region australia-southeast1 \
    --source lambdas/function


gcloud functions deploy set_remaining_time \
    --gen2 \
    --allow-unauthenticated \
    --runtime python312 \
    --trigger-http \
    --memory 128Mi \
    --region australia-southeast1 \
    --source lambdas/function
