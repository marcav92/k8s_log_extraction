# sysdig_test

## The script that I made

The script is called [extract_logs.py](extract_logs.py), to run the script you will
need to first install it's dependencies with:

```
pip3 install -r requirements.txt -t .
```

After that make sure that you have a running deployment in your target cluster, you can use
[test_deployment.yaml](test_deployment.yaml) to create a deployment of ngingx.

Once you have created your deployment, you can use the script like this:

```
python3 extract_logs.py --namespace 'default' --labels '{"app":"test"}'
```

The script is using argparser so in case you have any doubts about it's arguments you can use:

```
python3 extract_logs.py -h
```

## Implementation procedure

commands used:

After I installed minikube and bootstrapped a k8s cluster I used [test_deployment.yaml](./test_deployment.yaml), to create an nginx deployment. For that I used:

```
kubectl apply -f ./test_deployment.yaml
```

I then exposed the pods of this deployment using the following command:

```
kubectl expose deployment test --name my-nginx-service --port 8080 --target-port=80 --type NodePort
```

After that to generate some fake traffic I used:
To find out nodes ip

```
kubectl get nodes -o wide
```

To find the node port

```
kubectl get svc -l app=test
```

# with more time I would add:

- A way better frontend: I would create a whole dashboard that could somehow
  show all the pods and would allow to choose which pod logs I want to see.

- I could turn this script into package that would include all the logic necessary
  to spawn a local server to show the dashboard.
