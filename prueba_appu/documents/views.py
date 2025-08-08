from django.shortcuts import render
from django.http import JsonResponse
from .dynamodb import create_document, get_document_by_id, get_documents_by_name, update_document, delete_document
from .s3_utils import upload_file
import uuid
from datetime import datetime

def create_document_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_name = request.POST.get('file_name')
        
        if not file or not file_name:
            return JsonResponse({'error': 'File and file_name are required.'}, status=400)

        # Upload the file to S3
        s3_file_url = upload_file(file, file_name)

        # Create a document in DynamoDB
        document_id = str(uuid.uuid4())
        document = {
            'id': document_id,
            'file_name': file_name,
            's3_file_url': s3_file_url,
            'created_at': str(datetime.now())
        }

        # Save the document to DynamoDB
        create_document(document)

        return JsonResponse({'id': document_id, 's3_file_url': s3_file_url}, status=201)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def document_list_view(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        if name:
            documents = get_documents_by_name(name)
            return JsonResponse({'documents': documents}, status=200)
        else:
            return JsonResponse({'error': 'Name parameter is required.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def document_delete_view(request, document_id):
    if request.method == 'DELETE':
        try:
            delete_document(document_id)
            return JsonResponse({'message': 'Document deleted successfully.'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)