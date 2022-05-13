from kubernetes.client.rest import ApiException
from kubernetes import client, config
from helper import generate_pod_logs_html, get_pods_from_namespace
import json
import webbrowser
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-n','--namespace', type=str,\
  required=False, help='Specify the namespace of the pods',
  default='default')

parser.add_argument('-l', '--labels', type=json.loads,\
  required=False, help=f"""
    Specify labels of pods (specify a dictionary as string)
    Ex: \'{{"example_label":"example_value"}}\'
  """,\
  default={}
)

try:
  args = parser.parse_args()
except:
  print('Arguments not provided correctly')
  sys.exit(1)

config.load_kube_config()


try:
    api_instance = client.CoreV1Api()

    pods_list = get_pods_from_namespace(api_instance, 'default', {'app': 'test'})

    for pod in pods_list:
      api_response = api_instance.read_namespaced_pod_log(name=pod, namespace='default')
      generate_pod_logs_html(pod, api_response.split('\n'))
      webbrowser.open_new_tab(f"{pod}.html")

except ApiException as e:
    print('Found exception in reading the logs')