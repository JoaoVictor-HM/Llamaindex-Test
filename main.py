# criar arquivo .env com o seguinte conteúdo: LLAMA_CLOUD_API_KEY="llx-x0NBaFwN8DEWMk7xsuV6UoqxBYQFd41K4vJuaAnEzaGPgIiC"
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from dotenv import load_dotenv

load_dotenv()

llm = Ollama(model="mistral", request_timeout=100.0)

parser = LlamaParse(result_type="markdown")

file_extractor = {
    ".pdf": parser
}

docs = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()


embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(docs,embed_model=embed_model)
query_engine = vector_index.as_query_engine(llm=llm)

while (prompt := "Responda tudo em português!\n" + input("O Que deseja Saber sobre o Documento? (q para sair): ")) != "q":
    result = query_engine.query(prompt)
    print(result)

print("\nBye!")

