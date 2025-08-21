from celery import shared_task
from docx import Document
from .models import *

@shared_task(bind=True, max_retries=3)
def process_file(self, file_id):
    try:
        try:
            file_obj = FileUpload.objects.get(id=file_id)
        except FileUpload.DoesNotExist:
            return  
        
        file_path = file_obj.file.path
        word_count = 0

        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                word_count = len(text.split())
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            text = " ".join([para.text for para in doc.paragraphs])
            word_count = len(text.split())
        else:
            file_obj.status = "failed"
            file_obj.save()
            return

        file_obj.word_count = word_count
        file_obj.status = "completed"
        file_obj.save()

        ActivityLog.objects.create(
            user_profile=file_obj.user_profile,
            action="file_processed",
            metadata={"filename": file_obj.filename, "word_count": word_count},
        )

    except Exception as e:
        if file_obj:
            file_obj.status = "failed"
            file_obj.save()
        raise self.retry(exc=e, countdown=60)
