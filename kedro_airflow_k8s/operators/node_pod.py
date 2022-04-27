"""
Module contains Apache Airflow operator that creates k8s pod for execution of
kedro node.
"""

import uuid
from typing import List, Dict, Optional

from airflow.contrib.kubernetes.pod_generator import PodGenerator
from airflow.contrib.operators.kubernetes_pod_operator import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s


class NodePodOperator(KubernetesPodOperator):
    """
    Operator starts pod with target image with kedro projects and executes one node from
    the pipeline. This class simplifies creation of pods by providing convenient options.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        node_name: str,
        namespace: str,
        image: str,
        image_pull_policy: str,
        env: str,
        task_id: str,
        pipeline: str = "__default__",
        pvc_name: Optional[str] = None,
        startup_timeout: int = 600,
        volume_disabled: bool = False,
        volume_owner: int = 0,
        mlflow_enabled: bool = True,
        requests_cpu: Optional[str] = None,
        requests_memory: Optional[str] = None,
        limits_cpu: Optional[str] = None,
        limits_memory: Optional[str] = None,
        node_selector_labels: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        tolerations: Optional[List[Dict[str, str]]] = None,
        annotations: Optional[Dict[str, str]] = None,
        source: str = "/home/kedro/data",
    ):
        """

        :param node_name: name from the kedro pipeline
        :param namespace: k8s namespace the pod will execute in
        :param pvc_name: name of the shared storage attached to this pod
        :param image: image to be mounted
        :param image_pull_policy: k8s image pull policy
        :param env: kedro pipeline configuration name, provided with '-e' option
        :param pipeline: kedro pipeline name, provided with '--pipeline' option
        :param task_id: Airflow id to override
        :param startup_timeout: after the amount provided in seconds the pod start is
                                timed out
        :param volume_disabled: if set to true, shared volume is not attached
        :param volume_owner: if volume is not disabled, fs group associated with this pod
        :param mlflow_enabled: if mlflow_run_id value is passed from xcom
        :param requests_cpu: k8s requests cpu value
        :param requests_memory: k8s requests memory value
        :param limits_cpu: k8s limits cpu value
        :param limits_memory: k8s limits memory value
        :param node_selector_labels: dictionary of labels to be put into pod node selector
        :param source: mount point of shared storage
        """
        self._task_id = task_id
        self._volume_disabled = volume_disabled
        self._pvc_name = pvc_name
        self._mlflow_enabled = mlflow_enabled

        super().__init__(
            name=task_id,
            task_id=task_id,
            security_context=self.create_security_context(
                volume_disabled, volume_owner
            ),
            namespace=namespace,
            image=image,
            image_pull_policy=image_pull_policy,
            arguments=[
                "kedro",
                "run",
                "-e",
                env,
                "--pipeline",
                pipeline,
                "--node",
                node_name,
            ],
            volume_mounts=[
                k8s.V1VolumeMount(mount_path=source, name="storage")
            ]
            if not volume_disabled
            else [],
            resources=self.create_resources(
                requests_cpu, requests_memory, limits_cpu, limits_memory
            ),
            startup_timeout_seconds=startup_timeout,
            is_delete_operator_pod=True,
            config_file=self.minimal_pod_template,
            node_selectors=node_selector_labels,
            labels=labels,
            tolerations=tolerations,
            annotations=annotations
        )

    @staticmethod
    def create_resources(
        requests_cpu, requests_memory, limits_cpu, limits_memory
    ) -> k8s.V1ResourceRequirements:
        """
        Creates k8s resources based on requests and limits
        :param requests_cpu:
        :param requests_memory:
        :param limits_cpu:
        :param limits_memory:
        :return:
        """
        resources = {}
        if requests_cpu:
            resources["request_cpu"] = requests_cpu
        if requests_memory:
            resources["request_memory"] = requests_memory
        limits = {}
        if limits_cpu:
            resources["limit_memory"] = limits_cpu
        if limits_memory:
            resources["limit_cpu"] = limits_memory
        return resources

    @property
    def minimal_pod_template(self):
        """
        This template is required since 'volumes' arguments are not templated via direct
        API nor passing xcom values in pod definition.
        :return: partial pod definition that should be complemented by other operator
                parameters
        """
        minimal_pod_template = f"""
apiVersion: v1
kind: Pod
metadata:
  name: {self._task_id}.{uuid.uuid4().hex}
spec:
  containers:
    - name: base
      env:
"""
        if self._mlflow_enabled:
            minimal_pod_template += """
        - name: MLFLOW_RUN_ID
          value: {{ task_instance.xcom_pull(key="mlflow_run_id") }}
"""
        if not self._volume_disabled:
            minimal_pod_template += f"""
  volumes:
    - name: storage
      persistentVolumeClaim:
        claimName: {self._pvc_name}
"""
        return minimal_pod_template

    @staticmethod
    def create_security_context(
        volume_disabled: bool, volume_owner: int
    ) -> Dict[str, str]:
        """
        Creates security context based on volume information
        :param volume_disabled:
        :param volume_owner:
        :return:
        """
        return (
            {fs_group: volume_owner}
            if not volume_disabled
            else {}
        )
