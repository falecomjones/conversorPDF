#!/bin/bash
((i = 0));

bucket=$BUCKET
awsid=$AWSID
awssecret=$AWSSECRET
region=$REGION
fileoutput=$FILEOUTPUT

#while IFS='=' read key value; do
 #   case "$key" in
 #  bucket)
#        bucket=$value
#    ;;
#    awsid)
#       awsid=$value
#    ;;
#    awssecret)
#        awssecret=$value
#    ;;
#    region)
#        region=$value
#    ;;
#    fileoutput)
#	fileoutput=$value
#    ;;
#esac
#done < <(sed 's/\s\+:\s\+/:/' /bin/parametros)
#	echo $bucket
#	echo $awsid
#	echo $awssecret
#	echo $region
#	echo $fileoutput

cd /bin

PYTHONPATH='.' luigi --module primeiro MyTask --bucket $bucket --awsid $awsid --awssecret $awssecret --region $region --fileoutput $fileoutput

#while IFS='=' read b aws secret reg file; do
#	bucket="${b}"
#	awsid="${aws}"
#	awssecret="${secret}"
#	region="${reg}"
#	fileoutput="${json}"
#	echo $bucket
#	echo $awsid
#	echo $awssecret
#	echo $region
#	echo $fileoutput
#done <  parametros
