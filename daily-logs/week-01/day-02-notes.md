# Day 2 Notes — K8s Hands-On Learnings


WHAT I DID TODAY

  - Started minikube cluster
  - Ran kubectl get pods --all-namespaces → saw all 7 system pods
  - Deployed nginx with kubectl create deployment → hit ImagePullBackOff
  - Debugged it: minikube VM couldn't reach Docker Hub (DNS timeout)
  - Fixed it: pulled image via Podman, sideloaded into minikube, set imagePullPolicy: Never
  - Scaled deployment to 3 replicas, deleted a pod, watched K8s self-heal
  - Created first YAML manifest (nginx-deployment.yaml) with Deployment + Service
  - Applied it, saw 2 pods running, opened nginx in browser via minikube service
  - Cleaned up everything: deleted deployments, services, stopped minikube


— — —


READING kubectl describe pod

When something breaks, run: kubectl describe pod <pod-name>

It dumps a wall of text. Here's what to actually look at, in priority order:


  #1 — Events (always scroll to the bottom first)

  The timeline of what happened. Scheduling, image pulls, crashes, restarts.
  Your error messages live here. This is where we spotted ImagePullBackOff.
  80% of debugging starts and ends here.

    Events:
      Type     Reason      Age   From              Message
      Normal   Scheduled   26m   default-scheduler Successfully assigned...
      Warning  Failed      26m   kubelet           Failed to pull image "nginx"
      Normal   Started     26m   kubelet           Container started


  #2 — Status + State + Restart Count

    Status:         Running       ← good. "Pending" or "CrashLoopBackOff" = problem
    State:          Running       ← the container itself
    Restart Count:  0             ← high number = your app keeps crashing and restarting


  #3 — Conditions

  Five quick green/red lights:

    PodScheduled:                True   ← was it assigned to a node?
    Initialized:                 True   ← did init containers finish?
    ContainersReady:             True   ← are all containers healthy?
    Ready:                       True   ← can it receive traffic?
    PodReadyToStartContainers:   True   ← is the sandbox ready?

  If any say False, that's your clue.


  #4 — Node + IP

    Node:   minikube/192.168.64.2    ← which machine it's running on
    IP:     10.244.0.8               ← its internal address in the cluster

  Useful when debugging networking or "why is this pod on this node?"


  #5 — Image + Container ID

    Image:   docker.io/library/nginx:latest
    Image ID: docker://sha256:0000f06a...

  Confirms the exact image. Catches "I deployed the wrong version" mistakes.


  Rule: scroll to the bottom first. Events tell you 80% of the story.


— — —


TROUBLESHOOTING: ImagePullBackOff

  What it means:
  K8s tried to download the container image from a registry and failed.
  It backed off and will retry with increasing delays.

  Root cause (our case):
  Minikube's VM couldn't reach Docker Hub. DNS timeout.
  My Mac had internet, but minikube's Linux VM inside it didn't.

  How we found it:
  kubectl describe pod <name> → Events section showed:
    "dial tcp: lookup registry-1.docker.io ... i/o timeout"

  The fix:
  Pulled the image on the host machine and sideloaded it into minikube.

    podman pull docker.io/library/nginx:latest
    podman save docker.io/library/nginx:latest -o /tmp/nginx.tar
    minikube image load /tmp/nginx.tar

  Then told K8s not to try pulling from the internet:

    kubectl patch deployment my-web -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","imagePullPolicy":"Never"}]}}}}'

  Why this matters:
  This is exactly how air-gapped environments work (banks, government, healthcare).
  They never pull from public registries in production. Images are pre-loaded
  into private registries after being scanned for vulnerabilities.


— — —


imagePullPolicy — THREE OPTIONS

  Always        → download the image every time, even if it's already local
  IfNotPresent  → use local copy if it exists, pull only if missing
  Never         → don't pull at all, fail if the image isn't already on the node

  Default behavior:
    - If tag is "latest"    → defaults to Always
    - If tag is specific    → defaults to IfNotPresent (e.g. nginx:1.25)


— — —


SYSTEM PODS — what's running in kube-system namespace

  coredns                  → cluster DNS, translates service names to IPs
  etcd                     → database that stores all cluster state
  kube-apiserver           → front door, everything talks to this
  kube-controller-manager  → self-healing engine, "are we running what we should?"
  kube-proxy               → routes network traffic to the right pods
  kube-scheduler           → decides which node gets each new pod
  storage-provisioner      → minikube-specific, handles local storage volumes

  You never touch these. They're the engine under the hood.
  Your apps go in the "default" namespace.


— — —


COMMANDS TO REMEMBER

  kubectl get pods                          list all pods
  kubectl get pods -w                       watch pods in real time (Ctrl+C to stop)
  kubectl get pods --all-namespaces         see system pods too
  kubectl get deployments                   list deployments
  kubectl get svc                           list services
  kubectl get all                           list everything
  kubectl describe pod <name>              deep info (Events at the bottom!)
  kubectl logs <pod-name>                   see container stdout/stderr
  kubectl scale deployment <n> --replicas=X scale up or down
  kubectl apply -f <file>.yaml              create/update from YAML
  kubectl delete -f <file>.yaml             delete what the YAML created
  kubectl delete pod <name>                 kill a pod (K8s will recreate it)
  minikube image load <file>.tar            sideload an image into minikube
  minikube service <svc-name>               open a service in browser


— — —


THINGS THAT SURPRISED ME

  - K8s self-heals. Delete a pod, it comes right back. It fights to maintain
    the desired state you declared.

  - YAML manifests are the "real" way. Nobody types kubectl create in production.
    Everything is a file, checked into Git. That's GitOps.

  - minikube runs a full Linux VM. That VM has its own network, its own DNS,
    its own container runtime. That's why it couldn't reach Docker Hub
    even though my Mac could.

  - The describe command is the most important tool in the toolbox.
    Not get. Not logs. Describe.


— — —


YAML MANIFEST LESSON

  One YAML file can define multiple resources separated by ---

  Our nginx-deployment.yaml had:
    1. A Deployment (2 replicas of nginx)
    2. A Service (NodePort to expose it)

  Key fields in a Deployment:
    replicas          → how many pods to run
    selector          → how the deployment finds its pods (matchLabels)
    template          → the pod blueprint (what containers to run)
    imagePullPolicy   → Always, IfNotPresent, or Never

  Key fields in a Service:
    type              → ClusterIP (internal), NodePort (external port), LoadBalancer
    selector          → which pods to route traffic to (must match pod labels)
    port              → the service port
    targetPort        → the container port

  Apply:   kubectl apply -f <file>.yaml   (create or update)
  Delete:  kubectl delete -f <file>.yaml  (remove everything in the file)

  This is GitOps — infrastructure defined in files, checked into Git.


— — —


SELF-HEALING DEMO

  Told K8s: I want 3 replicas
    kubectl scale deployment my-web --replicas=3

  Killed one:
    kubectl delete pod <pod-name>

  Immediately checked:
    kubectl get pods → still 3 pods

  K8s noticed one died and instantly replaced it.
  It will always fight to match the desired state you declared.


— — —


WHAT CONFUSED ME

  - Basic thing, like happens under the hood when we get the `ImagePullBackOff` error.

 - What concerning factors to look with the `kubectl describe pod` command. 

WHAT I WANT TO EXPLORE NEXT

  - How k8 can be complicated as I dug deeper and learn more about it. 
