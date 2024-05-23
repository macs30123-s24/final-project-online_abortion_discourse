# setup.sh
set -x -e

# Install Java
sudo yum install -y java-1.8.0-openjdk-devel

# Set environment variables
echo -e 'export PYSPARK_PYTHON=/usr/bin/python3
export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_JARS_DIR=/usr/lib/spark/jars
export SPARK_HOME=/usr/lib/spark' >> $HOME/.bashrc && source $HOME/.bashrc

# Install necessary Python packages
sudo python -m pip3 install awscli boto spark-nlp 

set +x
exit 0
