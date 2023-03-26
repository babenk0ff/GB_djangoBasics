import os

from locust import HttpUser, task

SERVER_IP_ADDR = os.getenv('SERVER_IP_ADDR', '127.0.0.1')


class LoadTestingBraniacLMS(HttpUser):
    @task
    def test_some_pages_open(self):
        # Mainapp
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/courses_list/')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/courses/1/detail/')
        # Authapp
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/register/')
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/login/')
