from locust import HttpUser, task, between


class LoadTest(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def predict_with_no_batch(self):
        request_body = {
            "sentence": "This story is really amazing!"
        }
        
        self.client.post(
            url="http://34.47.86.49/inference",
            json=request_body
        )