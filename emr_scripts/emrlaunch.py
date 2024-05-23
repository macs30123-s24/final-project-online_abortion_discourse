
'''
aws emr create-cluster \
--name "Spark NLP 5.3.3" \
--release-label emr-6.2.0 \
--applications Name=Hadoop Name=Spark Name=Hive Name=JupyterHub \
--instance-type m4.xlarge\
--instance-count 4 \
--use-default-roles \
--log-uri "s3://131313113finalproject/" \
--bootstrap-actions Path="s3://131313113finalproject/setup.sh",Name=custom \
--configurations file://~/desktop/30123/project/emr_scripts/sparknlp-config.json \
--ec2-attributes '{"KeyName": "vockey2"}' --region us-east-1\
'''

# after cluster is launched:
# sudo pip3 install --upgrade pip
# sudo python3 -m pip install pandas seaborn matplotlib wordcloud

'''
ssh -i ~/.aws/vockey2.pem -NL 9443:localhost:9443 hadoop@ec2-34-230-23-74.compute-1.amazonaws.com
https://localhost:9443
'''

# when there are issues with the cluster or server:
# cd /var/log/livy
# sudo systemctl stop livy-server
# sudo systemctl status livy-server
# sudo systemctl start livy-server
# sudo systemctl restart livy-server

# ways to check the status of the cluster:
# top
# free -h
