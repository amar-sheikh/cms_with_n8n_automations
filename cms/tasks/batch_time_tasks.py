from celery import shared_task
from datetime import datetime, timedelta

@shared_task
def generate_batch_times_task(batch_slot_id):
    from cms.models import BatchSlot, BatchTime

    try:
        slot = BatchSlot.objects.get(id=batch_slot_id)

        BatchTime.objects.filter(batch_slot=slot).delete()

        current_date = slot.batch.start_date
        end_date = slot.batch.end_date

        while current_date.strftime('%a') != slot.day:
            current_date += timedelta(days=1)

        while current_date <= end_date:
            start_datetime = datetime.combine(current_date, slot.start_time)
            end_datetime = datetime.combine(current_date, slot.end_time)

            BatchTime.objects.create(
                batch=slot.batch,
                batch_slot=slot,
                start_datetime=start_datetime,
                end_datetime=end_datetime
            )
            current_date += timedelta(weeks=1)

        return f"Batch times created for BatchSlot ID: {batch_slot_id}"

    except BatchSlot.DoesNotExist:
        return f"BatchSlot with ID {batch_slot_id} does not exist"
