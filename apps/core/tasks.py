from celery import shared_task

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_order_notification(self, order_id: int):
    # Demo placeholder. Integrate a real email provider in a verified environment.
    return {"order_id": order_id, "status": "queued"}
