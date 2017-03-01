#!/bin/sh
if [ -z $LIGHT_STEP_ACCESS_TOKEN ]
then
  echo "LIGHT_STEP_ACCESS_TOKEN must be set"
  exit -1
fi
export PYTHONPATH="../../py/"
go run server/main.go --access_token $LIGHT_STEP_ACCESS_TOKEN
