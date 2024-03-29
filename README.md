# Inkit
This is an SDK to use with Inkit. Learn more at https://inkit.com or signup right away with https://app.inkit.com.

### Installing:

`pip install inkit`

### Usage Examples:
```
import inkit
from inkit.exceptions import InkitClientException, InkitResponseException


inkit.api_token = 'ENTER YOUR API KEY'


# Get list of Folders

try:
    resp = inkit.Folder.list(
        sort='created_at',
        data_description='My'
    )

except InkitResponseException as e:
    print(e)
    print(e.response.data)

except InkitClientException as e:
    print(e)

else:
    print(resp.data.items)


# Create Template (HTML example with inkit_storage destination)

resp = inkit.Template.create(
    name='My HTML template',
    source='html',
    file='<html>My awesome HTML</html>',
    data={
        'width': 6.5,
        'height': 11.5,
        'unit': 'in'
    },
    destinations=[{  # inkit_storage
        'id': 'dest_12345',
        'folder_id': 'fold_12345',
        'expire_after_n_views': 2,
        'required': True,
        'retain_for': {
            'hours': 1
        }
    }]
)
print(resp.data)


# Create Template (DOCX example with inkit_storage and salesforce destinations)

with open('path/to/your/file.docx', 'rb') as f:
    docx = f.read()

resp = inkit.Template.create(
    name='My DOCX template',
    source='docx',
    file=docx,
    data={
        'file_name': 'DOCX template'
    },
    destinations=[
        {
            'id': 'dest_12345',
            'folder_id': 'fold_12345',
            'expire_after_n_views': 2,
            'required': True
        },
        {
            'id': 'dest_123456',
            'type': 'file'
        }
    ]
)
print(resp.data)


# Get list of Templates

resp = inkit.Template.list(
    search='My',
    sort='created_at',
    page=1,
    source='docx'
)
print(resp.data.items)


# Get single Template

resp = inkit.Template.get('tmpl_12345')
print(resp.data)


# Create Render

resp = inkit.Render.create(
    template_id='tmpl_12345',
    merge_parameters={
        'mp1': 'MP1',
        'mp2': 'MP2'
    },
    destinations={
        'inkit_storage': {
            'name': 'My awesome render',
            'description': 'My awesome render description'
        },
        'salesforce': {
            'record_id': 'Your salesforce LinkedEntityId',
            'salesforce_type': 'link',
            'file_name': 'My awesome PDF',
            'description': 'Salesforce PDF description'
        }
    }
)
print(resp.data)


# Get single Render

resp = inkit.Render.get('rend_12345')
print(resp.data)


# Get list of Renders

resp = inkit.Render.list(
    sort='-created_at',
    page_size=2,
    page=1,
    destination_name='salesforce',
    destination_status='completed'
)
print(resp.data.items)


# Get PDF document

resp = inkit.Render.get_pdf('rend_12345')
print(len(resp.content))


# Create renders Batch

resp = inkit.Batch.create(
    template_id='tmpl_123456',
    renders=[
        {
            'merge_parameters': {
                'mp1': 'MP1',
                'mp2': 'MP2'
            },
            'destinations': {
                'inkit_storage': {
                    'name': 'My first batch render',
                    'description': 'My first batch render description'
                },
                'salesforce': {
                    'record_id': 'Your salesforce LinkedEntityId',
                    'salesforce_type': 'link',
                    'file_name': 'My first awesome PDF',
                    'description': 'Salesforce first PDF description'
                }
            }
        },
        {
            'merge_parameters': {
                'mp1': 'MP11',
                'mp2': 'MP22'
            },
            'destinations': {
                'inkit_storage': {
                    'name': 'My second batch render'
                },
                'salesforce': {
                    'record_id': 'Your salesforce LinkedEntityId',
                    'salesforce_type': 'link',
                    'file_name': 'My second awesome PDF',
                    'description': 'Salesforce second PDF description'
                }
            }
        }
    ]
)
print(resp.data)


# Get list of renders Batches

resp = inkit.Batch.list(
    destination_name='inkit_storage'
)
print(resp.data.items)


# Get single renders Batch

resp = inkit.Batch.get('rb_12345')
print(resp.data)


# Get list of Documents

resp = inkit.Document.list(
    search='My'
)
print(resp.data.items)


# Get single Document

resp = inkit.Document.get('doc_12345')
print(resp.data)


# Delete Document

resp = inkit.Document.delete('doc_12345')
print(resp.status_code)


# Get PDF document

resp = inkit.Document.download('doc_12345')
print(len(resp.content))
```
