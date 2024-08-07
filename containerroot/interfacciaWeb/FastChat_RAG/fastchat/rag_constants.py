EMBED_NAME = "BAAI/bge-m3"
RERANKER_NAME = "BAAI/bge-reranker-base"

TOP_K_RANK = 8
TOP_K_RERANK = 5
TOP_K_SHOW_CARDS = 5

ENCODER_DEVICE='cuda:1'
RANKER_DEVICE='cuda:1'

MIN_DOCS_TO_SHOW = 5
MIN_SHOW_SIM_SCORE = 0.05
MIN_CHUNK_LEN_THRESHOLD = 10

TEMPERATURE = 0.3
TOP_P = 0.85
MAX_NEW_TOKENS = 2048
REP_PENALTY = 1.1

CHUNK_SIZE=512
CHUNK_OVERLAP=0