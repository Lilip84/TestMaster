from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def load_test(self):
        self.client.get("/")
        self.client.get("/api/test")