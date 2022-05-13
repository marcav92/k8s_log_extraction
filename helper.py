from bs4 import BeautifulSoup
from kubernetes.client.rest import ApiException


def compare_labels(input_labels, pod_labels):
  """Compares 2 dictionaries a removes default pod-template-hash label
  :param input_labels: label dictionary provided by the user
  :type: dict
  :param pod_labels: labels taken from kubernetes api response
  :type dict

  :return: if whether or not dictionaries are equal
  :rtype: boolean
  """

  pod_labels.pop('pod-template-hash')
  return input_labels == pod_labels

def get_pods_from_namespace(api_instance, namespace, labels={}):
  """Returns a string list of pods names that match that exist in provided
  namespace and whose labels match with the labels provided by the user

  :param api_instance: CoreV1Api instance
  :param namespace: the namespace that holds the pods whose logs will be extracted
  :param labels: dictionary

  :return: a list of strings with the pods names that were found
  :rtype: list[str]
  """
  try:
    pods_list = api_instance.list_namespaced_pod(namespace=namespace).to_dict()['items']

    if pods_list:
      if labels:
        return [pod['metadata']['name'] for pod in pods_list if compare_labels(labels, pod['metadata']['labels'])]
      else: 
        return [pod['metadata']['name'] for pod in pods_list]
    else:
      print('No Pods Found!')
      return []

  except ApiException as e:
    print(f"API Exception: {e}")

def generate_pod_logs_html(pod_name, logs_list):
  """This function takes a list of strings with the logs of a pod and converts it into a
  nice looking html file that will nicely show the logs in the a browser

  :param pod_name: This is the pod for which the file will be generated
  :param logs_list: strinmg list with the lines of the logs that were received from k8s api
  """
  soup =  BeautifulSoup(open('index.html'), 'html.parser')
  pod_name_html = f"""
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">
            Pod {pod_name} logs
          </h4>
        </div>
      </div>
    """
  soup.body.append(BeautifulSoup(pod_name_html, 'html.parser'))
  for idx, log in enumerate(logs_list):
    if log == '':
      continue
    log_html = f"""
      <div class="card">
        <div class="card-body">
          {idx} - {log}
        </div>
      </div>
    """
    soup.body.append(BeautifulSoup(log_html, 'html.parser'))

  with open(f"{pod_name}.html",'w') as file:
    file.write(str(soup))
