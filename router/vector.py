from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from pydantic import BaseModel
from typing import List, Tuple
from supabase import create_client, Client
from tempfile import SpooledTemporaryFile
import shutil
import pypandoc

from controls.utills.summarization import llm_evaluate_summaries
from controls.utills.utils import similarity_search
from controls.utills.utils import common_dependencies,  CommonsDep
from controls.utills.utils import ChatMessage
#from controls.utills.llm.qa import get_qa_llm
from controls.utills.parsers.common import file_already_exists
from controls.utills.parsers.txt import process_txt
from controls.utills.parsers.csv import process_csv
from controls.utills.parsers.docx import process_docx
from controls.utills.parsers.pdf import process_pdf
from controls.utills.parsers.notebook import process_ipnyb
from controls.utills.parsers.markdown import process_markdown
from controls.utills.parsers.powerpoint import process_powerpoint
from controls.utills.parsers.html import process_html
from controls.utills.parsers.epub import process_epub
from controls.utills.parsers.audio import process_audio
from controls.utills.crawler import CrawlWebsite

from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse,Response

import logger 

logger = logger.logging.getLogger(__name__)

#from logger import get_logger
#logger = get_logger(__name__)

from fastapi import Request,Depends
from models.db import User
from router.auth import check_token

from fastapi import APIRouter
router = APIRouter()
'''
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#这里会自动下载pandoc
@router.on_event("startup")
async def startup_event():
    pypandoc.download_pandoc()
'''

file_processors = {
    ".txt": process_txt,
    ".csv": process_csv,
    ".md": process_markdown,
    ".markdown": process_markdown,
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
    ".pdf": process_pdf,
    ".html": process_html,
    ".pptx": process_powerpoint,
    ".docx": process_docx,
    ".epub": process_epub,
    ".ipynb": process_ipnyb,
}


async def filter_file(file: UploadFile, enable_summarization: bool, supabase_client: Client):

    print(supabase_client.supabase_key)
    print(supabase_client.storage_url)
    print(supabase_client.auth)
    ok = await file_already_exists(supabase_client, file)
    print(ok)
    #return {"message": f"🤔 {file.filename} already exists.", "type": "warning"}

    if await file_already_exists(supabase_client, file):
        return {"message": f"🤔 {file.filename} already exists.", "type": "warning"}
    elif file.file._file.tell() < 1:
        return {"message": f"❌ {file.filename} is empty.", "type": "error"}
    else:
        file_extension = os.path.splitext(file.filename)[-1]
        if file_extension in file_processors:
            await file_processors[file_extension](file, enable_summarization)
            return {"message": f"✅ {file.filename} has been uploaded.", "type": "success"}
        else:
            return {"message": f"❌ {file.filename} is not supported.", "type": "error"}


@router.post("/vec/upload", response_class=JSONResponse)
async def upload_file(file: UploadFile, enable_summarization: bool = False,current_user:User=Depends(check_token)):
    #commons: CommonsDep, 
    commons = common_dependencies()
    message = await filter_file(file, enable_summarization, commons['supabase'])
    return message

''' 不需要这个函数，统一到api/chat中对话。
@router.post("/vec/chat/")
async def chat_endpoint(commons: CommonsDep, chat_message: ChatMessage,current_user:User=Depends(check_token)):
    history = chat_message.history
    qa = get_qa_llm(chat_message)
    history.append(("user", chat_message.question))

    if chat_message.use_summarization:
        # 1. get summaries from the vector store based on question
        summaries = similarity_search(
            chat_message.question, table='match_summaries')
        # 2. evaluate summaries against the question
        evaluations = llm_evaluate_summaries(
            chat_message.question, summaries, chat_message.model)
        # 3. pull in the top documents from summaries
        logger.info('Evaluations: %s', evaluations)
        if evaluations:
            reponse = commons['supabase'].from_('documents').select(
                '*').in_('id', values=[e['document_id'] for e in evaluations]).execute()
        # 4. use top docs as additional context
            additional_context = '---\nAdditional Context={}'.format(
                '---\n'.join(data['content'] for data in reponse.data)
            ) + '\n'
        model_response = qa(
            {"question": additional_context + chat_message.question})
    else:
        model_response = qa({"question": chat_message.question})
    history.append(("assistant", model_response["answer"]))

    return {"history": history}
'''

@router.post("/vec/crawl/")
async def crawl_endpoint(crawl_website: CrawlWebsite, enable_summarization: bool = False,current_user:User=Depends(check_token)):
    #commons: CommonsDep, 
    commons = common_dependencies()
    file_path, file_name = crawl_website.process()

    # Create a SpooledTemporaryFile from the file_path
    spooled_file = SpooledTemporaryFile()
    with open(file_path, 'rb') as f:
        shutil.copyfileobj(f, spooled_file)

    # Pass the SpooledTemporaryFile to UploadFile
    file = UploadFile(file=spooled_file, filename=file_name)
    message = await filter_file(file, enable_summarization, commons['supabase'])
    return message


@router.post("/vec/explore")
async def explore_endpoint(current_user:User=Depends(check_token)):
    #commons: CommonsDep, 
    commons = common_dependencies()

    response = commons['supabase'].table("documents").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact").execute()
    documents = response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    unique_data = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    # Sort the list of documents by size in decreasing order
    unique_data.sort(key=lambda x: int(x['size']), reverse=True)

    return {"documents": unique_data}


@router.delete("/vec/explore/{file_name}")
async def delete_endpoint(file_name: str,current_user:User=Depends(check_token)):
    #commons: CommonsDep, 
    commons = common_dependencies()
    # Cascade delete the summary from the database first, because it has a foreign key constraint
    commons['supabase'].table("summaries").delete().match(
        {"metadata->>file_name": file_name}).execute()
    commons['supabase'].table("documents").delete().match(
        {"metadata->>file_name": file_name}).execute()
    return {"message": f"{file_name} has been deleted."}


@router.get("/vec/explore/{file_name}")
async def download_endpoint(file_name: str,current_user:User=Depends(check_token)):
    #commons: CommonsDep, 
    commons = common_dependencies()
    response = commons['supabase'].table("documents").select(
        "metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url").match({"metadata->>file_name": file_name}).execute()
    documents = response.data
    # Returns all documents with the same file name
    return {"documents": documents}

'''
@router.get("/vec")
async def root():
    return {"message": "Hello World"}

'''